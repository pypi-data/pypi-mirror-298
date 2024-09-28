"""
pdf_reader.py

This module provides functionality for reading PDF files and extracting their
text content. It is a crucial component of the Injury Summary Generator project,
responsible for the initial step of processing medical records.

Key functions:
1. read_pdf_files: Identifies all PDF files in a specified directory.
2. extract_text_from_pdf: Extracts text content from a single PDF file.

Dependencies:
- pypdf: For reading and extracting text from PDF files. 
  Install using: pip install pypdf

Usage:
This module is typically imported and used by the main script
(main.py) but can also be used independently
for PDF processing tasks.
"""

import os
import logging
from typing import List
from pypdf import PdfReader

def read_pdf_files(input_folder: str) -> List[str]:
    """
    Read all PDF files from the specified input folder.

    This function scans the input folder for files with a '.pdf' extension
    (case-insensitive) and returns their full paths.

    Args:
    input_folder (str): Path to the folder containing input PDF files.

    Returns:
    List[str]: A list of file paths for all PDF files in the input folder.
    """
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"The directory {input_folder} does not exist.")
    
    pdf_files = []
    
    # Iterate through all files in the input folder
    for file in os.listdir(input_folder):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(input_folder, file))
    
    logging.info(f"Found {len(pdf_files)} PDF files in {input_folder}")
    
    return pdf_files

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file and save it to data/output directory.

    Args:
    pdf_path (str): Path to the PDF file.

    Returns:
    str: Extracted text content from the PDF.
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        logging.info(f"Successfully extracted text from {pdf_path}")
        
        return text
    except Exception as e:
        logging.error(f"Error reading PDF {pdf_path}: {str(e)}")
        return ""

# You can add more PDF-related functions here as needed