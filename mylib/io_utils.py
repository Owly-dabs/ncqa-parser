import fitz


def read_pdf_pages(pdf_path) -> list[str]:
    """
    Reads a PDF and returns a list where each element is the text of one page.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        list[str]: A list of strings, each representing a page's text.
    """
    pages = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text("text").strip()
            pages.append(text)
    return pages