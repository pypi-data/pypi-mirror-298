"""
Setup Configuration for Injury Summary Generator

This setup script is used for packaging and distributing the Injury Summary Generator project.
"""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        # ... other setup parameters ...
        package_data={
            'generate_summary_of_injuries': ['data/*.csv'],
        },
        include_package_data=True,
        # ... rest of the setup ...
    )