import os, time
from urllib.parse import quote
from models.file_progress import FileProgress
import requests

class AlienVault:
    def __init__(self, api_key):
        """
        Class to interact with the AlienVault OTX API.
        
        Official documentation on request limits:
        https://success.alienvault.com/s/question/0D53q0000ADUdhBCQT/api-requests-limit
        
        Important note:
        The limit with an API key is 10,000 requests per hour.
        This limit may change without prior notice.
        """
        self.api_key = api_key
        self.header = {"X-OTX-API-KEY": self.api_key}
        self.session = requests.Session()
        self.session.headers.update(self.header)
        self.MAX_REQUEST_PER_DAY = 240000
        self.MAX_REQUESTS_PER_HOUR = 10000  

    def _get(self, url, params=None, max_retries=5):
        for i in range(max_retries):
            r = self.session.get(url, params=params, timeout=50)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 2)) or (2 * (i + 1))
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        raise RuntimeError("Too many 429s from OTX")

    def pulses_for_url(self, url: str):
        enc = quote(url, safe="")  # importante para / en URLs
        data = self._get(f"https://otx.alienvault.com/api/v1/indicators/url/{enc}/general")
        return data.get("pulse_info", {}).get("pulses", [])

    def pulses_for_hostname(self, hostname: str):
        data = self._get(f"https://otx.alienvault.com/api/v1/indicators/hostname/{hostname}/general")
        return data.get("pulse_info", {}).get("pulses", [])

    def pulses_for_domain(self, domain: str):
        data = self._get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general")
        return data.get("pulse_info", {}).get("pulses", [])

    def search_pulses(self, query: str, limit=50, max_pages=5):
        base = "https://otx.alienvault.com/api/v1/search/pulses"
        all_hits = []
        for page in range(1, max_pages + 1):
            data = self._get(base, params={"q": query, "sort": "-modified", "limit": limit, "page": page})
            hits = data.get("results", []) or data.get("pulses", []) or []
            if not hits: break
            all_hits.extend(hits)
            if len(hits) < limit: break
            time.sleep(1) 
        return all_hits
    
    def search_pulses_top10(self, query: str):
        base = "https://otx.alienvault.com/api/v1/search/pulses"
        data = self._get(base, params={"q": query, "sort": "-modified", "limit": 10, "page": 1})
        # 'results' o 'pulses' depende de la versión del API
        hits = data.get("results", []) or data.get("pulses", [])
        return hits[:10]  # asegúrate de no pasar de 10 aunque la API devuelva más
    
    def find_or_create_progress(self, file_path, db_session):
        """Find existing progress for file or create a new one"""
        progress = db_session.query(FileProgress).filter_by(
            file_path=str(file_path),
            extracted_from='AlienVault'
        ).first()
        if not progress:
            progress = FileProgress(file_path=str(file_path), extracted_from='AlienVault', last_line_read=0)
            db_session.add(progress)
            db_session.commit()
        return progress
    
    def get_waiting_time_between_requests(self):
        return int(2)

# Ejemplo de uso correcto con tu indicador de ejemplo (hostname):
# alv = AlienVault(os.getenv("ALIEN_VAULT_OTX_KEY"))
# pulses = alv.pulses_for_hostname("27c73bq66y4xqoh7.dorfact.at")
# print(pulses)
