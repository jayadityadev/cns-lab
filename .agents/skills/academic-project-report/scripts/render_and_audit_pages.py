"""Render all pages of a compiled PDF into PNG images and output page audit metrics.

Uses PyMuPDF (fitz) to convert pages at 150 DPI and print diagnostic first/last line
traces so agents can visually or textually audit layout density, page overflows,
and check for unwanted blank spaces.

Usage:
    python render_and_audit_pages.py [--pdf path/to/report.pdf] [--out path/to/rendered_pages]
"""

import os
import sys
import argparse
import shutil
from pathlib import Path

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF (fitz) is not installed. Install via: pip install pymupdf")
    sys.exit(1)


def audit_and_render(pdf_path: Path, output_dir: Path):
    if not pdf_path.exists():
        print(f"Error: PDF file '{pdf_path}' not found.")
        sys.exit(1)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    total_pages = len(doc)
    print(f"Loaded '{pdf_path.name}' with {total_pages} pages.")

    rendered_files = []
    issues_detected = []

    print("-" * 78)
    print(f"{'Page':<6} | {'Top Line Preview':<35} | {'Bottom Line Preview':<30}")
    print("-" * 78)

    for idx, page in enumerate(doc):
        page_num = idx + 1
        pix = page.get_pixmap(dpi=150)
        img_path = output_dir / f"page_{page_num:02d}.png"
        pix.save(str(img_path))
        rendered_files.append(img_path)

        # Extract text snippets for quick sanity check
        text = page.get_text().strip()
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if not lines:
            first_clean = "[BLANK / IMAGE ONLY]"
            last_clean = "[BLANK / IMAGE ONLY]"
            # If there are no images on this page either, flag as potential blank page
            image_list = page.get_images()
            if not image_list:
                issues_detected.append(f"Page {page_num}: Completely blank page detected.")
        else:
            first_clean = lines[0][:35].encode("ascii", "replace").decode("ascii")
            last_clean = lines[-1][:30].encode("ascii", "replace").decode("ascii")

        print(f"{page_num:<6} | {first_clean:<35} | {last_clean:<30}")

    print("-" * 78)
    print(f"\nRendered all {total_pages} pages to: {output_dir.resolve()}")

    if issues_detected:
        print("\n[!] Potential Layout Issues Detected:")
        for issue in issues_detected:
            print(f"    - {issue}")
    else:
        print("\n[OK] No completely blank text/image pages detected.")

    return total_pages, rendered_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render PDF pages to PNG and audit layout.")
    parser.add_argument("--pdf", type=str, default="report/main.pdf", help="Path to PDF file")
    parser.add_argument("--out", type=str, default="report/rendered_pages", help="Output directory for PNGs")
    args = parser.parse_args()

    audit_and_render(Path(args.pdf), Path(args.out))
