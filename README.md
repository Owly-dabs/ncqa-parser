# 🧩 NCQA Parser

A lightweight Python CLI that parses NCQA audit PDFs into structured CSV data for analysis and automation.

---

## 🚀 Installation

You can install the CLI directly with a single command — no manual setup needed:

```bash
curl -fsSL https://raw.githubusercontent.com/Owly-dabs/ncqa-parser/main/install.sh | sh
```

This will:

* Clone the latest version of **ncqa-parser** to `~/.ncqa-parser`
* Install Python dependencies automatically
* Add the CLI to your `PATH` (so it’s available globally)

Once complete, restart your terminal or run:

```bash
source ~/.zshrc   # or ~/.bashrc depending on your shell
```

---

## 🧰 Usage

Run the CLI from anywhere:

```bash
ncqa-cli.py [options]
```

### Example

To parse all NCQA PDFs in a dir:
```bash
ncqa-cli.py parse-dir /path/to/pdfs/dir ./output.csv
```

To parse a single NCQA PDF:
```bash
ncqa-cli.py parse-pdf /path/to/ncqa.pdf ./output.csv
```

---

## 🛠️ Updating

To update to the latest version:

```bash
curl -fsSL https://raw.githubusercontent.com/Owly-dabs/ncqa-parser/refs/heads/main/install.sh | sh
```

The installer will detect your existing installation and pull the latest changes.

---

## 🧼 Uninstalling

To remove ncqa-parser completely:

```bash
rm -rf ~/.ncqa-parser
```

Then remove the line containing `ncqa-parser` from your shell config file (`.zshrc` or `.bashrc`).

---

## 🧾 Requirements

* Python 3.7 or newer
* Pip installed
* Git installed
* Internet access (for first-time setup)

---

## 💡 Notes

* The tool installs itself under `~/.ncqa-parser` by default.
* The installer is idempotent — you can rerun it safely anytime.
* All dependencies are managed via `pip` inside your system Python.

---

## CSV Columns
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
