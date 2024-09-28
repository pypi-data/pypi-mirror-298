# Injury Summary Generator

This project automates the process of creating a demand letter for a client based on medical records in PDF format. It extracts relevant information from medical records and generates a "Summary of Injuries" section in a table format.

## Data Source

The ICD-10 codes used in this project are sourced from the Centers for Medicare & Medicaid Services (CMS) website. You can find the official ICD-10 code lists at:

https://www.cms.gov/medicare/coordination-benefits-recovery/overview/icd-code-lists

This authoritative source ensures that our project uses up-to-date and accurate ICD-10 codes for classifying diagnoses.

## Features

- **PDF Processing**: Reads multiple PDF files containing medical records and extracts text.
- **Information Extraction**: Extracts key information such as visit dates, diagnoses, and page numbers.
- **ICD-10 Code Determination**: Determines appropriate ICD-10 codes for extracted diagnoses.
- **PDF Generation**: Creates a summary PDF with a formatted table of extracted information.

## Installation

You can install the Injury Summary Generator using pip:
```bash
pip install injury-summary-generator
```

## Usage

After installation, you can run the Injury Summary Generator using the following command:

```bash
injury-summary-generator <input_folder> <output_folder>
```

Where:
- `<input_folder>` is the path to the folder containing the medical record PDF files.
- `<output_folder>` is the path where the output summary PDF will be saved.

To check the version of the installed package, use:

```bash
injury-summary-generator --version
```

## Project Structure

- `generate_summary_of_injuries/`: Main package directory.
  - `__init__.py`: Package initialization file.
  - `_metadata.py`: Package metadata.
  - `main.py`: Entry point for the command-line interface.
  - `processor.py`: Main processing logic.
  - `pdf_reader.py`: Handles reading PDF files and extracting text.
  - `date_extractor.py`: Extracts dates from text.
  - `diagnosis_extractor.py`: Extracts diagnoses from text.
  - `icd_code_determiner.py`: Determines ICD-10 codes based on diagnoses.
  - `pdf_creator.py`: Creates the final summary PDF.
  - `data/`: Contains data files used by the project.
    - `icd10_codes.csv`: CSV file containing ICD-10 codes and descriptions.
- `tests/`: Contains unit tests for the project.
- `setup.py` and `setup.cfg`: Configuration files for packaging and distribution.
- `requirements.in` and `requirements.txt`: Lists Python dependencies for the project.
- `MANIFEST.in`: Specifies additional files to include in the package.
- `README.md`: Provides information about the project and how to use it.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Development

To set up the development environment:

1. Clone the repository: `git clone https://github.com/yourusername/injury-summary-generator.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Install the package in editable mode: `pip install -e .`

## Testing

To run the tests, use the following command:

```bash
pytest
```

## Contributing

Contributions to this project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

## Releasing

To create a new release:

1. Update the version number in `setup.py`.
2. Create a new tag with the version number: `git tag v1.0.0`
3. Push the tag to GitHub: `git push origin v1.0.0`
4. Create a new release on GitHub, describing the changes and new features.
5. Build and upload the package to PyPI:
   ```
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.