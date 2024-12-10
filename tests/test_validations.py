import pytest
import os
import yaml

from utils.data_extractor import extract_from_csv, extract_data_from_pdf
from utils.validators import (
    check_presence,
    check_data_type,
    check_length,
    check_lookup,
    check_exact_value, check_exact_pdf)


@pytest.fixture
def load_config():
    """ Fixture to load the configuration from config.yaml """
    with open('config/config.yaml', 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture
def sample_data():
    """Fixture to load sample data from the first CSV file found in the specified directory"""
    directory = 'data/reports/'
    csv_file_path = None

    for file in os.listdir(directory):
        if file.endswith('.csv'):
            csv_file_path = os.path.abspath(os.path.join(directory, file))
            break  # Stop after the first CSV file is found

    if not csv_file_path:
        raise FileNotFoundError("No CSV file found in the specified directory.")

    return extract_from_csv(csv_file_path)

@pytest.fixture
def pdf_data():
    """ Fixture to load the first PDF file found in the reports directory """
    directory = 'data/reports/'
    pdf_file_path = None

    for file in os.listdir(directory):
        if file.endswith('.pdf'):
            pdf_file_path = os.path.abspath(os.path.join(directory, file))
            break  # Stop after the first PDF file is found

    if not pdf_file_path:
        raise FileNotFoundError("No PDF file found in the specified directory.")

    return extract_data_from_pdf(pdf_file_path)


# Test for check_presence
def test_check_presence(sample_data, load_config):
    required_fields = load_config['validations']['required_fields']

    errors = check_presence(sample_data, required_fields)

    if errors:
        print(f"\nValidation errors for presence check: {errors}")
    else:
        print("\nAll required fields are present and not empty.")

    assert len(errors) == 0

#Tests for data type
def test_check_data_type(sample_data, load_config):
    formats =  load_config['validations']['formats']
    errors = check_data_type(sample_data, formats)
    assert len(errors) == 0

# Test for check_length
def test_check_length(sample_data, load_config):
    length_constraints = load_config['validations']['length_constraints']
    errors = check_length(sample_data, length_constraints)

    if errors:
        print(f"\nValidation errors for lengt: {errors}")
    else:
        print("\nAll fields have correct lenght.")

    assert len(errors) == 0

# Test for check_lookup
def test_check_lookup(sample_data, load_config):
    lookups = load_config['lookups']
    errors = check_lookup (sample_data, lookups)

    if errors:
        print(f"\nValidation errors for lookups: {errors}")
    else:
        print("\nAll lookups fields have correct value.")

    assert len(errors) == 0

# Test for check_exact_value
def test_check_exact_value(sample_data):
    filepath = "data/expected/etalon_file.csv"
    errors = check_exact_value(sample_data, filepath)

    if errors:
        print(f"\nValidation errors for check_exact_value: {errors}")
    else:
        print("\nExact validation passed.")

    assert len(errors) == 0

# Test for check_exact_value
def test_check_exact_pdf(pdf_data):
    filepath = "data/expected/etalon_file.pdf"
    errors = check_exact_pdf(pdf_data, filepath)

    if errors:
        print(f"\nPDF Validation errors for check_exact_pdf_value: {errors}")
    else:
        print("\nExact PDF validation passed.")

    assert len(errors) == 0