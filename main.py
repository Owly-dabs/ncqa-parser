import fitz
import re

from workflows import *


if __name__ == "__main__":
    PDF_PATH = "/home/owly/Documents/ncqa-parser/ncqa_2025/04 - Quality Management and Improvement.pdf"

    parse_pdf_incremental(PDF_PATH, "./output.csv")
    
    # pages = utils.read_pdf_pages(PDF_PATH)
    
    # # ------------------------ FUNCTIONAL_AREA --------------------------
    # functional_area = pages[0].replace("\n", "")
    # print(functional_area)

    # # ------------------------ STANDARD --------------------------
    # standard_dict = standard.separate_pages_by_standard(pages[1:])
    # print(standard_dict.keys())
    # first_element = list(standard_dict.keys())[0]
    # first_standard_body = standard_dict[first_element]
    # #print(first_standard_body)
    
    # # ------------------------ ELEMENTS --------------------------
    # elements_dict = standard.standard_to_elements(first_standard_body)
    # for k,v in elements_dict.items():
    #     # print(f"{k}:\n{v}\n")
    #     element_header = k
    #     element_body = v
    #     break
    
    # element_index = element.get_index(element_header)
    # print(element_index)

    # element_title = element.get_title(element_header)
    # print(element_title)

    # element_scoring = element.get_scoring(element_body)
    # print(element_scoring)

    # element_data_sources = element.get_data_source(element_body)
    # print(element_data_sources)
    
    # element_explanation = element.get_explanation(element_body)
    # print(element_explanation)

    # factors_text = element.get_factors_text(element_body)
    # print(factors_text)
    
    # factors_list = element.element_to_factors(element_body)
    # for fact in factors_list:
    #     print(fact.factor_index)
    #     print(fact.factor_title)
    #     print(fact.factor_description)
    #     print(fact.factor_explanation)
    #     print(fact.factor_critical)

    # print(pages[0])