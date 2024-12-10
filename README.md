# Report Validation Framework

This project is a data validation framework designed to process and validate reports generated in CSV and PDF.
It includes static validation of the pdf against etalon value and validations of csv file 
Presence Validation
Format Validation
Length Validation
Lookup Validation
Exact Value Validation.


## Table of Contents
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Report Generation](#report-generation)
- [Running Tests](#running-tests)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)

## Technologies
- python
- pytest
- PyYAML
- pdfplumber
- pandas
- Jinja2

## Prerequisites

Before running the application or tests, ensure you have the following installed:

- Python 3.6 or later
- Pip
- Virtual environment tools

*Note: All pakages dependencies are stored in requirements.txt


## Installation
- Clone or extract the directory
- Set up a virtual environment
- Install required packages with "pip install -r requirements.txt" command
- Install additionally packages with "pip install pandas PyYAML Jinja2 pdfplumber pytest pytest-html"

*Note: on your machine it could be "pip3" instead of "pip".

## Running the Application
- Reports under the test are supposed to be placed at "data/reports" directory
- Run the application with the "python main.py" command
- The html report will be saved in "outputs" directory

By running the application assumed start the validation process including reading configuration, reading data from files, validation against the rules and generating report with the results.

## Report Generation

After running the application, an HTML report of the results will be generated using Jinja2. 
Location of the Report: The report will be saved at outputs/

What to Expect in the Report:
The report will include sections for:
- Presence Validation
- Format Validation
- Length Validation
- Lookup Validation
- Exact Value Validation
- Pdf validation

For each validation type, the status will be shown "PASSED" or "FAILED" will be displayed beside the validation type.
If there are errors, they will be listed below the status in a clear format.


## Running Tests
- Tests separately could be run with command "pytest -v tests/test_validations.py"


## Directory Structure
├── README.md                 # Documentation
├── config/
│   ├── config.yaml           # Configuration file for validation rules and lookups
├── data/
│   ├── reports/              # Directory for input files (PDF/CSV)
│   ├── expected/             # Directory for etalon values for exact validation
├── outputs/                  # Directory for validation report outputs
│   ├── template/             # Directory for validation report template
├── tests/
│   ├── test_validations.py    # Contains Pytest test cases
├── utils/
│   ├── data_extractor.py     # Functions for reading and extracting data from files
│   ├── validators.py          # Validation functions
└── main.py                   # Main script to orchestrate the validation process

## Contributing

for all contribution contact natallia.niaverka@gmail.com
