# google-drive-id-extractor

**google-drive-id-extractor** is a simple Python package that allows users to easily extract the Google Drive ID from any Google Drive file URL. This package uses regular expressions to find and extract the file ID from various formats of Google Drive links.

## Features

- Extract Google Drive file ID from multiple link formats
- Lightweight and simple to use
- Works with various types of Google Drive links, such as shareable links and embedded links

## Installation

To install the **google-drive-id-extractor** package, use the following command:

```bash
pip install google-drive-id-extractor
```

## Usage

After installing the package, you can start using it by importing the `extract_google_drive_id` function. Here's a simple example of how to extract a Google Drive file ID from a link:

```python
from google_drive_id_extractor import extract_google_drive_id

# Example Google Drive URL
drive_link = "https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view?usp=sharing"

# Extract the Google Drive file ID
file_id = extract_google_drive_id(drive_link)

# Output the result
print(f"The Google Drive ID is: {file_id}")
```

This will extract the file ID from a Google Drive link and print it. The function handles different link formats, including:

- `https://drive.google.com/file/d/[fileID]/view?usp=sharing`
- `https://drive.google.com/open?id=[fileID]`
- `https://drive.google.com/uc?id=[fileID]`

### Supported Link Formats

The package is capable of extracting the Google Drive file ID from the following types of URLs:

1. Direct file URLs:  
   Example:  
   `https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view?usp=sharing`

2. Embedded URLs:  
   Example:  
   `https://drive.google.com/embeddedfolderview?id=1A2B3C4D5E6F7G8H9I0J`

3. Open links with the file ID as a parameter:  
   Example:  
   `https://drive.google.com/open?id=1A2B3C4D5E6F7G8H9I0J`

## Function

### `extract_google_drive_id(drive_link)`

- **Description**: This function extracts and returns the Google Drive file ID from a provided Google Drive URL.
- **Parameters**:
  - `drive_link` (str): The Google Drive URL from which to extract the file ID.
- **Returns**:
  - `str`: The extracted Google Drive file ID, or `None` if no valid ID is found.

## Example

```python
# Example with different formats
links = [
    "https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view?usp=sharing",
    "https://drive.google.com/open?id=1A2B3C4D5E6F7G8H9I0J",
    "https://drive.google.com/embeddedfolderview?id=1A2B3C4D5E6F7G8H9I0J"
]

for link in links:
    file_id = extract_google_drive_id(link)
    print(f"Extracted File ID: {file_id}")
```

## License

This package is licensed under the MIT License.

## About

This package is provided by [ToolsForFree.com](https://toolsforfree.com/). ToolsForFree.com provides a variety of helpful utilities to make working with Google Drive and other services more convenient.

If you're looking to convert Google Drive shareable links into direct download links, be sure to check out our [Google Drive Direct Link Generator](https://toolsforfree.com/google-drive-direct-link-generator).

---

### Author

- ToolsForFree.com
