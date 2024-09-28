"""
This module is responsible for creating a summary PDF report of injuries.
It uses the ReportLab library to generate a professional-looking PDF document
containing a table with injury records, including visit dates, diagnoses, ICD codes,
and references.
"""

from typing import List, Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

def create_summary_pdf(records: List[Dict], output_file: str):
    """
    Create a summary PDF of injury records.

    Args:
    records (List[Dict]): List of dictionaries containing injury record data.
    output_file (str): Path to save the output PDF file.
    """
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    body_style = styles['BodyText']

    # Add title
    title = Paragraph("Summary of Injuries", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Prepare table data
    data = [['Date of Visit', 'Diagnosis', 'ICD Code', 'Reference']]
    for record in records:
        data.append([
            record['date'],
            Paragraph(record['diagnosis'], body_style),
            record['icd_code'],
            Paragraph(record['reference'], body_style)
        ])

    # Create and style the table
    table = Table(data, repeatRows=1)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),                 # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),             # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('WORDWRAP', (0, 0), (-1, -1), True)
    ])

    # Apply alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)

    table.setStyle(style)

    # Set column widths
    table_width = 540
    column_widths = [
        table_width * 0.15,  # Date of Visit
        table_width * 0.45,  # Diagnosis
        table_width * 0.15,  # ICD Code
        table_width * 0.25   # Reference
    ]
    table._argW = column_widths

    elements.append(table)

    # Generate the PDF
    doc.build(elements)
