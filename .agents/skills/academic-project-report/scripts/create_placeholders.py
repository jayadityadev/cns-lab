"""Create professional academic image placeholders with institutional branding.

Generates double-bordered placeholder cards with university maroon accent lines
so LaTeX documents compile cleanly without missing-image errors before the user
drops actual terminal or code screenshots into the project.

Usage:
    python create_placeholders.py [--dir report/figures]
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is not installed. Install via: pip install pillow")
    sys.exit(1)


def create_placeholder(
    path: Path,
    width: int = 1000,
    height: int = 600,
    title: str = "FIGURE PLACEHOLDER",
    subtitle: str = "Drop actual screenshot or image here",
    primary_color: tuple = (128, 0, 0),
):
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (width, height), color=(248, 249, 250))
    draw = ImageDraw.Draw(img)

    # Outer and inner border
    draw.rectangle([(2, 2), (width - 3, height - 3)], outline=primary_color, width=3)
    draw.rectangle([(8, 8), (width - 9, height - 9)], outline=(180, 190, 200), width=1)

    # Accent decorative top bar
    draw.rectangle([(8, 8), (width - 9, 24)], fill=primary_color)

    # Text rendering
    draw.text((width // 2, height // 2 - 20), title, fill=(30, 41, 59), anchor="mm")
    if subtitle:
        draw.text((width // 2, height // 2 + 20), subtitle, fill=(100, 116, 139), anchor="mm")

    img.save(path)
    print(f"Created placeholder: {path}")


def generate_default_suite(base_dir: Path):
    """Generates the standard set of placeholders for an academic report."""
    code_dir = base_dir / "code"
    screens_dir = base_dir / "screenshots"

    # 1. Official Presentation Photograph
    create_placeholder(
        base_dir / "team_presentation.jpg",
        width=1200,
        height=750,
        title="PROJECT PRESENTATION & DEFENSE PHOTOGRAPH",
        subtitle="Drop official presentation photo (JPEG/PNG) here",
    )

    # 2. Standard Code Snippet Placeholders
    code_snippets = [
        ("listing_01_core.jpg", "Listing 1: Core Algorithm Implementation"),
        ("listing_02_pipeline.jpg", "Listing 2: Pipeline Transformation & Logic"),
        ("listing_03_verification.jpg", "Listing 3: Verification & Invertibility Logic"),
        ("listing_04_tamper.jpg", "Listing 4: Integrity & Edge Case Handling"),
    ]
    for filename, title in code_snippets:
        create_placeholder(code_dir / filename, width=950, height=550, title=title)

    # 3. Standard Execution Screenshots
    screenshots = [
        ("screenshot_01_main_menu.png", "Figure: Unified CLI / Application Interface"),
        ("screenshot_02_execution_primary.png", "Figure: Primary Execution & Validation"),
        ("screenshot_03_execution_secondary.png", "Figure: Secondary Algorithm Execution"),
        ("screenshot_04_attack_or_tamper.png", "Figure: Edge Case / Tamper Detection Output"),
    ]
    for filename, title in screenshots:
        create_placeholder(screens_dir / filename, width=1100, height=520, title=title)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate styled academic image placeholders.")
    parser.add_argument("--dir", type=str, default="report/figures", help="Base figures directory")
    args = parser.parse_args()

    generate_default_suite(Path(args.dir))
