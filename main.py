import fitz
import re

from mylib import io_utils as utils
from workflows import *


if __name__ == "__main__":
    # utils.clear_csv("./output.csv")
    
    # DIR_PATH = "/home/owly/Documents/ncqa-parser/ncqa_2026"
    # parse_pdfs_in_dir(DIR_PATH, "./output.csv")
    
    # DIR_PATH = "/home/owly/Documents/ncqa-parser/ncqa_2026_2"
    # parse_pdfs_in_dir(DIR_PATH, "./output.csv")

    PDF_PATH = "reordered2.pdf"
    parse_pdf_incremental(PDF_PATH, "./output_im3.csv")
