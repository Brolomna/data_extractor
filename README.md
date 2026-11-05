# JSON Data Extractor

A small Python command-line tool that reads a JSON file, finds nested records containing four selected fields, and writes them to a clean text report.

This project began as a utility for extracting selected fields from JSON data encountered during authorized web-application testing. It now uses Python's built-in JSON parser instead of regular expressions, so values stay associated with the correct record.

## Features

- Reads valid JSON objects and arrays, including nested structures.
- Extracts records containing all four required fields: `nickname`, `user_id`, `nationality`, and `head_url`.
- Keeps fields together within their original JSON object.
- Writes a readable report and replaces an existing output file to avoid accidental duplicate entries.
- Reports missing files and malformed JSON with useful error messages.
- Uses only the Python standard library; no third-party packages are required.

## Requirements

- Python 3.9 or newer

## Usage

Run the script with an input JSON file and an output text file:

```bash
python details_extractor.py input.json report.txt
```

Example input:

```json
{
  "list": [
    {
      "nickname": "Alex",
      "user_id": 12345,
      "nationality": "US",
      "head_url": "alex.png",
      "is_banned_comment": false
    },
    {
      "nickname": "Sam",
      "user_id": 67890,
      "nationality": "GB",
      "head_url": "sam.png"
    }
  ]
}
```

Example output:

```text
Nickname: Alex
User ID: 12345
Nationality: US
Head URL: alex.png
----------------------------------------
Nickname: Sam
User ID: 67890
Nationality: GB
Head URL: sam.png
----------------------------------------
```

Objects that do not contain all four required fields are skipped. If no complete records are found, the tool creates an empty report and prints a message.

## Run the tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests cover nested records, incomplete objects, output formatting, output-file replacement, and protection against using the same input and output path.

## Limitations

- The tool expects valid JSON; it does not parse arbitrary text or malformed JSON.
- It extracts only the four fields listed above.
- The output is a plain-text report, not JSON or CSV.

## Responsible use

Use this tool only with data you own or are authorized to access and process. Avoid collecting, sharing, or retaining personal data without permission.
