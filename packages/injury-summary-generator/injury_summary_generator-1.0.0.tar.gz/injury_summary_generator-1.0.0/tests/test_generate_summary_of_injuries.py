import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.generate_summary_of_injuries import process_pdf_files, sort_records, main
from src.pdf_reader import read_pdf_files, extract_text_from_pdf
from src.diagnosis_extractor import extract_diagnosis
from src.date_extractor import extract_date
from src.icd_code_determiner import determine_icd_code


# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


@pytest.fixture
def mock_dependencies(mocker):
    # Mock dependencies to isolate the tests from actual implementations
    mocker.patch('src.pdf_reader.read_pdf_files')
    mocker.patch('src.pdf_reader.extract_text_from_pdf')
    mocker.patch('src.diagnosis_extractor.extract_diagnosis')
    mocker.patch('src.date_extractor.extract_date')
    mocker.patch('src.icd_code_determiner.determine_icd_code')
    mocker.patch('src.pdf_creator.create_summary_pdf')

def test_process_pdf_files(mock_dependencies):
    """
    Test the process_pdf_files function to ensure it processes PDF files correctly.

    This test mocks the dependencies to simulate the behavior of reading PDF files,
    extracting text, extracting diagnosis and date, and determining ICD codes. It then verifies
    that the process_pdf_files function returns the expected results.
    """

    # Mock the return values of the dependencies
    read_pdf_files.return_value = ['file1.pdf', 'file2.pdf']
    extract_text_from_pdf.return_value = 'Sample text'
    extract_diagnosis.return_value = 'Test'
    extract_date.return_value = '2023-01-01'
    determine_icd_code.return_value = 'A00'

    # Call the function to test
    result = process_pdf_files('/fake/path')

    # Assert that the result contains the expected number of records
    assert len(result) == 2
    # Assert that all records have the expected ICD code
    assert all(record['icd_code'] == 'A00' for record in result)
    # Assert that all records contain a reference field
    assert all('reference' in record for record in result)

def test_sort_records():
    """
    Test the sort_records function to ensure it sorts records by date in descending order.

    This test provides a list of records with different dates and verifies that the
    sort_records function returns the records sorted by date in descending order.
    """
    records = [
        {'date': '2023-02-01'},
        {'date': '2023-01-01'},
        {'date': '2023-03-01'}
    ]
    # Call the function to test
    sorted_records = sort_records(records)
    # Assert that the records are sorted by date in descending order
    assert [record['date'] for record in sorted_records] == ['2023-03-01', '2023-02-01', '2023-01-01']

def test_main(mock_dependencies, tmp_path):
    """
    Test the main function to ensure it processes input files and creates the output PDF.

    This test creates temporary input and output directories, runs the main function,
    and verifies that the output PDF file is created and is not empty.
    """
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"
    input_folder.mkdir()
    output_folder.mkdir()

    # Run main with two arguments
    main(str(input_folder), str(output_folder))

    # Check that the file was created
    output_file = os.path.join(output_folder, "summary_of_injuries.pdf")
    assert os.path.exists(output_file)

    # Check that the file is not empty
    assert os.path.getsize(output_file) > 0
    # Additional checks can be added here

