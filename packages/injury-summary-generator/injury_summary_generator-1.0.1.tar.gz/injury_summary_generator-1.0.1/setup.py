"""
Setup Configuration for Injury Summary Generator

This setup script is used for packaging and distributing the Injury Summary Generator project.
"""

from setuptools import setup, find_packages

# Read the contents of README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="injury-summary-generator",
    version="1.0.1",
    author="Eduard Izgorodin",
    author_email="edizgorodin@gmail.com",
    description="Automates the creation of demand letters based on medical PDF records.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/izgorodin/generate_summary_of_injuries",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "reportlab",
        "spacy",
        "nltk",
        "python-dateutil",
        "pytest",
        "pytest-mock",
        "pypdf",
        "dateparser",
        "fuzzywuzzy",
    ],
    entry_points={
        'console_scripts': [
            'injury-summary-generator=generate_summary_of_injuries:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='medical pdf summary injury demand-letter',
    project_urls={
        'Bug Reports': 'https://github.com/izgorodin/generate_summary_of_injuries/issues',
        'Source': 'https://github.com/izgorodin/generate_summary_of_injuries',
    },
)