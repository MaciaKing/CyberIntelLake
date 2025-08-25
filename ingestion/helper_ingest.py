from datetime import datetime
from pathlib import Path

def get_file_to_extract():
    """
    This function selects which file to extract based on the current day of the month.
    - If the day number is even, it chooses "black_list_domain.txt".
    - If the day number is odd, it chooses "otro_fichero.txt".
    The purpose is to alternate the file used depending on whether the day is even or odd.
    """
    today = datetime.today().day
    if today % 2 == 0:
        file_path_to_extract = Path(__file__).parent / '../data_to_extract/black_list_domain.txt'
    else:
        file_path_to_extract = Path(__file__).parent / '../data_to_extract/white_list_domain.txt'
    return file_path_to_extract
