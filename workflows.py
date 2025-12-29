import pandas as pd
from datetime import datetime
from pathlib import Path
from tqdm import tqdm 

from mylib import document, element, standard, io_utils as utils
from mylib.logs import logger


COLUMNS = [
    "source", "functional_area", "standard_index", "standard_title",
    "element_index", "element_title", "element_scoring", "element_data_source",
    "element_must_pass", "element_explanation", "element_num_factors",
    "element_reference", "factor_index", "factor_title", "factor_description",
    "factor_explanation", "factor_critical", "factor_reference",
    "effective_date", "updated_at"
]


def parse_pdfs_in_dir(dir_path: str, output_csv: str):
    """Parse all PDF files in a directory and append data to a CSV file.

    Args:
        dir_path (str): Path to the directory containing PDF files to process.
        output_csv (str): Path where the output CSV file will be created/appended.

    Raises:
        FileNotFoundError: If the specified directory does not exist.

    Returns:
        None

    Example:
        >>> parse_pdfs_in_dir("/path/to/pdfs", "output.csv")
    """
    dir_path = Path(dir_path)
    output_csv = Path(output_csv)

    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {dir_path}")

    pdf_files = sorted([p for p in dir_path.glob("*.pdf")])
    if not pdf_files:
        logger.warning("⚠️ No PDF files found in directory.")
        return

    logger.info(f"📚 Found {len(pdf_files)} PDF files to process in '{dir_path}'")
    logger.info(f"📝 Output CSV: {output_csv}")

    start_time = datetime.now()

    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            parse_pdf_incremental(pdf_path, output_csv)
        except Exception as e:
            logger.debug(f"❌ Error processing {pdf_path.name}: {e}")
            continue

    logger.info(f"✅ Completed parsing {len(pdf_files)} PDFs in {datetime.now() - start_time}")
    logger.info(f"📄 Output saved to: {output_csv}")


def parse_pdf_incremental(pdf_path: str, output_csv: str):
    """Parse a single PDF file incrementally and append data to CSV.

    Args:
        pdf_path (str): Path to the PDF file to be parsed.
        output_csv (str): Path to the CSV file where data will be appended.

    Returns:
        None

    Note:
        This function uses the v2 parsing method which is less strict than v1,
        allowing for more flexible parsing of document structures.
    """
    SOURCE = "NCQA Health Plan Standards"
    pdf_path = Path(pdf_path)
    output_csv = Path(output_csv)

    pages = utils.read_pdf_pages(pdf_path)
    functional_area = document.get_functional_area(pages)
    effective_date = document.get_date(pages)
    year = document.get_year_from_date(effective_date)
    standards = standard.separate_pages_by_standard_v2(pages) #NOTE: v2 is less strict

    # Track whether we’ve written the header yet
    write_header = not output_csv.exists()

    for std_header, std_body in standards.items():
        std_index = standard.get_index(std_header)
        std_title = standard.get_title(std_header)
        elements_dict = standard.standard_to_elements(std_body)

        rows = []  # rows for this standard

        for elem_header, elem_body in elements_dict.items():
            elem_index = element.get_index(elem_header)
            elem_title = element.get_title(elem_header)
            elem_scoring = element.get_scoring(elem_body) 
            elem_data_source = element.get_data_source(elem_body)
            elem_explanation = element.get_explanation(elem_body)
            elem_ref = ', '.join([SOURCE, year, std_index, elem_index])
            elem_must_pass = element.check_must_pass(elem_explanation)
            elem_factors = element.element_to_factors(elem_body)
            elem_factors_text = element.get_factors_text(elem_body)
            elem_num_factors = len(elem_factors)

            if elem_num_factors == 0:
                rows.append({
                    "source": SOURCE,
                    "functional_area": functional_area,
                    "standard_index": std_index,
                    "standard_title": std_title,
                    "element_index": elem_index,
                    "element_title": elem_title,
                    "element_scoring": elem_scoring,
                    "element_data_source": elem_data_source,
                    "element_must_pass": elem_must_pass,
                    "element_explanation": elem_explanation,
                    "element_num_factors": elem_num_factors,
                    "element_reference": elem_ref,
                    "factor_index": "",
                    "factor_title": "",
                    "factor_description": elem_factors_text.replace("\n", " "),
                    "factor_explanation": "",
                    "factor_critical": "",
                    "factor_reference": elem_ref,
                    "effective_date": effective_date,
                    "updated_at": datetime.now().strftime("%Y-%m-%d")
                })

            for fact in elem_factors:
                rows.append({
                    "source": SOURCE,
                    "functional_area": functional_area,
                    "standard_index": std_index,
                    "standard_title": std_title,
                    "element_index": elem_index,
                    "element_title": elem_title,
                    "element_scoring": elem_scoring,
                    "element_data_source": elem_data_source,
                    "element_must_pass": elem_must_pass,
                    "element_explanation": elem_explanation,
                    "element_num_factors": elem_num_factors,
                    "element_reference": elem_ref,
                    "factor_index": fact.factor_index,
                    "factor_title": fact.factor_title,
                    "factor_description": fact.factor_description,
                    "factor_explanation": fact.factor_explanation,
                    "factor_critical": fact.factor_critical,
                    "factor_reference": ', '.join([elem_ref, fact.factor_index]),
                    "effective_date": effective_date,
                    "updated_at": datetime.now().strftime("%Y-%m-%d")
                })

        # Convert this standard’s data to DataFrame
        df = pd.DataFrame(rows, columns=COLUMNS)

        # Append to CSV (write header only if first time)
        df.to_csv(
            output_csv,
            mode="a",
            header=write_header,
            index=False,
            encoding="utf-8"
        )

        write_header = False  # after first write

        logger.info(f"✅ Written standard {std_index} ({len(rows)} rows) to {output_csv.name}")