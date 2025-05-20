# UUID Replacer for DOCX Files

This tool searches for UUIDs in DOCX files and replaces them with the original names from the anonymization mapping.

## Installation

1. Make sure you have the required dependencies:
   ```bash
   pip install python-docx cryptography
   ```

## Usage

Basic usage:
```bash
python uuid_replacer.py input.docx
```

With custom output file:
```bash
python uuid_replacer.py input.docx -o output.docx
```

With custom file paths:
```bash
python uuid_replacer.py input.docx -m mapping.json -c anonymized.csv -k key.key
```

## Options

- `docx_file`: Path to the DOCX file to process (required)
- `-o, --output`: Output file path (default: input_deanonymized.docx)
- `-m, --mapping`: Path to mapping.json (default: mapping.json)
- `-c, --csv`: Path to anonymized.csv (default: anonymized.csv)
- `-k, --key`: Path to key.key (default: key.key)

## How it works

1. Reads all UUIDs from the anonymized.csv file
2. Loads and decrypts the mapping from mapping.json using the key
3. Creates a mapping from UUIDs to original names
4. Searches and replaces all UUIDs in the DOCX file
5. Saves the result to a new file

## Notes

- The tool will replace UUIDs in both regular paragraphs and tables
- Only UUIDs that appear in both the CSV and mapping files will be replaced
- The original DOCX file is not modified; a new file is created