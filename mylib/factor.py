import re


def get_num_factors(factors_text: str) -> int:
    """
    Counts the number of numbered factors in the given text.

    Example pattern:
        1. The QI program structure.
        2. The behavioral healthcare aspects of the program.
        ...

    Args:
        factors_text (str): The text containing the factor list.

    Returns:
        int: Number of factors detected (0 if none found).
    """
    # Match lines starting with e.g. "1. ", "2. ", etc.
    pattern = re.compile(r"(?m)^\s*\d+\.\s+")
    matches = pattern.findall(factors_text)

    return len(matches)


def get_index(factors_text: str, index: int) -> str:
    return f"Factor {str(index)}"


def get_title(element_explanation: str, factors_text: str, index: int) -> str:
    title: str | None = get_title_from_explanation(element_explanation, index)
    if title: return title
    
    title: str | None = get_title_from_factors_text(factors_text, index)
    if title: return title
    
    raise ValueError(f"❌ No title found for factor {index}.")


def get_title_from_explanation(element_explanation: str, index: int) -> str | None:
    """
    Extracts the title of a specific factor from the element explanation.

    Example:
        For "Factor 2: Behavioral healthcare" → returns "Behavioral healthcare"

    Args:
        element_explanation (str): The full explanation text.
        index (int): The factor number to search for (e.g., 2).

    Returns:
        str | None: The title of the factor, or None if not found.
    """
    # Multiline regex: match a line starting with "Factor {index}:" and capture the title after it
    pattern = re.compile(rf"(?m)^Factor\s+{index}:\s*(.*)")

    match = pattern.search(element_explanation)
    if not match:
        return None

    # Clean up and normalize whitespace
    title = match.group(1).strip()
    return title or None


def get_title_from_factors_text(factors_text: str, index: int) -> str | None:
    """
    Extracts the title of a numbered factor from the factors section text.

    Example:
        For index=1 and the line "1. The QI program structure."
        → returns "The QI program structure"

    Args:
        factors_text (str): Text containing the list of numbered factors.
        index (int): Factor number (e.g., 1, 2, 3...).

    Returns:
        str | None: The factor title, or None if not found.
    """
    # Match a line starting with e.g. "1. ..." and capture everything after the number
    pattern = re.compile(rf"(?m)^\s*{index}\.\s*(.+)")

    match = pattern.search(factors_text)
    if not match:
        return None

    title = match.group(1).strip()
    # Remove trailing period if present (common in NCQA text)
    if title.endswith("."):
        title = title[:-1].strip()

    return title or None


def get_description(factors_text: str, index: int) -> str:
    """
    Extracts the full natural-language description of a factor.

    Combines the introductory sentence (the line before the first numbered factor)
    with the text of the specified factor.

    Example:
        "The organization’s QI program description specifies:" +
        "The behavioral healthcare aspects of the program."
        → "The organization’s QI program description specifies the behavioral healthcare aspects of the program."

    Args:
        factors_text (str): Text containing the factor list.
        index (int): Factor number (e.g., 1, 2, 3...).

    Returns:
        str: The full description of the specified factor.

    Raises:
        ValueError: If the factor index or intro line cannot be found.
    """
    # --- Extract intro (everything before the first numbered line) ---
    intro_match = re.search(r"(?s)^(.*?)^\s*1\.", factors_text, re.MULTILINE)
    intro = re.sub(r"[:\s]+$", "", intro_match.group(1)).strip() if intro_match else ""

    # --- Extract factor-specific line ---
    pattern = re.compile(
        rf"(?ms)^\s*{index}\.\s*(.*?)(?=^\s*\d+\.\s|\Z)"
    )
    match = pattern.search(factors_text)
    if not match:
        raise ValueError(f"❌ Could not find description for factor {index}.")

    # Clean the factor description
    factor_desc = re.sub(r"\s+", " ", match.group(1)).strip()
    if not factor_desc:
        raise ValueError(f"❌ Factor {index} description is empty.")

    # --- Combine intro and factor text ---
    if intro:
        # remove trailing punctuation like ':' or '.' to flow naturally
        intro = intro.rstrip(":.")
        full_desc = f"{intro} {factor_desc}".strip()
    else:
        full_desc = factor_desc

    return full_desc


def get_explanation(element_explanation: str, index: int) -> str:
    """
    Extracts the explanation text specific to a given factor index.

    Handles:
        Factor 3:
        Factor 2-4:
        Factor 1,3
        Factors 2, 3
    and excludes any text on the same line as the 'Factor' label
    (e.g., "Program structure" after 'Factor 3:').

    Stops capturing at the next factor line, or 'Exceptions'/'Related information' line.
    
    Args:
        element_explanation (str): Full element explanation text.
        index (int): Factor number (e.g., 1, 2, 3...).

    Returns:
        str: Explanation text for the specified factor.

    Raises:
        ValueError: If no matching explanation section is found.
    """
    text = element_explanation.strip()

    # Match "Factor"/"Factors" blocks (with or without colon)
    pattern = re.compile(
        r"(?ms)^Factors?\s+([\d,\-–—\s]+)(?::[^\n]*)?\n(.*?)(?=^Factors?\s+\d|^Exceptions?|^Related information|\Z)",
        re.IGNORECASE,
    )

    matches = pattern.findall(text)
    if not matches:
        print(f"❌ No factor explanation sections found for factor {index}.")
        return "No factor explanation provided."
        # raise ValueError(f"❌ No factor explanation sections found for factor {index}. Text: {text}")

    explanations = []

    for factor_spec, content in matches:
        # Normalize factor spec
        factor_spec = factor_spec.replace(" ", "")
        factor_spec = factor_spec.replace("–", "-").replace("—", "-")

        factors = set()
        for part in factor_spec.split(","):
            if "-" in part:
                start, end = part.split("-")
                if start.isdigit() and end.isdigit():
                    factors.update(range(int(start), int(end) + 1))
            elif part.isdigit():
                factors.add(int(part))

        # If current factor applies to the requested index
        if index in factors:
            cleaned = re.sub(r"\s+", " ", content.strip())
            explanations.append(cleaned)

    if not explanations:
        raise ValueError(f"❌ No explanation found for factor {index}. Text: {text}")

    return " ".join(explanations).strip()


def check_critical(factors_text: str, index: int) -> bool:
    """
    Returns True if the specified factor is marked critical.

    A factor is critical iff:
      - Its own factor block ends with '*', AND
      - A footnote line starting with '*Critical factors' exists somewhere in the text.

    Args:
        element_factors (str): The text containing all factors (numbered '1.', '2.', ...).
        index (int): The factor number to check.

    Returns:
        bool: True if critical, else False.
    """
    # 1) Extract the factor block (handles wrapped lines)
    block_re = re.compile(rf"(?ms)^\s*{index}\.\s*(.*?)(?=^\s*\d+\.\s|\*Critical|\Z)")
    m = block_re.search(factors_text)
    if not m:
        return False  # factor not found -> not critical

    factor_block = m.group(1).rstrip()

    # 2) Does the factor block end with '*'?
    has_star = factor_block.endswith("*")

    if not has_star:
        return False

    # 3) Footnote presence: '*Critical factors' line exists
    footnote_present = bool(re.search(r"(?mi)^\*Critical factors\b", factors_text))

    return has_star and footnote_present