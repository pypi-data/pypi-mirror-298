"""
Setup Configuration for Injury Summary Generator

This setup script is used for packaging and distributing the Injury Summary Generator project.
"""

from setuptools import setup, find_packages

setup(
    name="injury-summary-generator",
    version="1.0.0",
    author="Eduard Izgorodin",
    author_email="edizgorodin@gmail.com",
    description="Automates the creation of demand letters based on medical PDF records.",
    long_description=open('README.md').read(),
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
            'generate-injury-summary=generate_summary_of_injuries:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


