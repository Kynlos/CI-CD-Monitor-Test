# API Documentation

*Last updated: 1763155247.344252*

API Documentation
================

## Overview of Changes

The `generate-docs.py` script has been updated to generate comprehensive API documentation for changed code files. The script reads the changed files, sends them to the Groq API for documentation generation, and saves the generated documentation as a Markdown file.

## Functions and Classes

### `build_file_context(files_data)`

*   **Description:** Builds a file context with the full code of the changed files.
*   **Parameters:**
    *   `files_data` (dict): A dictionary containing the file paths and their corresponding contents.
*   **Returns:** A string representing the file context.

### `generate_documentation(file_context, file_list)`

*   **Description:** Calls the Groq API to generate documentation for the given file context and list of changed files.
*   **Parameters:**
    *   `file_context` (str): The file context built by the `build_file_context` function.
    *   `file_list` (list): A list of changed file paths.
*   **Returns:** A string representing the generated documentation.

### `calculate_tokens(file_context)`

*   **Description:** Calculates the token count and cost for the given file context.
*   **Parameters:**
    *   `file_context` (str): The file context built by the `build_file_context` function.
*   **Returns:** A dictionary containing the token count and cost.

### `main()`

*   **Description:** The main entry point of the script. It reads the changed files, generates documentation, and saves it as a Markdown file.
*   **Parameters:** None
*   **Returns:** None

## Usage Examples for Exports

The `generate-docs.py` script can be used to generate documentation for changed code files. Here's an example usage:

1.  Create a `changed_files.txt` file containing the paths of the changed files, one file per line.
2.  Run the `generate-docs.py` script using Python: `python generate-docs.py`
3.  The script will generate documentation for the changed files and save it as a Markdown file named `doc_output.md`.

## Parameter Descriptions

The `generate-docs.py` script uses the following parameters:

*   `GROQ_API_KEY`: The API key for the Groq API.
*   `GROQ_API_URL`: The URL of the Groq API.
*   `MODEL`: The model used for documentation generation.

## Return Value Documentation

The `generate_documentation` function returns a string representing the generated documentation. The documentation includes an overview of changes, all functions and classes, usage examples for exports, parameter descriptions, and return value documentation.

### Token Usage

The `calculate_tokens` function calculates the token count and cost for the given file context. The token count is calculated by dividing the length of the file context by 4, and the cost is calculated by multiplying the token count by the Groq pricing (0.075 per 1 million tokens).

### API Documentation File

The generated documentation is saved as a Markdown file named `API-DOCS.md`. This file contains the API documentation for the changed code files.

### PR Comment

The generated documentation is also saved as a Markdown file named `doc_output.md`, which can be used as a PR comment. The file contains the API documentation for the changed code files, along with the token usage and cost.

Commit Message
--------------

The commit message for the updated `generate-docs.py` script should include a brief description of the changes made, such as:

```
Update generate-docs.py to generate comprehensive API documentation

* Added support for generating documentation for changed code files
* Updated the script to use the Groq API for documentation generation
* Added token usage and cost calculation
```