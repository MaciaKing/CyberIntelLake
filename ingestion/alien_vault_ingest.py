import time
import os
import json
from ingestion.helper_ingest import get_file_to_extract, get_logging_config
from models.database import SessionLocal
from models.alien_vault import AlienVault
from models.file_reader import FileReader
from pathlib import Path
from datetime import datetime

logger = get_logging_config('AlienVault ELT')

# File to extract data
file_path_to_extract = get_file_to_extract()
fr = FileReader(file_path_to_extract)

# Create database session
database_session = SessionLocal()
av = AlienVault(os.getenv('ALIEN_VAULT_OTX_KEY'))

# Load last progress or create it
progress = av.find_or_create_progress(file_path_to_extract, database_session)
OUTPUT_FILE = Path(__file__).parent / F"../data/bronze/alien_vault/alien_vault_batch{progress.last_batch_number_extracted}.ndjson"

request_day_counter = 0

try:
    while request_day_counter <= av.MAX_REQUEST_PER_DAY:
        domain_to_query = fr.read_line(progress.last_line_read)
        # The file has been read completely.
        if not domain_to_query:
            break

        try:
            record = av.search_pulses_top10(domain_to_query)
        except Exception as e:
            logger.info(f"Error con {domain_to_query}: {e}")
            record = {}

        # Encapsulate the record with the domain and the
        # name of the file from which it was extracted.
        wrapped_record = {
            "id": domain_to_query,
            "file_extracted": str(file_path_to_extract),
            "response": record
        }

        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(wrapped_record, ensure_ascii=False) + "\n")

        # Save last line read of AV extraction
        progress.last_line_read += 1
        progress.save(database_session)
        request_day_counter += 1

        logger.info(f"{domain_to_query} processed")

        # Wait time between requests
        time.sleep(av.get_waiting_time_between_requests())

finally:
    progress.last_batch_number_extracted +=1
    progress.save(database_session)
    logger.info(f"ELT for Alien Vault finished at {datetime.now()}")
