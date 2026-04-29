import pandas as pd
import excel_constants as ec
class ExcelAdapter:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self, sheet_name):
        pd.read_excel(ec.EXCEL_FILE_PATH, skiprows=ec.SKIP_ROWS, usecols=ec.USE_COLUMNS)
        
        pass

    def write_excel(self, data):
        # Implement logic to write data to Excel file
        pass