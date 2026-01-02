from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import logging
import pytz
from filelock import FileLock, Timeout
import threading

logging.basicConfig(level=logging.INFO)

SCRIPTS = {
    "vt": {
        "cmd": ["python3", "ingestion/vt_ingest.py"],
        "locks": ["/tmp/vt_1.lock", "/tmp/vt_2.lock"]  # máx 2
    },
    "alien": {
        "cmd": ["python3", "ingestion/alien_vault_ingest.py"],
        "locks": ["/tmp/alien.lock"]  # máx 1
    }
}

def launch_script(name, cfg):
    for lock_path in cfg["locks"]:
        lock = FileLock(lock_path)
        try:
            lock.acquire(timeout=0)
            logging.info(f"Launched {name}")

            def _run():
                try:
                    subprocess.run(cfg["cmd"])
                finally:
                    lock.release()
                    logging.info(f"{name} finished")

            threading.Thread(target=_run, daemon=True).start()
            return

        except Timeout:
            continue

    logging.warning(f"{name}: Execution is already in progress, it is not launched")

def run_etl():
    logging.info("*** ETL Init ***")

    for name, cfg in SCRIPTS.items():
        launch_script(name, cfg)

scheduler = BlockingScheduler(timezone=pytz.UTC)

scheduler.add_job(
    run_etl,
    "cron",
    hour=17,
    minute=27,
    max_instances=1,
    coalesce=False
)

scheduler.start()
