import fitz
import re
import json

from mylib.datamodels import Factor
from mylib import factor

def get_index(element_header:str) -> str:
    """
    Extracts the element index (e.g., 'Element A') from a header like
    'Element A: QI Program Structure'.

    Args:
        element_header (str): The full element header line.

    Returns:
        str: The element index (e.g., 'Element A'), or None if not found.
    """
    match = re.match(r"^(Element\s+[A-Z]{1,2})\s*:", element_header.strip())
    return match.group(1) if match else None


def get_title(element_header: str) -> str:
    """
    Extracts the title portion from an element header, e.g.
    'Element A: QI Program Structure' → 'QI Program Structure'.

    Args:
        element_header (str): The full element header line.

    Returns:
        str: The title text after the colon, or None if not found.
    """
    parts = element_header.split(":", 1)
    if len(parts) < 2:
        return None
    return parts[1].strip()


def get_scoring(element_body:str) -> str:
    """
    Extracts the scoring section from an element body and 
    formats it into a JSON string.
    
    Args:
        element_body (str): The body of element text
        
    Returns:
        str: JSON string with fields as shown 
        {
            'met': {
                'description': 'The organization meets 5 factors',
                'min_num_factors': 5,
                'max_num_factors': 5
            },
            'partially_met': {
                'description': 'The organization meets 3-4 factors',
                'min_num_factors': 3,
                'max_num_factors': 4
            }, 
            'not_met': {
                'description': 'The organization meets 0-2 factors',
                'min_num_factors': 0,
                'max_num_factors': 2
            }
        }
    """
    text = get_scoring_text(element_body)
    formatted_text = format_scoring(text)
    return formatted_text


def get_scoring_text(element_body: str) -> str:
    """
    Extracts the 'Scoring' section from an element body.

    The scoring section starts at the line 'Scoring' and ends before
    the next major section header (e.g. 'Data source', 'Scope of review',
    'Documentation', etc.), or the end of the text.

    Args:
        element_body (str): Full element text.

    Returns:
        str: The scoring section text (without the 'Scoring' header).

    Raises:
        ValueError: If no 'Scoring' section is found in the text.
    """
    pattern = re.compile(
        r"(?ms)^Scoring\s*(.*?)^(?:Data source|Scope of|Documentation|Look-back|Explanation|Factor\s+\d+:|Exceptions|Related information|Examples|$)"
    )

    match = pattern.search(element_body)
    if not match:
        raise ValueError("❌ No 'Scoring' section found in the provided element body.")

    scoring_text = match.group(1).strip()
    return scoring_text


def format_scoring(scoring_text: str) -> str:
    """
    Formats the scoring text into a structured JSON string.

    Assumes the scoring text always has these 3 categories in order:
    ["Met", "Partially Met", "Not Met"]

    Each scoring description starts with either:
      - 'The organization' or
      - 'No scoring'
    and continues until the next description or the end of the section.

    Args:
        scoring_text (str): Raw scoring text from the element body.

    Returns:
        str: JSON-formatted string of the scoring breakdown.

    Raises:
        ValueError: If fewer than 3 scoring descriptions are found.
    """
    categories = ["Met", "Partially Met", "Not Met"]

    # Clean up and normalize text
    lines = [line.strip() for line in scoring_text.splitlines() if line.strip()]
    try:
        not_met_idx = lines.index("Not Met")
    except ValueError:
        raise ValueError("❌ 'Not Met' not found — malformed scoring text.")

    desc_block = "\n".join(lines[not_met_idx + 1 :])
    if not desc_block:
        raise ValueError("❌ No scoring descriptions found after category headers.")

    # Find all lines that begin with "The organization" or "No scoring"
    pattern = re.compile(
        r"(?m)^(The organization.*|The description.*|No scoring.*|An average.*|High.*|Medium.*|Low.*)",
        re.IGNORECASE
    )
    matches = list(pattern.finditer(desc_block))

    if len(matches) < 3:
        raise ValueError(
            f"❌ Expected 3 scoring descriptions, but found {len(matches)}. Text:\n{desc_block[:300]}"
        )

    # Capture description blocks between each match
    descriptions = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(desc_block)
        block = desc_block[start:end].strip()
        descriptions.append(block)

    # Factor pattern for extracting numbers
    factor_pattern = re.compile(r"(\d+)(?:-(\d+))?\s*factors?", re.IGNORECASE)

    result = {}
    for cat, desc in zip(categories, descriptions):
        label = cat.lower().replace(" ", "_")
        entry = {"description": desc.replace("\n", " ").strip()}

        match = factor_pattern.search(desc)
        if match:
            entry["min_num_factors"] = int(match.group(1))
            entry["max_num_factors"] = int(match.group(2)) if match.group(2) else int(match.group(1))

        result[label] = entry

    return json.dumps(result, indent=4)


def get_data_source(element_body: str) -> list[str]:
    """
    Extracts the list of data sources from an element body.

    Expected pattern:
        Data source
        Documented process
    or:
        Data source
        Documented process, Reports

    Args:
        element_body (str): Full element text.

    Returns:
        list[str]: List of data sources (e.g., ["Documented process", "Reports"]).

    Raises:
        ValueError: If 'Data source' or its corresponding line cannot be found.
    """
    lines = [line.strip() for line in element_body.splitlines() if line.strip()]

    for i, line in enumerate(lines):
        if line.lower() == "data source":
            if i + 1 >= len(lines):
                raise ValueError("❌ Found 'Data source' but no following line.")
            next_line = lines[i + 1]
            # Split by comma and strip extra spaces
            return [src.strip() for src in next_line.split(",") if src.strip()]

    raise ValueError("❌ 'Data source' not found in element body.")


def get_explanation(element_body: str) -> str:
    """
    Extracts the 'Explanation' section from an element body.

    Captures all text starting from the line 'Explanation'
    until the line 'Examples' (exclusive).

    Args:
        element_body (str): Full element text.

    Returns:
        str: The extracted explanation text (trimmed).

    Raises:
        ValueError: If 'Explanation' or the section text is not found.
    """
    pattern = re.compile(r"(?ms)^Explanation\s*(.*?)^Examples\s*\n", re.IGNORECASE)

    match = pattern.search(element_body)
    if not match:
        raise ValueError("❌ Could not find 'Explanation' section in element body.")

    explanation_text = match.group(1).strip()
    if not explanation_text:
        raise ValueError("❌ 'Explanation' section found but empty.")

    return explanation_text


def get_factors_text(element_body: str) -> str:
    """
    Extracts the text from the start of the element body
    until the line before 'Summary of Changes'.

    Args:
        element_body (str): Full element text.

    Returns:
        str: The extracted text containing the factor section.

    Raises:
        ValueError: If 'Summary of Changes' is not found.
    """
    pattern = re.compile(r"(?ms)^(.*?)(?=^Summary of Changes)", re.IGNORECASE)
    match = pattern.search(element_body)

    if not match:
        raise ValueError("❌ 'Summary of Changes' not found in element body.")

    factors_text = match.group(1).strip()
    return factors_text


def element_to_factors(element_body:str) -> list[Factor]:
    element_factors = get_factors_text(element_body)
    num_factors = factor.get_num_factors(element_factors)
    if num_factors == 0:
        print(f"No factors in {element_body[:100]}...")
        pass #TODO: Make functions for elements with no factors
    
    factors: list[Factor] = []
    element_explanation = get_explanation(element_body)
    for i in range(1, num_factors+1):
        factor_index = factor.get_index(element_factors, i)
        factor_title = factor.get_title(element_explanation, element_factors, i)
        factor_description = factor.get_description(element_factors, i)
        factor_explanation = factor.get_explanation(element_explanation, i)
        factor_critical:bool = factor.check_critical(element_factors, i)
        
        factors.append(Factor(
            factor_index=factor_index,
            factor_title=factor_title,
            factor_description=factor_description,
            factor_explanation=factor_explanation,
            factor_critical=factor_critical
        ))

    return factors
    

def check_must_pass(element_explanation: str) -> bool:
    """
    Checks if 'MUST-PASS' appears within the first 50 characters
    of the element explanation text.

    Args:
        element_explanation (str): The explanation text.

    Returns:
        bool: True if 'MUST-PASS' appears within the first 50 characters, else False.
    """
    if not element_explanation:
        return False

    snippet = element_explanation[:50].upper() # Arbitrary length, usually in first sentence.
    return "MUST-PASS" in snippet

