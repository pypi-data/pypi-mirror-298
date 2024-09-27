import os
import tempfile
from generate_summary_of_injuries.pdf_creator import create_summary_pdf

def test_create_summary_pdf():
    records = [
        {'date': '2023-01-01', 'diagnosis': 'Fracture', 'icd_code': 'S42', 'reference': 'Doc1 - p. 1'},
        {'date': '2023-02-01', 'diagnosis': 'Sprain', 'icd_code': 'S43', 'reference': 'Doc2 - p. 2'}
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, 'test_summary.pdf')
        create_summary_pdf(records, output_file)

        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0