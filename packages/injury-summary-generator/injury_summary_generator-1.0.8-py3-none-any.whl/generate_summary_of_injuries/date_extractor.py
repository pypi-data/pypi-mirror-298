import re
from typing import Optional, List
from dateutil import parser
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_text(text: str) -> str:
    """
    Preprocess the text to correct common corruption patterns in dates.
    
    Args:
        text (str): The input text with potential corrupted dates.
    
    Returns:
        str: The preprocessed text with corrected date formats.
    """
    logging.info("Starting preprocessing of text.")
    
    # Remove non-printable or corrupt characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    logging.debug(f"Text after removing non-ASCII characters: {text[:100]}...")  # Show first 100 chars
    
    # Correct common date corruption patterns, e.g., '2 021' to '2021'
    # This pattern finds digits separated by a space and removes the space
    text = re.sub(r'(\d)\s+(\d)', r'\1\2', text)
    logging.debug(f"Text after correcting separated digits: {text[:100]}...")
    
    return text

def extract_date(text: str) -> Optional[str]:
    """
    Extract the most likely visit date from the given text using contextual analysis.
    
    This function preprocesses the text to correct common corruptions, identifies all
    potential dates, classifies them based on surrounding keywords, and selects the
    most probable visit date.
    
    Args:
        text (str): The input text containing date information.
    
    Returns:
        Optional[str]: The extracted visit date in 'YYYY-MM-DD' format,
                       or 'Date not found' if no valid date is found.
    """
    logging.info("Starting date extraction process.")
    
    # Preprocess the text to fix common corruption issues
    cleaned_text = preprocess_text(text)
    
    # Define regex patterns
    date_pattern = r'\b(\d{1,4}[-/\s.]\d{1,2}[-/\s.]\d{1,4}|' \
                  r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{2,4}|' \
                  r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}(?:st|nd|rd|th)?\s*,?\s*\d{2,4})\b'
    potential_dates = list(re.finditer(date_pattern, cleaned_text, re.IGNORECASE))
    
    # Define keyword patterns
    visit_keywords = ['visit', 'appointment', 'seen']
    birth_keywords = ['birth', 'born', 'dob']
    
    # Extract all dates with their positions
    dates = []
    for match in potential_dates:
        dates.append({
            'text': match.group(0),
            'start': match.start(),
            'end': match.end()
        })
        logging.debug(f"Found date: {match.group(0)} at positions {match.start()}-{match.end()}")
    
    # Extract positions of keywords
    keyword_positions = {
        'visit': [],
        'birth': []
    }
    
    for keyword in visit_keywords:
        for match in re.finditer(rf'\b{keyword}\w*\b', cleaned_text, re.IGNORECASE):
            keyword_positions['visit'].append(match.start())
            logging.debug(f"Found visit keyword '{match.group(0)}' at position {match.start()}")
    
    for keyword in birth_keywords:
        for match in re.finditer(rf'\b{keyword}\w*\b', cleaned_text, re.IGNORECASE):
            keyword_positions['birth'].append(match.start())
            logging.debug(f"Found birth keyword '{match.group(0)}' at position {match.start()}")
    
    # Function to determine nearest keyword distance
    def nearest_distance(pos: int, keyword_list: List[int]) -> Optional[int]:
        if not keyword_list:
            return None
        return min(abs(pos - kw_pos) for kw_pos in keyword_list)
    
    # Classify dates
    classified_dates = []
    for date in dates:
        date_str = date['text']
        date_pos = date['start']
    
        # Determine proximity to keywords
        visit_dist = nearest_distance(date_pos, keyword_positions['visit'])
        birth_dist = nearest_distance(date_pos, keyword_positions['birth'])
    
        # Attempt to parse the date
        try:
            parsed_date = parser.parse(date_str, fuzzy=True)
            
            # Correct two-digit years
            if parsed_date.year < 100:
                parsed_date = parsed_date.replace(year=2000 + parsed_date.year)
            
            classified_dates.append({
                'original_str': date_str,
                'parsed_date': parsed_date,
                'visit_dist': visit_dist if visit_dist is not None else float('inf'),
                'birth_dist': birth_dist if birth_dist is not None else float('inf')
            })
            logging.debug(f"Parsed date: {parsed_date} from '{date_str}' with visit distance {visit_dist} and birth distance {birth_dist}")
        except ValueError as e:
            logging.debug(f"Error parsing date '{date_str}': {e}")
            continue
    
    if not classified_dates:
        logging.warning("No valid dates found in the text.")
        return "Date not found"
    
    # Identify birth dates to establish a reference
    birth_dates = [d for d in classified_dates if d['birth_dist'] < d['visit_dist']]
    latest_birth_date = max(birth_dates, key=lambda x: x['parsed_date']) if birth_dates else None
    
    # Filter visit dates that are after birth dates
    visit_dates = []
    for d in classified_dates:
        if d['visit_dist'] < d['birth_dist']:
            if not latest_birth_date or d['parsed_date'] > latest_birth_date['parsed_date']:
                visit_dates.append(d)
    
    if not visit_dates:
        logging.warning("No valid visit dates found in the text.")
        return "Date not found"
    
    # Select the closest visit date
    visit_dates.sort(key=lambda x: (x['visit_dist'], -x['parsed_date'].timestamp()))
    best_visit_date = visit_dates[0]
    
    logging.info(f"Best visit date: {best_visit_date['parsed_date'].strftime('%Y-%m-%d')} from '{best_visit_date['original_str']}'")
    return best_visit_date['parsed_date'].strftime('%Y-%m-%d')

# Example usage
if __name__ == "__main__":
    sample_texts = [
        "Patient visited on 07/26/2021 for a follow-up appointment.",
        "The patient was seen on January 15, 2021. Date of birth: 05/12/1980.",
        "Appointment Date: 15 Jan 2021",
        "Patient was seen in our clinic on 05/12/2022. Born on 11/30/1975.",
        "Last visited: 11-30-2023",
        "Visit record: 2023.06.15 - Patient reported feeling much better.",
        "Visit date: 07/26/2021 (Corrected: 07/26/2021)",
        "The visit on 2023-05-01 was rescheduled. New appointment date is 2023-06-15. DOB: 1990-03-22",
        "Visit date: 07/26/2 021"  # Corrupted date with space
    ]
    for text in sample_texts:
        result = extract_date(text)
        print(f"Input: {text}\nExtracted date: {result}\n")