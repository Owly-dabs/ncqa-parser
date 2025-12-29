import re


def separate_pages_by_standard(pages: list[str]) -> dict[str, str]:
    """
    Extracts standards from a list of PDF pages, returning a dictionary where
    keys are the standard titles (e.g., 'QI 1: Program Structure and Operations')
    and values are the combined body text across all relevant pages.

    Raises:
        ValueError: If any page does not start with a valid standard header.

    Args:
        pages (list[str]): A list of page texts, such as from read_pdf_pages().

    Returns:
        dict[str, str]: Mapping of standard titles to their body text.
    """
    standards = {}
    current_standard = None

    # Match 2–4 uppercase letters, then number(s), optional sub-IDs, then colon
    standard_pattern = re.compile(r"^[A-Z]{2,4}\s*\d+[A-Z0-9.: -]*:.*")

    for i, text in enumerate(pages, start=1):
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            raise ValueError(f"❌ Page {i} is empty or unreadable.")

        first_line = lines[0]
        match = standard_pattern.match(first_line)

        if not match:
            raise ValueError(f"❌ Page {i} does not start with a valid standard header: '{first_line}'")

        current_standard = match.group(0).strip()
        body_text = "\n".join(lines[4:]).strip() # Body text starts from 4th line onwards

        # Merge if same standard continues over multiple pages
        standards[current_standard] = standards.get(current_standard, "") + "\n" + body_text

    return {k: v.strip() for k, v in standards.items()}

    
def separate_pages_by_standard_v2(pages: list[str]) -> dict[str, str]:
    """
    Groups PDF pages by standards, checking if a new standard begins on each page
    by inspecting line[4]. Collates pages until the next standard is found.

    A valid standard page is detected if lines[4] starts with a standard index pattern
    (e.g., 'QI 1:', 'QI 2.1:', etc.). The standard index and title are extracted from
    lines[0], while the rest of the text (from line[4:] onward) is merged as body text.
    
    There are a few amendable components depending on the structure of the PDF.
    1. Starting page: 0 or 1?
    2. What line does the new Standard Title usually appear? 2 or 4?
    3. What line does the Standard in the header appear? 0 or 1?
    4. What line does the body text in a page start? 4th line onwards or between the 2nd line and 2nd last line? 

    Args:
        pages (list[str]): List of page texts (each as a string).

    Returns:
        dict[str, str]: Mapping of standard titles to combined page content.
    """
    standards = {}
    current_standard = None
    current_text = []

    # Match pattern like "QI 1:", "QI 2.3A:", "CC 10.2:" etc.
    standard_pattern = re.compile(r"^[A-Z]{2,4}\s*\d+[A-Z0-9.: -]*:")

    for i, text in enumerate(pages, start=1): # CHANGEABLE
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) < 5:
            # Skip or log short / blank pages
            continue

        # Check if lines[4] looks like a new standard
        line4 = lines[4] # CHANGEABLE
        new_standard_match = standard_pattern.match(line4)

        if new_standard_match:
            # If a previous standard exists, finalize it
            if current_standard:
                standards[current_standard] = "\n".join(current_text).strip()
                current_text = []

            # Extract the new standard title from line[0]
            current_standard = lines[0].strip() #CHANGEABLE
            # Start body text from line[4] onward
            current_text.append("\n".join(lines[4:]).strip())

        else:
            # Same standard continues — just add the page text
            current_text.append("\n".join(lines[4:]).strip())

    # Add the last standard at end of document
    if current_standard and current_text:
        standards[current_standard] = "\n".join(current_text).strip()

    return standards


def standard_to_elements(standard_body: str) -> dict[str,str]:
    """
    Splits a standard's full body text into elements, where each element starts with
    'Element <Letter>:' and continues until the next element or the end of the document.

    Args:
        standard_body (str): The body text of one standard (as a single string).

    Returns:
        dict[str, str]: Mapping of element titles (e.g. 'Element A: ...') to their content.

    Raises:
        ValueError: If no elements are found in the standard body.
    """
    # Matches lines like "Element A:", "Element B:", "Element AA:", etc.
    element_pattern = re.compile(r"(?m)^Element\s+[A-Z]{1,2}:\s+.*")

    matches = list(element_pattern.finditer(standard_body))
    if not matches:
        raise ValueError("❌ No element headers found in the provided standard text.")

    elements = {}

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(standard_body)
        element_title = match.group(0).strip()
        
        # Remove first letter if double-letter element (usually striked text)
        if len(element_title.split()[1]) > 2:
            element_title = "Element " + element_title.split()[1][1:] + ' ' + ' '.join(element_title.split()[2:])
        
        element_body = standard_body[start + len(element_title):end].strip()
        elements[element_title] = element_body

    return elements

    
def get_index(standard_header: str) -> str:
    return standard_header.split(':')[0].strip()


def get_title(standard_header: str) -> str:
    return standard_header.split(':')[1].strip()
