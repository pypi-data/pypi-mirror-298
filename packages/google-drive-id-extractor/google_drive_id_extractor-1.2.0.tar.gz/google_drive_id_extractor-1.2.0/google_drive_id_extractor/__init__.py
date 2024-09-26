import re


def extract_google_drive_id(drive_link):
    patterns = [
        r"/d/([a-zA-Z0-9_-]{25,})",
        r"id=([a-zA-Z0-9_-]{25,})",
        r"/file/d/([a-zA-Z0-9_-]{25,})",
    ]

    for pattern in patterns:
        match = re.search(pattern, drive_link)
        if match:
            return match.group(1)

    return None
