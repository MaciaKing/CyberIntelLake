import time
import os
import json
from models.database import SessionLocal
from models.virus_total import VirusTotal
from models.file_reader import FileReader
from pathlib import Path
from datetime import datetime

# File to extract data
file_path_to_extract = Path(__file__).parent / '../data_to_extract/black_list_domain.txt'
fr = FileReader(file_path_to_extract)

# Create database session
database_session = SessionLocal()
vt = VirusTotal(os.getenv('VIRUS_TOTAL_API_KEY'))

# Load last progress or create it
progress = vt.find_or_create_progress(file_path_to_extract, database_session)
OUTPUT_FILE = Path(__file__).parent / F"../data/bronze/virus_total/virus_total_batch{progress.last_batch_number_extracted}.ndjson"

request_day_counter = 0

try:
    while request_day_counter <= vt.MAX_REQUEST_PER_DAY:
        domain_to_query = fr.read_line(progress.last_line_read)
        # The file has been read completely.
        if not domain_to_query:
            break
        record = vt.make_domain_query(domain_to_query)

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

        print(f"{domain_to_query} processed")

        # Wait time between requests
        time.sleep(vt.get_waiting_time_between_requests())

finally:
    progress.last_batch_number_extracted +=1
    progress.save(database_session)
    print(f"ELT for Virus Total finished at {datetime.now()}")
