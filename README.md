# JSON Data Extractor

A small Python command-line utility that searches nested JSON data for records containing four selected fields and exports them as a readable text, CSV, or JSON report.

This project began as a utility for extracting selected fields from JSON data encountered during authorized web-application testing. It uses Python's built-in JSON parser rather than regular expressions, keeping values associated with their original record.

## Features

- Recursively finds matching objects inside nested JSON dictionaries and lists.
- Extracts `nickname`, `user_id`, `nationality`, and `head_url`.
- Preserves the relationship between fields in each matching object.
- Exports to plain text, CSV, or JSON.
- Handles missing files, malformed JSON, and unsafe input/output path reuse with clear errors.
- Uses only the Python standard library.

## Requirements

- Python 3.9 or newer

## Usage

The default output is a plain-text report:

```bash
python details_extractor.py input.json report.txt
```

Choose CSV or JSON when you need structured output:

```bash
python details_extractor.py input.json report.csv --format csv
python details_extractor.py input.json report.json --format json
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

Objects without all four required fields are skipped. If no complete records are found, an empty report (or a CSV containing only its header) is written.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers nested extraction, incomplete records, text/CSV/JSON output, and input/output path protection. GitHub Actions runs the tests on Python 3.9 through 3.13 for pushes and pull requests.

## Limitations

- Input must be valid JSON; arbitrary text and malformed JSON are not supported.
- Only the four fields listed above are extracted.
- The utility does not make network requests or fetch the URLs found in the data.
- It does not validate whether the extracted values are accurate or safe to use.

## Responsible use

Use this tool only with data you own or are authorized to access and process. Avoid collecting, sharing, or retaining personal data without permission.
