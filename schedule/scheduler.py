from time import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import logging
import pytz

logging.basicConfig(level=logging.INFO)

def run_etl():
    logging.info("Iniciando ETL...")

    procs = []
    scripts = [
        ["python", "ingestion/ip_quality_score_ingest.py"],
        ["python", "ingestion/vt_ingest.py"],
        ["python", "ingestion/alien_vault_ingest.py"]
    ]

    for script in scripts:
        procs.append(subprocess.Popen(script))

    for p in procs:
        p.wait()

# Define timezone
madrid_tz = pytz.timezone("Europe/Madrid")
scheduler = BlockingScheduler(timezone=madrid_tz)

scheduler.add_job(run_etl, "cron", hour=11, minute=35)
scheduler.start()
