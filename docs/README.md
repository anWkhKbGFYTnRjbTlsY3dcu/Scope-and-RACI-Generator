@"
# Scope and RACI Generator

A Python-based tool to generate project scope forms and RACI matrices as interactive HTML files.

## Features
* **Automated HTML Generation**: Creates clean, styled forms from JSON data.
* **Local Server**: Includes a `serve.py` script to view your forms instantly.
* **Customizable**: Modify `lib/input_fields.json` to change form fields.

## How to Run
1. Double-click `start.bat` (Windows).
2. Or run `python serve.py` in your terminal.
3. Open `http://localhost:8000` in your browser.

## License
This project is licensed under the GNU GPL v3. See the LICENSE file for details.
"@ | Out-File -FilePath README.md -Encoding utf8