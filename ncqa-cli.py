#!/usr/bin/env python3
 
import fire
from workflows import parse_pdfs_in_dir, parse_pdf_incremental

if __name__=='__main__':
    fire.Fire({
        'parse-dir': parse_pdfs_in_dir,
        'parse-pdf': parse_pdf_incremental
    })
