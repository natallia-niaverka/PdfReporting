import os

import pandas as pd
import pdfplumber


def extract_data_from_pdf(file_path):
    """
    Extracts text data from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text = page.extract_text()
    return text


def extract_from_csv(file_path):
    """
    Extracts data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries containing the data rows.
    """
    df = pd.read_csv(file_path)

    content = df.to_dict(orient='records')

    return content

def get_csv_files(directory):
    """
    Returns a list of CSV file paths in the given directory.

    Args:
        directory (str): The directory to search for CSV files.

    Returns:
        list: A list of paths to the found CSV files.
    """
    csv_files = []
    for file in os.listdir(directory):
        if file.endswith('.csv'):
            csv_files.append(os.path.join(directory, file))
    return csv_files

def get_pdf_files(directory):
    """
    Returns a list of PDF file paths in the given directory.

    Args:
        directory (str): The directory to search for PDF files.

    Returns:
        list: A list of paths to the found PDF files.
    """
    pdf_files = []
    for file in os.listdir(directory):
        if file.endswith('.pdf'):
            pdf_files.append(os.path.join(directory, file))
    return pdf_files