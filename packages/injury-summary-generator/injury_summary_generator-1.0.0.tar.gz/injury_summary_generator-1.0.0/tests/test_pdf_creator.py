import os
import tempfile
from src.pdf_creator import create_summary_pdf
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def test_create_summary_pdf():
    records = [
        {'date': '2023-01-01', 'diagnosis': 'Fracture', 'icd_code': 'S42', 'reference': 'Doc1 - p. 1'},
        {'date': '2023-02-01', 'diagnosis': 'Sprain', 'icd_code': 'S43', 'reference': 'Doc2 - p. 2'}
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, 'test_summary.pdf')
        create_summary_pdf(records, output_file)

        # Check if the file was created
        assert os.path.exists(output_file)

        # Check if the file is not empty
        assert os.path.getsize(output_file) > 0

        # You could add more detailed checks here, such as parsing the PDF content
        # to verify the table structure and content, but that would require additional libraries.
