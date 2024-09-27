import re
from typing import Dict, List, Tuple
import logging
from fuzzywuzzy import fuzz
from generate_summary_of_injuries.icd_codes_data import ICD_CODES

class ICDCodeDeterminer:
    """
    A class to determine ICD-10 codes from medical diagnoses.

    Attributes:
        icd_codes (Dict[str, List[str]]): Mapping from keywords to ICD-10 codes.
        code_to_description (Dict[str, str]): Mapping from ICD-10 codes to their descriptions.
        description_to_code (Dict[str, str]): Mapping from diagnosis descriptions to ICD-10 codes.
    """

    def __init__(self):
        """
        Initializes the ICDCodeDeterminer with the ICD codes from icd_codes_data.py.
        """
        self.icd_codes: Dict[str, List[str]] = self._load_icd_codes()
        self.code_to_description: Dict[str, str] = {code: desc for code, desc in ICD_CODES}
        self.description_to_code: Dict[str, str] = {desc.lower(): code for code, desc in ICD_CODES}

    def _load_icd_codes(self) -> Dict[str, List[str]]:
        """
        Loads ICD-10 codes and maps keywords to their corresponding codes.

        Returns:
            Dict[str, List[str]]: A dictionary mapping keywords to lists of ICD-10 codes.
        """
        icd_codes = {}
        for code, description in ICD_CODES:
            keywords = self._extract_keywords(description)
            for keyword in keywords:
                if keyword not in icd_codes:
                    icd_codes[keyword] = []
                icd_codes[keyword].append(code)
        return icd_codes

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
            description = self.code_to_description[code]
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

    def get_description_by_code(self, code: str) -> str:
        return self.code_to_description.get(code, "")

# Usage
icd_determiner = ICDCodeDeterminer()

def determine_icd_code(diagnosis: str) -> str:
    icd_code = icd_determiner.determine_icd_code(diagnosis)
    logging.info(f"Determined ICD code {icd_code} for diagnosis: {diagnosis}")
    return icd_code

def get_description_by_code(code: str) -> str:
    return icd_determiner.get_description_by_code(code)