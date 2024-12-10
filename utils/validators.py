from datetime import datetime

import pandas as pd
import pdfplumber


def check_presence(data, required_fields):
    """
    Validates that required fields are not empty in the dataset.

    Args:
        data (list): A list of dictionaries containing the data rows.
        required_fields (list): A list of required fields that must not be empty.

    Returns:
        dict: A dictionary where keys are field names and values are lists of validation messages.
    """
    errors = []

    for index, row in enumerate(data):
        for field in required_fields:
            if field not in row:
                errors.append(f"Field '{field}' is missing in row {index + 1}.")
            elif row[field] == '':
                errors.append(f"Field '{field}' is empty in row {index + 1}.")

    return errors


def check_data_type(data, formats):
    """
    Validates if fields are of the expected data types.

    Args:
        data (list): A list of dictionaries containing the data rows.
        formats (dict): A dictionary mapping fields to their expected data types.

    Returns:
        list: A list of validation errors, if any.
    """
    errors = []

    for index, row in enumerate(data):
        for field, expected_type in formats.items():
            if field in row:
                if row[field] == '':
                    errors.append(f"Field '{field}' is empty in row {index + 1}.")
                else:
                    if expected_type == 'str':
                        if not isinstance(row[field], str):
                            errors.append(f"Field '{field}' should be of type str in row {index + 1}.")
                    elif expected_type == 'date':
                        try:
                            datetime.strptime(row[field], "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            errors.append(f"Field '{field}' contains wrong format date {row[field]} in row {index + 1}.")

    return errors


def check_length(data, length_constraints):
    """
    Validates if string lengths are within specified limits.

    Args:
        data (list): A list of dictionaries containing the data rows.
        length_constraints (dict): A dictionary mapping fields to their length constraints.

    Returns:
        list: A list of validation errors, if any.
    """
    errors = []

    for index, row in enumerate(data):
        for field, constraints in length_constraints.items():
            if field in row:
                if not isinstance(row[field], str):
                    errors.append(f"Field '{field}' is expected to be a string but got {type(row[field]).__name__} in row {index + 1}.")
                    continue

                field_length = len(row[field])

                if field_length < constraints['min']:
                    errors.append(
                        f"Field '{field}' is too short (min {constraints['min']} characters) in row {index + 1}.")
                elif field_length > constraints['max']:
                    errors.append(
                        f"Field '{field}' is too long (max {constraints['max']} characters) in row {index + 1}.")

    return errors


def check_lookup(data, lookup_dict):
    """
    Validates if specific field values exist in defined lookup tables.

    Args:
        data (list): A list of dictionaries containing the data rows.
        lookup_dict (dict): A dictionary containing lookup fields and their accepted values.

    Returns:
        list: A list of validation errors, if any.
    """
    errors = []

    for index, row in enumerate(data):
        for field, values in lookup_dict.items():
            if field in row:
                if row[field] not in values:
                    errors.append(
                        f"Field '{field}' contains an invalid value '{row[field]}' in row {index + 1}. Expected values: {values}.")

    return errors


def check_exact_value(data, filepath="../data/expected/etalon_file.csv"):
    """
    Checks if specific field values match known expected values.

    Args:
        data (list): A list of dictionaries containing the actual data rows.

    Returns:
        list: A list of validation errors if any discrepancies are found.
    """
    errors = []

    expected_df = pd.read_csv(filepath)
    expected_values = expected_df.to_dict(orient='records')

    for index, row in enumerate(data):
        # Find the corresponding expected value entry by unique identifier (e.g., Barcode)
        expected_row = next((item for item in expected_values if item['Barcode'] == row['Barcode']), None)

        if expected_row:
            for field in expected_row.keys():
                actual_value = row[field]
                expected_value = expected_row[field]

                # Check both actual and expected values for NaN
                if pd.isna(actual_value) and pd.isna(expected_value):
                    continue  # Both are NaN, so consider it a match
                elif actual_value != expected_value:
                    errors.append(
                        f"Field '{field}' does not match expected value in row {index + 1}. Expected '{expected_value}', found '{actual_value}'.")
        else:
            errors.append(f"No expected value found for Barcode '{row['Barcode']}' in row {index + 1}.")

    return errors


def check_exact_pdf(actual_data, expected_file_path="../data/expected/etalon_file.pdf"):
    """
    Checks if the actual string data matches the expected values from a PDF file.

    Args:
        actual_data (str): A string containing the actual data to compare against the PDF.
        expected_file_path (str): The path to the PDF file containing expected values.

    Returns:
        list: A list of validation errors if any discrepancies are found.
    """
    errors = []

    with pdfplumber.open(expected_file_path) as pdf:
        expected_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                expected_text += text + "\n"

    # Split the text into lines
    expected_lines = expected_text.splitlines()

    # Normalize the actual data
    actual_lines = actual_data.splitlines()
    for i, actual_line in enumerate(actual_lines):
        actual_line = actual_line.strip()
        found = False

        for expected_line in expected_lines:
            if actual_line in expected_line:
                found = True
                break

        if not found:
            errors.append(f"Line '{actual_line}' not found in expected data from PDF (line {i + 1}).")

    return errors