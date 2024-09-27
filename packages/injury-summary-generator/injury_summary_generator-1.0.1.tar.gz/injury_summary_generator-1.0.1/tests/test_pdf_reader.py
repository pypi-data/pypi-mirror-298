import os
import tempfile
import pytest
from src.pdf_reader import read_pdf_files, extract_text_from_pdf

def test_extract_text_from_pdf():
    test_pdf_path = 'test_input/test.pdf'
    expected_text = "This is a test PDF document. If you can read this, you have Adobe Acrobat Reader installed on your computer."
    
    # Check if the file exists
    assert os.path.exists(test_pdf_path), f"Test PDF file does not exist at {test_pdf_path}"
    
    extracted_text = extract_text_from_pdf(test_pdf_path)
    
    # Print the extracted text for debugging
    print(f"Extracted text: {extracted_text}")
    
    # Normalize whitespace for comparison
    normalized_extracted_text = ' '.join(extracted_text.split())
    normalized_expected_text = ' '.join(expected_text.split())
    
    print(f"Extracted text: {normalized_extracted_text}")
    print(f"Expected text: {normalized_expected_text}")

    assert normalized_extracted_text == normalized_expected_text

def test_read_pdf_files_empty_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        result = read_pdf_files(temp_dir)
        assert len(result) == 0

def test_read_pdf_files_nonexistent_directory():
    with pytest.raises(FileNotFoundError):
        read_pdf_files('/nonexistent/directory')
