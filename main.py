from utils.data_extractor import extract_data_from_pdf, get_csv_files, get_pdf_files
from utils.data_extractor import extract_from_csv
from jinja2 import Environment, FileSystemLoader
from utils.validators import (
    check_presence,
    check_data_type,
    check_length,
    check_lookup,
    check_exact_value, check_exact_pdf
)
import yaml


def load_config(config_path):
    """
    Load the configuration file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        dict: The parsed configuration data.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def generate_html_report(summary_results, output_path):
    """Generate an HTML report using Jinja2."""
    env = Environment(loader=FileSystemLoader('outputs/template'))
    template = env.get_template('report_template.html')

    report_data = []

    for result in summary_results:
        presence_errors = result['errors'].get('presence_errors', [])
        format_errors = result['errors'].get('format_errors', [])
        length_errors = result['errors'].get('length_errors', [])
        lookup_errors = result['errors'].get('lookup_errors', [])
        exact_value_errors = result['errors'].get('exact_value_errors', [])
        pdf_errors = result['errors'].get('pdf_errors', [])

        report_entry = {
            'file': result['file'],
            'presence_errors': presence_errors,
            'format_errors': format_errors,
            'length_errors': length_errors,
            'lookup_errors': lookup_errors,
            'exact_value_errors': exact_value_errors,
            'pdf_errors': pdf_errors,
            'presence_status': "PASSED" if not presence_errors else "FAILED",
            'format_status': "PASSED" if not format_errors else "FAILED",
            'length_status': "PASSED" if not length_errors else "FAILED",
            'lookup_status': "PASSED" if not lookup_errors else "FAILED",
            'exact_value_status': "PASSED" if not exact_value_errors else "FAILED",
            'pdf_status': "PASSED" if not pdf_errors else "FAILED",
            'presence_class': 'passed' if not presence_errors else 'failed',
            'format_class': 'passed' if not format_errors else 'failed',
            'length_class': 'passed' if not length_errors else 'failed',
            'lookup_class': 'passed' if not lookup_errors else 'failed',
            'exact_value_class': 'passed' if not exact_value_errors else 'failed',
            'pdf_class': 'passed' if not pdf_errors else 'failed',
        }

        report_data.append(report_entry)

    with open(output_path, 'w') as output_file:
        output_file.write(template.render(results=report_data))

def main():
    # Load configuration
    config_path = 'config/config.yaml'  # Path to your config file
    config = load_config(config_path)

    # Extract data from the config
    required_fields = config['validations']['required_fields']
    formats = config['validations']['formats']
    length_constraints = config['validations']['length_constraints']
    lookups = config['lookups']

    # To store final validation results for reporting
    summary_results = []

    # To store list of errors for each validation
    validation_results = {
        'presence_errors': [],
        'format_errors': [],
        'length_errors': [],
        'lookup_errors': [],
        'exact_value_errors': [],
        'pdf_errors': []
    }

    # Get CSV, PDF files from the reports directory
    reports_directory = 'data/reports/'
    print("Report directory: ", reports_directory)
    csv_files = get_csv_files(reports_directory)
    pdf_files = get_pdf_files(reports_directory)
    print(f"Files are found: ")
    print(f"CSV Files: {', '.join(csv_files)}")
    print(f"PDF Files: {', '.join(pdf_files)}")

    # Process PDF files
    for pdf_file in pdf_files:
        print(f"Processing PDF file: {pdf_file}")
        try:
            sample_data_pdf = extract_data_from_pdf(pdf_file)

            # Validate exact values in the expected PDF
            print("Pdf content Validation...")
            expected_pdf_path = 'data/expected/etalon_file.pdf'
            pdf_errors = check_exact_pdf(sample_data_pdf, expected_pdf_path)
            # Reporting results
            if pdf_errors:
                print("PDF Validation Errors:")
                for error in pdf_errors:
                    validation_results['pdf_errors'] += pdf_errors
                    print(f" - {error}")
            else:
                print("PDF Validation: All validations passed successfully")

        except Exception as e:
            print("An error occurred:", e)

    # Process CSV files
    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")

        try:
            # Extract content from the CSV file
            extracted_content = extract_from_csv(csv_file)
            print("CSV has been read successfully")

            # Validate presence of required fields
            print("Validation that all required fields...")
            presence_errors = check_presence(extracted_content, required_fields)
            validation_results['presence_errors'] += presence_errors

            if presence_errors:
                for error in presence_errors:
                    print("Presence Validation:", error)
            else:
                print("Presence Validation: All required fields are present.")

            # Validate data types based on formats
            print("Validation formats...")
            type_errors = check_data_type(extracted_content, formats)
            validation_results['format_errors'] += type_errors

            if type_errors:
                for error in type_errors:
                    print("Format Validation: Data Type Error:", error)
            else:
                print("Format Validation:All data types are valid.")

            # Validate string lengths based on constraints
            print("Length Validation...")
            length_errors = check_length(extracted_content, length_constraints)
            validation_results['length_errors'] += length_errors

            if length_errors:
                for error in length_errors:
                    print("Length Validation Error:", error)
            else:
                print("Length Validation: All string lengths are within specified limits.")

            # Validate lookups
            print("Lookup Validation...")
            lookup_errors = check_lookup(extracted_content, lookups)
            validation_results['lookup_errors'] += lookup_errors

            if lookup_errors:
                for error in lookup_errors:
                    print("Lookup Validation Error:", error)
            else:
                print("Lookup Validation: All lookup values are valid.")

            # Validate exact values
                print("Exact Value Validation...")
                exact_value_errors = check_exact_value(extracted_content, "data/expected/etalon_file.csv")
                validation_results['exact_value_errors'] += exact_value_errors
                if exact_value_errors:
                    for error in exact_value_errors:
                        print("Exact Value Validation Error:", error)
                else:
                    print("Exact Value Validation:All values match the expected values.")

            # Store results for reporting
            print("Report creation...")
            summary_results.append({'file': csv_file, 'errors': validation_results})
            # Generate HTML report
            print("Html report generating...")
            output_file_path = 'outputs/validation_report.html'  # Ensure this directory exists
            generate_html_report(summary_results, output_file_path)

            print(f"Results written to {output_file_path}")

        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    main()
