import fitz
import re

from mylib import io_utils as utils
from workflows import *


if __name__ == "__main__":
    # utils.clear_csv("./output.csv")
    
    DIR_PATH = "./FILL_THIS_DIRECTORY"
    parse_pdfs_in_dir(DIR_PATH, "./output.csv")

    # PDF_PATH = "./FILL_THIS_FILE"
    # parse_pdf_incremental(PDF_PATH, "./output.csv")
