
from typing import List, Dict
import logging
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
    # Use portrait orientation with letter page size
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    body_style = styles['BodyText']

    # Add a title
    title = Paragraph("Summary of Injuries", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add space after title

    # Define the table data with header
    data = [['Date of Visit', 'Diagnosis', 'ICD Code', 'Reference']]
    for record in records:
        data.append([
            record['date'],
            Paragraph(record['diagnosis'], body_style),
            record['icd_code'],
            Paragraph(record['reference'], body_style)
        ])

    # Create the table
    table = Table(data, repeatRows=1)

    # Adjust table style for a professional look
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),                 # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),             # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),        # Body background
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('WORDWRAP', (0, 0), (-1, -1), True)
    ])

    # Apply alternating row colors
    for i in range(1, len(data)):
        if i % 2 == 0:
            bg_color = colors.lightgrey
            style.add('BACKGROUND', (0, i), (-1, i), bg_color)

    table.setStyle(style)

    # Set column widths
    table_width = 540  # Total table width in points
    column_widths = [
        table_width * 0.15,  # Date of Visit
        table_width * 0.45,  # Diagnosis
        table_width * 0.15,  # ICD Code
        table_width * 0.25   # Reference
    ]
    table._argW = column_widths

    # Add the table to the elements
    elements.append(table)

    # Generate the PDF
    doc.build(elements)

    logging.info(f"Created PDF: {output_file}")

# Additional helper functions for PDF creation can be added here if needed
