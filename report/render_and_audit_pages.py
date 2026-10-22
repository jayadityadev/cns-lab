"""Render all pages of report/main.pdf into PNG images and output page audit metrics.

Target: report/rendered_pages/page_NN.png
"""

import os
import sys
import shutil
from pathlib import Path

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import fitz  # PyMuPDF


def audit_and_render():
    pdf_path = Path("report/main.pdf")
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found.")
        sys.exit(1)

    output_dir = Path("report/rendered_pages")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    print(f"Loaded {pdf_path.name} with {total_pages} pages.")

    rendered_files = []
    for idx, page in enumerate(doc):
        page_num = idx + 1
        pix = page.get_pixmap(dpi=150)
        img_path = output_dir / f"page_{page_num:02d}.png"
        pix.save(str(img_path))
        rendered_files.append(img_path)
        
        # Extract text snippets for quick sanity check
        text = page.get_text().strip()
        first_line = text.split("\n")[0] if text else "[EMPTY PAGE]"
        last_line = text.split("\n")[-1] if text else "[EMPTY PAGE]"
        first_clean = first_line[:40].encode("ascii", "replace").decode("ascii")
        last_clean = last_line[:30].encode("ascii", "replace").decode("ascii")
        print(f"Page {page_num:02d}: {first_clean:<40} | Last: {last_clean}")

    print(f"\nRendered all {total_pages} pages to {output_dir.resolve()}")
    return total_pages, rendered_files


if __name__ == "__main__":
    audit_and_render()
