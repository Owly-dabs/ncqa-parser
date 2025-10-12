import fitz
import pandas as pd


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

    
def clear_csv(file_path: str, header=False):
    """
    Clears a csv file. Leaves the header by default
    """
    df = pd.read_csv(file_path, nrows=0)  # read only the header
    df.to_csv(file_path, index=False)     # overwrite file with just the header
    print(f"✅ Cleared all rows except header in '{file_path}'")