"""
This module provides functionality for extracting and formatting diagnoses from medical record texts.
It contains functions to parse the text, locate relevant sections, and extract the primary diagnosis or chief complaint.
The extracted information is then formatted for consistency and returned.

Logging is used to track the extraction process and any potential issues.
"""

import re
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_diagnosis(text: str) -> Optional[str]:
    """
    Extract the primary diagnosis from a medical record text.

    This function attempts to find the primary diagnosis in the following order:
    1. Look for 'Primary Diagnosis', 'Diagnosis', or 'Prognosis' in the Assessment section.
    2. If not found, use the Chief Complaint as a fallback.

    Args:
    text (str): The full text of the medical record.

    Returns:
    str: The extracted diagnosis, formatted for consistency.
         Returns "Diagnosis not found" if no diagnosis could be extracted.

    Note:
    This function assumes the presence of an 'Assessment' section in the medical record.
    If such a section is absent, it may not extract the diagnosis correctly.
    """
    # Search for the Assessment section
    assessment_match = re.search(r'Assessment:(.+?)(?:\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
    if assessment_match:
        assessment_text = assessment_match.group(1)
        # Look for Primary Diagnosis, Diagnosis, or Prognosis within the Assessment section
        diagnosis_match = re.search(r'(?:Primary Diagnosis|Diagnosis|Prognosis)\s*:(.+?)(?:\n|$)', assessment_text, re.IGNORECASE)
        if diagnosis_match:
            diagnosis = format_diagnosis(diagnosis_match.group(1))
            logging.info(f"Successfully extracted diagnosis: {diagnosis}")
            return diagnosis
    
    # If no diagnosis found in Assessment, look for Chief Complaint
    chief_complaint_match = re.search(r'Chief Complaint:(.+?)(?:\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
    if chief_complaint_match:
        diagnosis = format_diagnosis(chief_complaint_match.group(1))
        logging.info(f"Successfully extracted chief complaint as diagnosis: {diagnosis}")
        return diagnosis
    
    # If no diagnosis or chief complaint found, return a default message
    logging.warning("No diagnosis or chief complaint found")
    return "Illness unspecified"

def format_diagnosis(diagnosis: str) -> str:
    """
    Format the extracted diagnosis for consistency.

    This function performs the following operations:
    1. Removes excess whitespace and newlines.
    2. Removes leading colons and spaces.
    3. Capitalizes the first letter of the diagnosis.

    Args:
    diagnosis (str): The raw extracted diagnosis text.

    Returns:
    str: The formatted diagnosis text.
    """
    # Remove excess whitespace and newlines
    diagnosis = re.sub(r'\s+', ' ', diagnosis).strip()
    # Remove leading colons and spaces
    diagnosis = re.sub(r'^:\s*', '', diagnosis)
    # Capitalize the first letter
    formatted_diagnosis = diagnosis[0].upper() + diagnosis[1:] if diagnosis else "Illness unspecified"
    logging.info(f"Formatted diagnosis: {formatted_diagnosis}")
    return formatted_diagnosis