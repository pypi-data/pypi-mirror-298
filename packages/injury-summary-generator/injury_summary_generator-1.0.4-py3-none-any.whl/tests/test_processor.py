import os
import pytest
from generate_summary_of_injuries.processor import process_pdf_files, sort_records, generate_summary

@pytest.fixture
def mock_dependencies(mocker):
    mocker.patch('generate_summary_of_injuries.processor.read_pdf_files')
    mocker.patch('generate_summary_of_injuries.processor.extract_text_from_pdf')
    mocker.patch('generate_summary_of_injuries.processor.extract_diagnosis')
    mocker.patch('generate_summary_of_injuries.processor.extract_date')
    mocker.patch('generate_summary_of_injuries.processor.determine_icd_code')
    mocker.patch('generate_summary_of_injuries.processor.create_summary_pdf')

def test_process_pdf_files(mock_dependencies):
    from generate_summary_of_injuries.processor import read_pdf_files, extract_text_from_pdf, extract_diagnosis, extract_date, determine_icd_code
    
    read_pdf_files.return_value = ['file1.pdf', 'file2.pdf']
    extract_text_from_pdf.return_value = 'Sample text'
    extract_diagnosis.return_value = 'Test'
    extract_date.return_value = '2023-01-01'
    determine_icd_code.return_value = 'A00'

    result = process_pdf_files('/fake/path')
    
    assert len(result) == 2
    assert all(record['icd_code'] == 'A00' for record in result)
    assert all('reference' in record for record in result)

def test_sort_records():
    records = [
        {'date': '2023-02-01'},
        {'date': '2023-01-01'},
        {'date': '2023-03-01'}
    ]
    sorted_records = sort_records(records)
    assert [record['date'] for record in sorted_records] == ['2023-03-01', '2023-02-01', '2023-01-01']

def test_generate_summary(mock_dependencies, tmp_path):
    from generate_summary_of_injuries.processor import create_summary_pdf
    
    input_folder = tmp_path / "input"
    output_folder = tmp_path / "output"
    input_folder.mkdir()
    output_folder.mkdir()

    generate_summary(str(input_folder), str(output_folder))

    output_file = os.path.join(output_folder, "summary_of_injuries.pdf")
    create_summary_pdf.assert_called_once()
    args, _ = create_summary_pdf.call_args
    assert args[1] == output_file  # Check if the output file path is correct