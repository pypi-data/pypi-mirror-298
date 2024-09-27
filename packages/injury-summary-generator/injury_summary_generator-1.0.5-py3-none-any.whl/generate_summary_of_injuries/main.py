"""
This module is responsible for generating a summary of injuries from PDF medical records.
It processes PDF files, extracts relevant information, and creates a summary PDF report.
"""
import sys
import logging
from generate_summary_of_injuries._metadata import __version__
from generate_summary_of_injuries.processor import generate_summary

# Configure logging to display informational messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    if len(sys.argv) != 3:
        print(f"Usage: injury-summary-generator <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    print(f"Injury Summary Generator v{__version__}")
    print(f"Processing files from {input_folder} and saving summaries to {output_folder}")

    generate_summary(input_folder, output_folder)

if __name__ == "__main__":
    main()