import os
# from pii_scanner.file.usage_files_csv import csv_file_pii_detector
# from pii_scan.core.usage_files_json import json_file_pii_detector
# from pii_scan.core.usage_files_xlsx import xlsx_file_pii_detector
# from pii_scan.Octopii.octopii_pii_detector import process_file_octopii
# from pii_scan.core.usage_text_docs_pdf import file_pii_detector
# from pii_scan.structured_ner_main import 
from core.structured import ScannerForStructuredData
from typing import List, Any, Optional
import logging
import traceback

class PIIScanner:
    def __init__(self):
        # Initialize the structured data scanner
        self.scanner = ScannerForStructuredData()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def scan_structured_data(self, data: Optional[List[dict]] = None, sample_size: float = 0.2, chunk_size: int = 1000) -> List[dict]:
        """
        Scan structured data for PII.

        Parameters:
        - data: The structured data to scan (list of dictionaries)
        - sample_size: Percentage of the data to sample
        - chunk_size: Size of data chunks to process at a time

        Returns:
        - List of detected PII entities.
        """
        if not data:
            self.logger.warning("No data provided for structured data scanning.")
            return []


        # Scan using NERScannerForStructuredData
        results = self.scanner.scan(data, chunk_size=chunk_size, sample_size=sample_size)
        return results.get("results", [])


# # Example usage:
# if __name__ == "__main__":
#     pii_scanner = PIIScanner()
#     data = ["Ankit Gupta", "Lucknow", "+9191840562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian"]
#     results = pii_scanner.scan_structured_data(data, chunk_size=10, sample_size=1.0)
#     print(results)