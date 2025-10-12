# NCQA PDF Parser

A Python tool for parsing NCQA (National Committee for Quality Assurance) Health Plan Accreditation PDF documents into structured CSV data.

## Installation and use
1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Edit `main.py` with the directory of file path
3. Run `main.py`
```bash
python main.py
```

## Columns
* source -- from header
* functional_area -- title page
* standard_index -- parse header line
* standard_title -- parse header line
* element_index -- Element header
* element_title -- Element header
* element_scoring -- Element body -> Scoring
* element_data_source -- Element body -> Data source
* element_must_pass -- Element body -> Explanation "MUST-PASS"
* element_explanation -- Element body -> From start to "Summary of * Changes"
* element_num_factors -- Element body -> Explanation	
* element_reference -- Source, Year, standard_index, element_index
* factor_index -- element body -> factors	
* factor_title -- explanation factor header if not, * factor_description
* factor_description -- element body -> factors
* factor_explanation -- explanation factor
* factor_critical -- element body -> factors, check for * and *Critical facto
* factor_reference -- element_reference, factor_index	
* effective_date	
* updated_at
