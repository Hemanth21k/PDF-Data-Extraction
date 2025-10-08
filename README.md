# PDF-Data-Extraction

A small utility to extract data from PDF files using PyMuPDF (fitz).

## Overview

This repository contains a simple script `extract_images.py` that opens a PDF from the `input_pdfs/` folder, reads the PDF metadata (title) and extracts images into the `output_images/<PDF Title>/images/` directory.

The intended output layout for each processed PDF is:

```
output_images/
	<PDF Title>/
		images/
		tables/     # reserved for extracted tables (not implemented)
		text/       # reserved for extracted text (not implemented)
```

The script currently extracts images only. The `tables/` and `text/` folders are included in the README as intended destinations if you extend the project to extract those artifacts.

## Project structure

```
.
├── extract_images.py      # main script that extracts images using PyMuPDF
├── input_pdfs/            # place source PDF files here
│   └── NIPS-2017-attention-is-all-you-need-Paper.pdf
├── output_images/         # generated output (created by the script)
│   └── <PDF Title>/
│       ├── images/
│       ├── tables/        # optional/placeholder
│       └── text/          # optional/placeholder
├── requirements.txt       # Python dependencies
└── README.md
```

## Setup

Create a virtual environment, activate it, and install dependencies from `requirements.txt`.

macOS / Linux (zsh / bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Notes:
- The `requirements.txt` in this repo currently contains `PyMuPDF==1.26.4`.
- Use the included virtual environment commands to keep dependencies isolated.

## Usage

1. Put PDFs you want to process into the `input_pdfs/` directory.
2. Run the script:

```bash
python extract_images.py
```

By default the script reads the pdf files it finds in `input_pdfs/`, opens it, reads the PDF metadata `title`, and creates an output folder under `output_images/<title>/`. Each extracted image is saved as `output_images/<title>/images/page{page_no}_img{idx}.{ext}`.

Example output after running the script on `NIPS-2017-attention-is-all-you-need-Paper.pdf`:

```
output_images/
	Attention is All you Need/
		images/
			page3_img1.png
			page4_img1.png
			page4_img2.png
```

## Extending the script

- To extract text, use PyMuPDF's `page.get_text()` or `page.get_text("blocks")` and save to the `text/` folder.
- To extract tables, consider using an OCR-based tool or table extraction library and save CSV/JSON to the `tables/` folder.

## Troubleshooting

- If the script fails to open a PDF, check the file path and permissions.
- If `pdf_document.metadata['title']` is empty, the script will attempt to use an empty folder name; you may want to modify the script to fall back to the filename when title metadata is not present.

## License

MIT License — see `LICENSE` if included.

## Contact

Open issues or submit a PR if you want improvements or features added.
