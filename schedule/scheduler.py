from time import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import logging
import pytz

logging.basicConfig(level=logging.INFO)

def run_etl():
    logging.info("Iniciando ETL...")
    subprocess.run(["python", "ingestion/vt_ingest.py"], check=True)

# Define timezone
madrid_tz = pytz.timezone("Europe/Madrid")
scheduler = BlockingScheduler(timezone=madrid_tz)

scheduler.add_job(run_etl, "cron", hour=17, minute=2)
scheduler.start()
