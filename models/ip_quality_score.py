
from models.helper import Helper
from models.file_progress import FileProgress

class IpQualityScore:
    """
    This class is to connect your code to the IPQualityScore API.
    For more information on the API, visit:
    https://www.ipqualityscore.com/documentation/malicious-url-scanner-api/overview

    API Usage Notes:
        - The free plan typically allows a limited number of monthly requests (e.g. 1,000).
        - URLs and IPs can be rescanned a limited number of times within a certain period (e.g. 35 days).
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url_scanner = f"https://www.ipqualityscore.com/api/json/url/{self.api_key}/"
        self.base_ip_scanner = f"https://www.ipqualityscore.com/api/json/ip/{self.api_key}/"
        self.MAX_REQUEST_PER_DAY = 35
        self.MONTHLY_REQUEST = 1000

    def scan_url(self, url_to_scan):
        """
        scan_url

        Description:
            - Make a URL query to the IPQualityScore API.

        Params:
            - url_to_scan (string): The full URL to be analyzed.

        Functionality:
            - Creates a request to the IPQualityScore endpoint to check for threats such as phishing or malware.

        Returns:
            - A 'dict' (JSON) object containing the scan results.
        """
        endpoint = self.base_url_scanner + url_to_scan
        return Helper.make_query(endpoint, header=None)
    
    def scan_ip(self, url_to_scan):
        """
        scan_ip

        Description:
            - Make an IP query to the IPQualityScore API.

        Params:
            - ip_to_scan (string): The IP address to be analyzed.

        Functionality:
            - Creates a request to the IPQualityScore endpoint to check for malicious activity or risk level.

        Returns:
            - A 'dict' (JSON) object containing the scan results.
        """
        endpoint = self.base_ip_scanner + url_to_scan
        return Helper.make_query(endpoint, header=None)
    
    def find_or_create_progress(self, file_path, db_session):
        """
        find_or_create_progress

        Description:
            - Find an existing progress record for a given file or create one if it doesn't exist.

        Params:
            - file_path (string): The full path of the file being processed.
            - db_session (Session): SQLAlchemy session object used to interact with the database.

        Functionality:
            - Checks if there is already a progress record for the specified file path in the database.
            - If found, it returns the existing record.
            - If not found, it creates a new `FileProgress` entry with `last_line_read = 0`,
              adds it to the session, commits it to the database, and then returns it.

        Returns:
            - A `FileProgress` object representing the current progress for the specified file.
        """
        progress = db_session.query(FileProgress).filter_by(
            file_path=str(file_path),
            extracted_from='IpQualityScore'
        ).first()

        if not progress:
            progress = FileProgress(file_path=str(file_path), extracted_from='IpQualityScore', last_line_read=0)
            db_session.add(progress)
            db_session.commit()
        return progress
    
    def get_waiting_time_between_requests(self):
        return 2