"""
Initialize the Injury Summary Generator package.

This module imports essential functions and classes used throughout the package,
providing a centralized point of access for the main functionalities.
"""
from .main import main
from .processor import process_pdf_files, sort_records, generate_summary
from ._metadata import __version__

__all__ = ['main', 'process_pdf_files', 'sort_records', 'generate_summary', '__version__']