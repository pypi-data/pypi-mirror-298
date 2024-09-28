import os
import logging
from .pdf_reader import read_pdf_files, extract_text_from_pdf
from .date_extractor import extract_date
from .diagnosis_extractor import extract_diagnosis
from .icd_code_determiner import determine_icd_code
from .pdf_creator import create_summary_pdf

def process_pdf_files(input_folder: str):
    """
    Process all PDF files in the input folder and extract relevant information.

    Args:
        input_folder (str): Path to the folder containing input PDF files.

    Returns:
        list: A list of dictionaries containing extracted information from each PDF.
    """
    pdf_files = read_pdf_files(input_folder)
    records = []

    for pdf_file in pdf_files:
        logging.info(f"Processing file: {pdf_file}")
        text = extract_text_from_pdf(pdf_file)
        date = extract_date(text)
        diagnosis = extract_diagnosis(text)
        
        record = {
            'date': date,
            'diagnosis': diagnosis,
            'icd_code': determine_icd_code(diagnosis),
            'reference': f"{os.path.basename(pdf_file)} - p. 1"  # Assuming the diagnosis is on the first page
        }
        
        records.append(record)

    return records

def sort_records(records):
    """
    Sort the records by date in descending order.

    Args:
        records (list): List of record dictionaries.

    Returns:
        list: Sorted list of record dictionaries.
    """
    return sorted(records, key=lambda x: x['date'], reverse=True)

def generate_summary(input_folder: str, output_folder: str):
    """
    Generate a summary of injuries from PDF files.

    Args:
        input_folder (str): Path to the folder containing input PDF files.
        output_folder (str): Path to the folder where the output PDF will be saved.
    """
    logging.info(f"Starting to process files from {input_folder}")
    
    # Process PDF files and extract records
    records = process_pdf_files(input_folder)
    
    # Sort the records by date
    sorted_records = sort_records(records)
    
    # Generate the output PDF file
    output_file = os.path.join(output_folder, "summary_of_injuries.pdf")
    create_summary_pdf(sorted_records, output_file)
    
    logging.info(f"Summary PDF created: {output_file}")