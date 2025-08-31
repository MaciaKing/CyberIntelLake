import time
import os
import json
from ingestion.helper_ingest import get_file_to_extract, get_logging_config
from database.database import SessionLocal
from models.virus_total import VirusTotal
from models.file_reader import FileReader
from models.batch_progres import LastBatchNumber
from pathlib import Path
from datetime import datetime

logger = get_logging_config('Virus Total ELT')

# File to extract data
file_path_to_extract = get_file_to_extract()
fr = FileReader(file_path_to_extract)

# Create database session
database_session = SessionLocal()
lbn = LastBatchNumber()

vt = VirusTotal(os.getenv('VIRUS_TOTAL_API_KEY'))

# Load last progress or create it
progress = vt.find_or_create_progress(file_path_to_extract, database_session)

vt_lbn_instance = lbn.find_or_create(database_session, 'VirusTotal')
OUTPUT_FILE = Path(__file__).parent / F"../data/bronze/virus_total/virus_total_batch_{vt_lbn_instance.last_batch_number_extracted + 1}.ndjson"

request_day_counter = 0

try:
    while request_day_counter <= vt.MAX_REQUEST_PER_DAY:
        domain_to_query = fr.read_line(progress.last_line_read)
        # The file has been read completely.
        if not domain_to_query:
            break
        
        try:
            record = vt.make_domain_query(domain_to_query)
        except Exception as e:
            logger.warning(f"Error querying domain '{domain_to_query}': {e}")
            # In some URLs, the VirusTotal query does not work properly.
            progress.last_line_read += 1
            progress.save(database_session)
            continue

        # Encapsulate the record with the domain and the
        # name of the file from which it was extracted.
        wrapped_record = {
            "id": domain_to_query,
            "file_extracted": str(file_path_to_extract),
            "response": record
        }

        # Save record as NDJSON
        # batch
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(wrapped_record, ensure_ascii=False) + "\n")

        # Save last line read of VT extraction
        progress.last_line_read += 1
        progress.save(database_session)
        request_day_counter += 1

        logger.info(f"{domain_to_query} processed")

        # Wait time between requests
        time.sleep(vt.get_waiting_time_between_requests())

finally:
    vt_lbn_instance.last_batch_number_extracted +=1
    vt_lbn_instance.save(database_session)
    logger.info(f"ELT for Virus Total finished at {datetime.now()}")
