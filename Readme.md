# DataExtraction Class Documentation

## Overview

The `DataExtraction` class is designed to extract data from invoice PDF files, process the data into structured formats, and export the results into Excel and CSV files.

## Features

- Extracts data from invoice PDFs using `tabula` and `PyPDF2`.
- Processes invoice details like total amount and invoice date.
- Outputs data as Pandas DataFrames.
- Exports results to Excel and CSV formats.

## Requirements

Make sure the following Python libraries are installed:

- `distro==1.9.0`
- `et_xmlfile==2.0.0`
- `numpy==2.2.1`
- `openpyxl==3.1.5`
- `pandas==2.2.3`
- `pip==24.3.1`
- `PyPDF2==3.0.1`
- `python-dateutil==2.9.0`
- `pytz==2024.2`
- `setuptools==63.2.0`
- `six==1.17.0`
- `tabula==1.0.5`
- `tabula-py==2.10.0`
- `tabulate==0.9.0`
- `tzdata==2024.2`
You can install above libraries using pip:

```bash
pip install -r requirements.txt
```

## Class Methods

### Constructor

```python
__init__(**kwargs)
```

- **Parameters:**
  - `invoice_pdf1`: Path to the first invoice PDF file.
  - `invoice_pdf2`: Path to the second invoice PDF file.
- **Description:** Initializes the class with PDF file paths.

### get_connection_str(path, file_name)

- **Parameters:**
  - `path`: Absolute path of the invoice PDF.
  - `file_name`: Name of the invoice PDF.
- **Description:** Reads the PDF file using `tabula` (for structured PDFs) or `PyPDF2` (for text extraction).
- **Returns:** List of DataFrames or a `PdfReader` object.

### get_filename(invoice_file_name)

- **Parameters:**
  - `invoice_file_name`: Path to the PDF file.
- **Description:** Extracts the file name without the extension.
- **Returns:** File name as a string.

### get_absfile_path(invoice_file_name)

- **Parameters:**
  - `invoice_file_name`: Path to the PDF file.
- **Description:** Returns the absolute path of the file.
- **Returns:** Absolute file path as a string.

### convert_date(format_type, date_time)

- **Parameters:**
  - `format_type`: Either 'German' or 'No'.
  - `date_time`: Date string to be formatted.
- **Description:** Converts date formats into `dd-MMMM-yyyy`.
- **Returns:** Formatted date string.

### format_invoice2(abs_filePath, abs_fileName)

- **Parameters:**
  - `abs_filePath`: Absolute path of the invoice file.
  - `abs_fileName`: invoice File name.
- **Description:** Extracts `Total USD` and `Invoice Date` from PDF2 and returns a DataFrame.
- **Returns:** Pandas DataFrame with `File Name`, `Date`, and `Value`.

### get_data()

- **Description:** Extracts data from both invoice PDFs, merges them into a single DataFrame, and saves results to Excel and CSV files.
- **Returns:** Merged DataFrame with `File Name`, `Date`, and `Value`.

## Usage Example

```python
if __name__ == '__main__':
    invoice_file_name1 = "sample_invoice_1.pdf"
    invoice_file_name2 = "sample_invoice_2.pdf"
    extract_data = DataExtraction(invoice_pdf1=invoice_file_name1, invoice_pdf2=invoice_file_name2)
    extract_data.get_data()
```

## Outputs

- **Excel File:** `invoice_excel.xlsx`
  - Sheet 1: Raw data from both PDFs.
  - Sheet 2: Pivot table summarizing the data.
- **CSV File:** `Total.csv` (semicolon-separated).

## Notes

- Ensure PDFs are formatted consistently.
- Verify locale settings (`deu`) for proper date parsing.

## Author

**P Mahesh Kumar**
