import re
from datetime import datetime

def get_date(pages: list[str]) -> str | None:
    """
    Extracts the effective date 

    Expected line format:
        "Effective for Surveys On or After July 1, 2025"

    Args:
        second_page (str): The full text of the second page.

    Returns:
        str | None: Date in ISO format ('YYYY-MM-DD'), or None if not found.
    """
    second_page = pages[1]
    
    # Regex to capture month day, year (e.g. July 1, 2025)
    pattern = re.compile(
        r"Effective for Surveys On or After\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})",
        re.IGNORECASE
    )

    match = pattern.search(second_page)
    if not match:
        return None

    date_str = match.group(1).strip()

    # Try to parse into datetime object
    try:
        parsed_date = datetime.strptime(date_str, "%B %d, %Y")
        # Return ISO format for easy DataFrame usage
        return parsed_date.date().isoformat()
    except ValueError:
        return None

        
def get_year_from_date(date: str) -> str:
    """Return the 4-digit year from an ISO-formatted date string."""
    return date.split("-")[0]


def get_functional_area(pages: list[str]) -> str:
    """
    Extracts the functional area title (e.g., 'Quality Management and Improvement')

    Handles both:
      1. A page containing only the title.
      2. A page with 'Effective for Surveys...' and 'Standards and Guidelines' lines before it.

    Args:
        first_page (str): Full text of the first page.

    Returns:
        str: Clean functional title.

    Raises:
        ValueError: If no functional title is found.
    """
    first_page = pages[0]

    # Split into non-empty lines
    lines = [line.strip() for line in first_page.splitlines() if line.strip()]

    # Remove boilerplate lines
    ignore_patterns = [
        r"Effective for Surveys On or After",
        r"Standards and Guidelines",
        r"HP Standards",
        r"NCQA"
    ]
    filtered = [
        line for line in lines
        if not any(re.search(pat, line, re.IGNORECASE) for pat in ignore_patterns)
    ]

    if not filtered:
        raise ValueError("❌ No functional title found on first page.")

    # Combine the remaining lines
    title = " ".join(filtered).strip()
    title = re.sub(r"\s+", " ", title)

    if not title:
        raise ValueError("❌ Unable to extract functional title text.")

    return title

