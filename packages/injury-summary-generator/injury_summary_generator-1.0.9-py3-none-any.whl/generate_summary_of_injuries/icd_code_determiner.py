import csv
import re
from typing import Dict, List, Tuple
import logging
import os
from fuzzywuzzy import fuzz

class ICDCodeDeterminer:
    """
    A class to determine ICD-10 codes from medical diagnoses.

    Attributes:
        icd_codes_path (str): The file path to the ICD-10 codes CSV.
        icd_codes (Dict[str, List[str]]): Mapping from keywords to ICD-10 codes.
        code_to_row (Dict[str, Tuple[str, ...]]): Mapping from ICD-10 codes to their CSV row data.
        description_to_code (Dict[str, str]): Mapping from diagnosis descriptions to ICD-10 codes.
    """

    def __init__(self, icd_codes_file: str):
        """
        Initializes the ICDCodeDeterminer with the given ICD-10 codes file.

        Args:
            icd_codes_file (str): The filename of the ICD-10 codes CSV located in the data directory.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.icd_codes_path = os.path.join(current_dir, 'data', icd_codes_file)
        
        self.icd_codes: Dict[str, List[str]] = self._load_icd_codes(self.icd_codes_path)
        self.code_to_row: Dict[str, Tuple[str, ...]] = self._load_code_to_row(self.icd_codes_path)
        self.description_to_code: Dict[str, str] = self._load_description_to_code(self.icd_codes_path)

    def _load_icd_codes(self, file_path: str) -> Dict[str, List[str]]:
        """
        Loads ICD-10 codes and maps keywords to their corresponding codes.

        Args:
            file_path (str): Path to the ICD-10 codes CSV file.

        Returns:
            Dict[str, List[str]]: A dictionary mapping keywords to lists of ICD-10 codes.
        """
        icd_codes = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                code, description = row[0], row[1]
                keywords = self._extract_keywords(description)
                for keyword in keywords:
                    if keyword not in icd_codes:
                        icd_codes[keyword] = []
                    icd_codes[keyword].append(code)
        return icd_codes

    def _load_code_to_row(self, file_path: str) -> Dict[str, Tuple[str, ...]]:
        """
        Loads a mapping from ICD-10 codes to their full CSV row data.

        Args:
            file_path (str): Path to the ICD-10 codes CSV file.

        Returns:
            Dict[str, Tuple[str, ...]]: A dictionary mapping ICD-10 codes to their row data.
        """
        code_to_row = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                code = row[0]
                code_to_row[code] = tuple(row)
        return code_to_row

    def _load_description_to_code(self, file_path: str) -> Dict[str, str]:
        """
        Loads a mapping from diagnosis descriptions to their corresponding ICD-10 codes.

        Args:
            file_path (str): Path to the ICD-10 codes CSV file.

        Returns:
            Dict[str, str]: A dictionary mapping lowercased descriptions to ICD-10 codes.
        """
        description_to_code = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                code, description = row[0], row[1]
                description_to_code[description.lower()] = code
        return description_to_code

    def _extract_keywords(self, description: str) -> List[str]:
        """
        Extracts significant keywords from a diagnosis description.

        Args:
            description (str): The diagnosis description.

        Returns:
            List[str]: A list of keywords extracted from the description.
        """
        words = re.findall(r'\b\w+\b', description.lower())
        return [word for word in words if len(word) > 2 and word not in ['and', 'the', 'with', 'without', 'due', 'to']]

    def determine_icd_code(self, diagnosis: str) -> str:
        if not diagnosis or diagnosis.lower() == "illness unspecified":
            return "R69"  # Fixed: Now correctly returns R69 for "Illness unspecified"

        # Check for exact match first
        if diagnosis.lower() in self.description_to_code:
            return self.description_to_code[diagnosis.lower()]

        diagnosis_keywords = self._extract_keywords(diagnosis)
        possible_codes = []
        for keyword in diagnosis_keywords:
            if keyword in self.icd_codes:
                possible_codes.extend(self.icd_codes[keyword])
        
        if not possible_codes:
            return "R69"  # Illness, unspecified

        # Rank possible codes using fuzzy matching
        ranked_codes = []
        for code in set(possible_codes):
            description = self.code_to_row[code][1]  # Assuming description is the second column
            score = fuzz.token_set_ratio(diagnosis.lower(), description.lower())
            
            # Boost score for more specific codes
            if len(code) > 3:
                score += 10
            
            # Boost score for codes that match important keywords
            important_keywords = ['leukemia', 'cholera', 'typhoid', 'tuberculosis', 'pneumonia']
            if any(keyword in description.lower() for keyword in important_keywords):
                score += 15

            ranked_codes.append((code, score))
        
        # Sort by score in descending order and return the top match
        ranked_codes.sort(key=lambda x: x[1], reverse=True)
        return ranked_codes[0][0]

    def get_full_row_by_code(self, code: str) -> Tuple[str, ...]:
        return self.code_to_row.get(code, tuple())

# Usage
icd_determiner = ICDCodeDeterminer('icd10_codes.csv')

def determine_icd_code(diagnosis: str) -> str:
    icd_code = icd_determiner.determine_icd_code(diagnosis)
    logging.info(f"Determined ICD code {icd_code} for diagnosis: {diagnosis}")
    return icd_code

def get_full_row_by_code(code: str) -> Tuple[str, ...]:
    return icd_determiner.get_full_row_by_code(code)