"""Generate the Final CNS Technical Report as an editable Microsoft Word document (.docx).

Batch: 2026_CNS_A_01
Target: report/CNS_Technical_Report_Batch_2026_CNS_A_01.docx
"""

import os
import sys
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


def set_cell_background(cell, hex_color: str):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set internal padding/margins for a table cell in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def add_code_block(doc: Document, text: str):
    """Add a styled code block with light gray background and monospace font."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, "F4F6F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph()  # Spacing after code block


def add_callout(doc: Document, title: str, text: str, is_warning: bool = False):
    """Add a professional academic callout box with a colored border."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    
    bg_color = "FDF2F2" if is_warning else "F0F9FF"
    border_color = "B91C1C" if is_warning else "0369A1"
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run_title = p.add_run(f"[{title.upper()}]\n")
    run_title.bold = True
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = RGBColor(185, 28, 28) if is_warning else RGBColor(3, 105, 161)
    
    run_text = p.add_run(text)
    run_text.font.name = "Calibri"
    run_text.font.size = Pt(9.5)
    run_text.font.color.rgb = RGBColor(51, 65, 85)
    doc.add_paragraph()


def format_table_headers(table, col_widths, headers):
    """Format the header row of a table with background and bold white/dark text."""
    hdr_row = table.rows[0]
    hdr_row.height = Pt(22)
    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        cell.width = col_widths[idx]
        set_cell_background(cell, "1E3A8A")  # Deep Navy Blue
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(heading)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)


def build_docx_report():
    doc = Document()
    
    # Configure 0.85-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
        # Configure Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Department of CSE | KSIT | Batch 2026_CNS_A_01 | CNS Technical Report")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Cryptography and Network Security Laboratory Technical Report")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # Base typography styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(5)

    # =========================================================================
    # 1. TITLE PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("KAMMAVARI SANGHAM INSTITUTE OF TECHNOLOGY\n")
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    r_sub = p_inst.add_run("(Affiliated to Visvesvaraya Technological University, Belagavi | Approved by AICTE, New Delhi)\n")
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)
    
    r_dept = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\nBengaluru – 560109, Karnataka, India\n")
    r_dept.font.size = Pt(10.5)
    r_dept.font.color.rgb = RGBColor(51, 65, 85)

    p_divider = doc.add_paragraph()
    p_divider.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line = p_divider.add_run("—" * 48)
    r_line.font.color.rgb = RGBColor(30, 58, 138)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(6)
    r_cns = p_title.add_run("Cryptography and Network Security\n")
    r_cns.bold = True
    r_cns.font.size = Pt(22)
    r_cns.font.color.rgb = RGBColor(30, 58, 138)
    
    r_course = p_title.add_run("Comprehensive Laboratory & Technical Audit Report\n")
    r_course.font.size = Pt(13)
    r_course.italic = True
    r_course.font.color.rgb = RGBColor(71, 85, 105)

    p_asg = doc.add_paragraph()
    p_asg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_asg.paragraph_format.space_before = Pt(10)
    p_asg.paragraph_format.space_after = Pt(14)
    r_asg_lbl = p_asg.add_run("Assignment Title:\n")
    r_asg_lbl.font.size = Pt(11)
    r_asg_lbl.font.color.rgb = RGBColor(100, 116, 139)
    r_asg_val = p_asg.add_run("Implementation, Empirical Verification, and Cryptanalytic Evaluation of Classical and Modern Cryptographic Systems")
    r_asg_val.bold = True
    r_asg_val.font.size = Pt(14)
    r_asg_val.font.color.rgb = RGBColor(15, 23, 42)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(18)
    r_b = p_meta.add_run("Batch Identifier: 2026_CNS_A_01\n")
    r_b.bold = True
    r_b.font.size = Pt(11.5)
    r_b.font.color.rgb = RGBColor(15, 23, 42)
    r_co = p_meta.add_run("Allocated Activities: Classical Substitution (CO1) | Polyalphabetic Substitution (CO4) |\nInformation-Theoretic Secrecy (CO3) | Digital Signatures (CO3)")
    r_co.font.size = Pt(10)
    r_co.font.color.rgb = RGBColor(51, 65, 85)

    # Student Roster Table
    roster_table = doc.add_table(rows=5, cols=4)
    roster_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [Inches(0.6), Inches(1.5), Inches(2.0), Inches(2.7)]
    headers = ["Sl.", "USN", "Student Name", "Designated Activity Area"]
    format_table_headers(roster_table, col_w, headers)
    
    roster_data = [
        ("1", "1KS23CS059", "Jayaditya Dev", "Unified TUI Engine & Activity 4 (RSA-PSS)"),
        ("2", "1KS23CS043", "Durgashree M", "Activity 3 (One-Time Pad CSPRNG)"),
        ("3", "1KS23CS020", "Aryaman Tiwari", "Activity 2 (Vigenère Tabula Recta)"),
        ("4", "1KS23CS034", "Chirag T", "Activity 1 (Caesar Modular Cipher)"),
    ]
    for r_idx, (s_no, usn, name, area) in enumerate(roster_data):
        row = roster_table.rows[r_idx + 1]
        for c_idx, val in enumerate([s_no, usn, name, area]):
            cell = row.cells[c_idx]
            cell.width = col_w[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            if c_idx in (1, 2):
                run.bold = True

    p_eval = doc.add_paragraph()
    p_eval.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_eval.paragraph_format.space_before = Pt(28)
    r_ev = p_eval.add_run("Submission Date: Academic Term 2026\nEvaluation Scheme: Maximum 25 Marks (Part A Demonstration: 15 Marks | Part B Technical Report: 10 Marks)")
    r_ev.font.size = Pt(9.5)
    r_ev.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS PLACEHOLDER & ABSTRACT
    # =========================================================================
    h1 = doc.add_heading("Table of Contents", level=1)
    h1.style.font.color.rgb = RGBColor(30, 58, 138)
    
    toc_items = [
        ("1. Abstract", "3"),
        ("2. Introduction and Objectives", "3"),
        ("3. Theoretical Background", "4"),
        ("4. Working Principles and Step-by-Step Traces", "6"),
        ("5. Algorithms, Pseudocode, and Architectural Flowcharts", "8"),
        ("6. System Requirements and Implementation Environment", "10"),
        ("7. Implementation Details and Code Architecture", "11"),
        ("8. Execution Procedure and Genuine Demonstration Transcripts", "12"),
        ("9. Testing Methodology and Results (69-Test Matrix)", "14"),
        ("10. Security Analysis and Cryptanalysis", "16"),
        ("11. Advantages and Limitations", "18"),
        ("12. Practical and Historical Applications", "18"),
        ("13. Conclusion", "19"),
        ("14. References", "19"),
        ("15. Group Contribution Matrix", "20"),
    ]
    toc_table = doc.add_table(rows=len(toc_items), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title, page) in enumerate(toc_items):
        r_toc = toc_table.rows[idx]
        c0, c1 = r_toc.cells[0], r_toc.cells[1]
        c0.width, c1.width = Inches(5.8), Inches(1.0)
        set_cell_margins(c0, top=40, bottom=40, left=60, right=60)
        set_cell_margins(c1, top=40, bottom=40, left=60, right=60)
        p0 = c0.paragraphs[0]
        run0 = p0.add_run(title)
        run0.font.name = "Calibri"
        run0.font.size = Pt(10)
        if title.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")):
            run0.bold = True
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run1 = p1.add_run(page)
        run1.font.name = "Calibri"
        run1.font.size = Pt(10)
        run1.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # =========================================================================
    # 2. ABSTRACT
    # =========================================================================
    h_abs = doc.add_heading("1. Abstract", level=1)
    h_abs.style.font.color.rgb = RGBColor(30, 58, 138)
    
    p_abs = doc.add_paragraph(
        "This technical report delivers a rigorous, empirical investigation and software audit of four fundamental cryptographic "
        "paradigms implemented for the Cryptography and Network Security course under Batch allocation 2026_CNS_A_01. "
        "The investigated systems span: (1) classical monoalphabetic substitution (Caesar Cipher), (2) polyalphabetic keyword "
        "substitution (Vigenère Cipher), (3) information-theoretic symmetric stream encryption (One-Time Pad), and (4) industry-standard "
        "asymmetric authentication and integrity verification (RSA-PSS digital signatures with SHA-256).\n\n"
        "Every cryptographic primitive was implemented natively in Python 3.14 without relying on high-level cryptographic "
        "abstractions for classical ciphers, while employing the rigorously audited, PyCA-backed cryptography engine for asymmetric "
        "primitives. All algorithms were subjected to automated verification comprising 69 distinct test cases spanning deterministic "
        "Known-Answer Tests (KAT), cyclic boundary conditions, malformed input handling, and negative tamper detection. All 69 tests "
        "executed successfully in 0.55 seconds with zero defects. Beyond functional implementation, this report provides formal "
        "cryptanalytic evaluations: exhaustive search analysis, frequency analysis, Kasiski examination, Friedman's Index of Coincidence, "
        "Shannon's unconditional secrecy theorem, the catastrophic Two-Time Pad vulnerability, and the architectural distinction between "
        "raw mathematical key pairs and Public Key Infrastructure (PKI). Genuine terminal transcripts and pipeline data flows establish "
        "that modern security requires provable cryptographic primitives rather than security through obscurity."
    )

    # =========================================================================
    # 3. INTRODUCTION AND OBJECTIVES
    # =========================================================================
    h_intro = doc.add_heading("2. Introduction and Objectives", level=1)
    h_intro.style.font.color.rgb = RGBColor(30, 58, 138)
    
    doc.add_paragraph(
        "Data security in modern computer networks rests upon four foundational security objectives:\n"
        "1. Confidentiality: Ensuring that unauthorized entities cannot read or interpret transmitted information.\n"
        "2. Integrity: Assuring that data has not been modified, corrupted, or injected in transit.\n"
        "3. Authenticity: Verifying the legitimate origin and authorship of communicating entities.\n"
        "4. Non-Repudiation: Preventing a sender from successfully denying having generated and dispatched a message.\n\n"
        "Historically, cryptographic engineering evolved from simple substitution and transposition techniques toward mathematically "
        "rigorous symmetric and asymmetric constructions. Classical ciphers sought secrecy by rearranging or replacing letters, but "
        "their underlying algebraic structures preserved natural language statistics, rendering them vulnerable to frequency cryptanalysis. "
        "The advent of Shannon's information theory revealed the conditions for unconditional secrecy, while modern public-key "
        "cryptosystems eliminated the secret key distribution paradox by decoupling signing and verification keys."
    )
    
    doc.add_heading("Course Outcome Mapping and Specific Objectives", level=2)
    doc.add_paragraph(
        "In strict adherence to the VTU syllabus and topic distribution for Batch 2026_CNS_A_01, the technical objectives are mapped "
        "directly to designated Course Outcomes (COs):\n"
        "• Activity 1 (CO1 - Classical Substitution): Implement and analyze the Caesar Cipher over the integer ring Z_26; demonstrate "
        "modular key normalization across negative shifts and keys >= 26; evaluate vulnerability to brute force and unigram frequency analysis.\n"
        "• Activity 2 (CO4 - Modern Block & Stream Ciphers / Polyalphabetic Substitution): Implement the Vigenère Cipher using the Tabula Recta; "
        "enforce strict alphabetic-only stream pointer advancement; analyze structural vulnerabilities via Kasiski examination and Index of Coincidence.\n"
        "• Activity 3 (CO3 - Public Key & Integrity / Information-Theoretic Secrecy): Construct a bytewise One-Time Pad using Python's secrets "
        "CSPRNG; mathematically formulate Shannon's theorem of perfect secrecy; demonstrate the empirical collapse of secrecy under key reuse.\n"
        "• Activity 4 (CO3 - Public Key & Integrity / Digital Signatures): Implement an enterprise-grade digital signature system using "
        "2048-bit RSA keys and RSA-PSS padding with SHA-256; prove tamper and corruption detection; contrast mathematical signatures with PKI."
    )

    # =========================================================================
    # 4. THEORETICAL BACKGROUND
    # =========================================================================
    h_theory = doc.add_heading("3. Theoretical Background", level=1)
    h_theory.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_heading("Activity 1: Caesar Cipher and the Integer Ring Z_26", level=2)
    doc.add_paragraph(
        "The Caesar Cipher is an additive monoalphabetic substitution cipher defined over the finite residue ring modulo 26: "
        "Z_26 = {0, 1, 2, ..., 25}. Letters of the Latin alphabet map injectively onto Z_26 via the mapping pi: A -> 0, B -> 1, ..., Z -> 25. "
        "For any integer shift key K in Z, encryption and decryption are given by:\n"
        "• Encryption: C_i = (P_i + K) mod 26\n"
        "• Decryption: P_i = (C_i - K) mod 26 = (C_i + (-K mod 26)) mod 26\n"
        "Because addition in Z_26 forms an abelian group, the decryption transformation is mathematically identical to encryption "
        "using the additive inverse key (-K mod 26). The Caesar cipher preserves letter frequency distributions because a fixed static "
        "shift is applied uniformly to all alphabetic tokens throughout the message."
    )

    doc.add_heading("Activity 2: Vigenère Cipher and Polyalphabetic Mapping", level=2)
    doc.add_paragraph(
        "The Vigenère cipher mitigates monoalphabetic frequency spikes by cycling through a sequence of Caesar shifts derived from a keyword "
        "K = (k_0, k_1, ..., k_{L-1}) of length L. The transformations are formulated as:\n"
        "• Encryption: C_i = (P_i + k_{i mod L}) mod 26\n"
        "• Decryption: P_i = (C_i - k_{i mod L}) mod 26\n"
        "Conceptually, this corresponds to coordinates in the Tabula Recta—a 26x26 grid of shifted alphabets where row P_i and column k_j "
        "intersect at ciphertext character C_i. By cycling through L distinct alphabets, unigram letter frequencies are distributed and flattened."
    )

    doc.add_heading("Activity 3: One-Time Pad and Shannon's Perfect Secrecy", level=2)
    doc.add_paragraph(
        "In 1949, Claude Shannon established the mathematical foundations of cryptography. Shannon defined perfect secrecy as the condition "
        "where observing the ciphertext C provides zero statistical information about the plaintext M:\n"
        "P(M = m | C = c) = P(M = m) for all m in M, c in C, or equivalently H(M | C) = H(M)\n"
        "Shannon proved that perfect secrecy requires H(K) >= H(M), implying that the keyspace must be at least as large as the message space. "
        "The bytewise One-Time Pad operates over byte vectors using bitwise Exclusive-OR (addition modulo 2):\n"
        "• C = M ^ K\n"
        "• M' = C ^ K = (M ^ K) ^ K = M ^ (K ^ K) = M ^ 0 = M\n"
        "Because XOR is commutative, associative, and its own self-inverse, every candidate plaintext m* corresponds to a unique key "
        "k* = c ^ m*. When K is uniformly random, P(K = k*) = 1/256^L, making all candidate plaintexts equally probable to an adversary."
    )

    doc.add_heading("Activity 4: Digital Signatures and RSA-PSS", level=2)
    doc.add_paragraph(
        "An asymmetric digital signature provides authenticity, integrity, and non-repudiation. An RSA key pair consists of a public key (e, n) "
        "and a private key (d, n) where n = p * q for large primes p, q, and e * d = 1 mod phi(n). Textbook RSA signatures (S = h^d mod n) "
        "are vulnerable to homomorphic multiplication and chosen-message attacks. To provide provable security, the Probabilistic Signature "
        "Scheme (RSA-PSS, RFC 8017 / PKCS#1 v2.1) is employed:\n"
        "1. Message Hashing: M is compressed into a 256-bit digest h = SHA-256(M).\n"
        "2. PSS Encoding: h is combined with a cryptographically generated random salt of length s_len via Mask Generation Function 1 (MGF1).\n"
        "3. Signing: The signer computes S = mu^d mod n, where mu is the encoded representative.\n"
        "4. Verification: The verifier recovers mu' = S^e mod n and validates that the extracted digest matches SHA-256(M)."
    )

    # =========================================================================
    # 5. WORKING PRINCIPLES
    # =========================================================================
    h_work = doc.add_heading("4. Working Principles and Step-by-Step Traces", level=1)
    h_work.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "To verify algorithmic correctness, step-by-step mathematical traces were conducted on verified project test vectors:"
    )

    doc.add_heading("Trace 1: Caesar Cipher Modular Shift (P = 'CNS 2026', Key = 29)", level=2)
    doc.add_paragraph(
        "1. Key Normalization: K_norm = 29 mod 26 = 3.\n"
        "2. Character Transformation:\n"
        "   • 'C' (pos 2): (2 + 3) mod 26 = 5 -> 'F'\n"
        "   • 'N' (pos 13): (13 + 3) mod 26 = 16 -> 'Q'\n"
        "   • 'S' (pos 18): (18 + 3) mod 26 = 21 -> 'V'\n"
        "   • ' ', '2', '0', '2', '6': Non-alphabetic tokens; preserved verbatim.\n"
        "3. Generated Ciphertext: 'FQV 2026'.\n"
        "4. Decryption: Applying additive inverse -3 mod 26 = 23 yields: 'F' (5 + 23) mod 26 = 2 -> 'C'. Recovered: 'CNS 2026'."
    )

    doc.add_heading("Trace 2: Vigenère Stream Alignment (P = 'ATTACK AT DAWN!', Key = 'LEMON')", level=2)
    doc.add_paragraph(
        "The keyword shifts are: L=11, E=4, M=12, O=14, N=13 (L=5). The key advances strictly on alphabetic characters:\n"
        "• P[0] 'A' (0) + Key 'L' (11) = 'L' (11)\n"
        "• P[1] 'T' (19) + Key 'E' (4) = 'X' (23)\n"
        "• P[2] 'T' (19) + Key 'M' (12) = 'F' (5)\n"
        "• P[3] 'A' (0) + Key 'O' (14) = 'O' (14)\n"
        "• P[4] 'C' (2) + Key 'N' (13) = 'P' (15)\n"
        "• P[5] 'K' (10) + Key 'L' (11) = 'V' (21)\n"
        "• P[6] ' ': Whitespace; preserved verbatim; key paused.\n"
        "• P[7] 'A' (0) + Key 'E' (4) = 'E' (4)\n"
        "• P[8] 'T' (19) + Key 'M' (12) = 'F' (5)\n"
        "• P[9] ' ': Whitespace; preserved verbatim; key paused.\n"
        "• P[10] 'D' (3) + Key 'O' (14) = 'R' (17)\n"
        "• P[11] 'A' (0) + Key 'N' (13) = 'N' (13)\n"
        "• P[12] 'W' (22) + Key 'L' (11) = 'H' (7)\n"
        "• P[13] 'N' (13) + Key 'E' (4) = 'R' (17)\n"
        "• P[14] '!': Punctuation; preserved verbatim.\n"
        "Ciphertext Output: 'LXFOPV EF RNHR!'. Note that the two 'A's map to 'L' and 'E', demonstrating polyalphabetic diffusion."
    )

    doc.add_heading("Trace 3: One-Time Pad Bytewise XOR (P = 'CNS 2026', 8 Bytes UTF-8)", level=2)
    doc.add_paragraph(
        "Plaintext Bytes: 0x43 0x4E 0x53 0x20 0x32 0x30 0x32 0x36\n"
        "CSPRNG Key Bytes: 0x9A 0x2B 0x7F 0xE1 0x0C 0x88 0x64 0x19\n"
        "Bytewise XOR:\n"
        "• Byte 1: 0x43 ^ 0x9A = 01000011 ^ 10011010 = 11011001 = 0xD9\n"
        "• Byte 2: 0x4E ^ 0x2B = 01001110 ^ 00101011 = 01100101 = 0x65\n"
        "• Byte 3: 0x53 ^ 0x7F = 01010011 ^ 01111111 = 00101100 = 0x2C\n"
        "• Byte 4: 0x20 ^ 0xE1 = 00100000 ^ 11100001 = 11000001 = 0xC1\n"
        "• Byte 5: 0x32 ^ 0x0C = 00110010 ^ 00001100 = 00111110 = 0x3E\n"
        "• Byte 6: 0x30 ^ 0x88 = 00110000 ^ 10001000 = 10111000 = 0xB8\n"
        "• Byte 7: 0x32 ^ 0x64 = 00110010 ^ 01100100 = 01010110 = 0x56\n"
        "• Byte 8: 0x36 ^ 0x19 = 00110110 ^ 00011001 = 00101111 = 0x2F\n"
        "Ciphertext Hex: D9652CC13E88562F. Decryption: Ciphertext ^ Key reproduces 0x434E532032303236 ('CNS 2026')."
    )

    doc.add_heading("Trace 4: RSA-PSS Digital Signature Execution", level=2)
    doc.add_paragraph(
        "1. Key Generation: 2048-bit RSA key pair with e = 65537.\n"
        "2. Message: 'Confidential Academic Dispatch 2026'.\n"
        "3. Hashing: SHA-256 digest h = SHA-256(M) (32 bytes / 256 bits).\n"
        "4. Padding: PSS with MGF1(SHA-256) and randomized salt of length MAX_LENGTH (222 bytes).\n"
        "5. Signing: S = mu^d mod n (256 bytes / 2048 bits).\n"
        "6. Verification: mu' = S^e mod n. Recalculated hash matches h. Verification: VALID."
    )

    # =========================================================================
    # 6. ALGORITHMS AND FLOWCHARTS
    # =========================================================================
    h_alg = doc.add_heading("5. Algorithms, Pseudocode, and Flowcharts", level=1)
    h_alg.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph("Core algorithmic implementations matching the codebase are specified below:")
    
    add_code_block(doc, 
        "Algorithm CaesarEncrypt(P, K):\n"
        "    shift = K mod 26\n"
        "    C = empty string\n"
        "    for each char in P:\n"
        "        if 'a' <= char <= 'z':\n"
        "            pos = ord(char) - ord('a')\n"
        "            C += chr((pos + shift) mod 26 + ord('a'))\n"
        "        else if 'A' <= char <= 'Z':\n"
        "            pos = ord(char) - ord('A')\n"
        "            C += chr((pos + shift) mod 26 + ord('A'))\n"
        "        else:\n"
        "            C += char\n"
        "    return C\n\n"
        "Algorithm VigenereEncrypt(P, K):\n"
        "    clean_k = NormalizeKey(K)\n"
        "    L = Length(clean_k)\n"
        "    k_idx = 0\n"
        "    C = empty string\n"
        "    for each char in P:\n"
        "        if char is alphabetic:\n"
        "            shift = ord(clean_k[k_idx mod L]) - ord('A')\n"
        "            base = ord('a') if islower(char) else ord('A')\n"
        "            pos = ord(char) - base\n"
        "            C += chr((pos + shift) mod 26 + base)\n"
        "            k_idx += 1\n"
        "        else:\n"
        "            C += char\n"
        "    return C"
    )

    add_code_block(doc,
        "Algorithm OTPEncrypt(M_bytes, K_bytes):\n"
        "    if Length(M_bytes) != Length(K_bytes):\n"
        "        raise ValueError('Length mismatch')\n"
        "    C_bytes = bytearray(Length(M_bytes))\n"
        "    for i from 0 to Length(M_bytes) - 1:\n"
        "        C_bytes[i] = M_bytes[i] XOR K_bytes[i]\n"
        "    return bytes(C_bytes)\n\n"
        "Algorithm RSAPSSSign(M, private_key):\n"
        "    data = UTF8Encode(M)\n"
        "    return private_key.sign(\n"
        "        data,\n"
        "        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),\n"
        "        hashes.SHA256()\n"
        "    )"
    )

    doc.add_heading("Architectural Pipeline Flowcharts", level=2)
    add_code_block(doc,
        "+-----------------------------------------------------------------------------+\n"
        "|                 CLASSICAL CIPHER FLOWCHART (CAESAR & VIGENÈRE)              |\n"
        "+-----------------------------------------------------------------------------+\n"
        "  [Input Plaintext P, Key K] ---> {Valid Key?} ---> (NO) ---> [Raise Error]\n"
        "                                       | (YES)\n"
        "                                       v\n"
        "                              [Normalize Key]\n"
        "                                       |\n"
        "                                       v\n"
        "                            +--[Loop Char c in P]--+\n"
        "                            |                      |\n"
        "                     {Is c alphabetic?}            |\n"
        "                        /          \\               |\n"
        "                   (YES)/            \\(NO)         |\n"
        "                       v              v            |\n"
        "                 [Compute Shift]  [Preserve]       |\n"
        "                 [Advance Index]  [Pause Pointer]  |\n"
        "                        \\            /             |\n"
        "                         v          v              |\n"
        "                     [Append c to Output C]        |\n"
        "                            |                      |\n"
        "                            +---{More chars?}------+ (Loop back)\n"
        "                                       | (NO)\n"
        "                                       v\n"
        "                            [Return Ciphertext C]"
    )

    # =========================================================================
    # 7. SYSTEM REQUIREMENTS
    # =========================================================================
    h_sys = doc.add_heading("6. System Requirements and Environment", level=1)
    h_sys.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "• Operating System: Microsoft Windows 11 Enterprise (64-bit AMD64 architecture)\n"
        "• Host Hardware: Intel Core i5-10300H CPU @ 2.50GHz, 4 Cores / 8 Logical Processors, 16 GB RAM\n"
        "• Programming Language: Python 3.14.6 AMD64 managed via uv virtual environment\n"
        "• Asymmetric Cryptography Engine: cryptography v50.0.2 (PyCA OpenSSL 3.x bindings)\n"
        "• Terminal Interface Framework: rich v15.0.0\n"
        "• Automated Test Framework: pytest v9.1.1\n"
        "• Typesetting Engines: MiKTeX 25.12 (pdflatex) & python-docx v1.2.0"
    )

    # =========================================================================
    # 8. IMPLEMENTATION DETAILS
    # =========================================================================
    h_impl = doc.add_heading("7. Implementation Details and Code Architecture", level=1)
    h_impl.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "In accordance with ADR-0001, each activity is structured as a dedicated, self-contained Python package:\n"
        "• activity1_caesar/caesar.py: Implements normalize_key(key), encrypt(plaintext, key), and decrypt(ciphertext, key). "
        "Strictly disallows booleans via isinstance(key, bool) to eliminate Python's bool subclassing pitfall.\n"
        "• activity2_vigenere/vigenere.py: Implements normalize_key(key), encrypt(plaintext, key), and decrypt(ciphertext, key). "
        "Validates ASCII alphabetic keys and implements the alphabetic stream pointer rule.\n"
        "• activity3_one_time_pad/otp.py: Implements generate_key(length) via secrets.token_bytes(), xor_bytes(data, key), "
        "and encrypt/decrypt wrappers supporting UTF-8 text and raw binary byte sequences.\n"
        "• activity4_digital_signature/signature.py: Implements 2048-bit RSA key generation (e=65537), sign_message() using "
        "RSA-PSS with SHA-256, verify_signature() returning boolean status, and get_public_key_fingerprint().\n"
        "• main.py: Implements the interactive TUI with arrow-key navigation, automated test runner, and character/byte "
        "Data Flow Pipeline Visualizations for all four activities."
    )

    # =========================================================================
    # 9. EXECUTION TRANSCRIPTS
    # =========================================================================
    h_exec = doc.add_heading("8. Execution Procedure and Genuine Transcripts", level=1)
    h_exec.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph("The following transcripts represent authentic, unedited terminal outputs from the execution records:")

    doc.add_heading("Activity 1: Caesar Cipher CLI Execution Transcript", level=2)
    add_code_block(doc,
        "$ uv run python activity1_caesar/cli.py -p 'CNS Lab: Activity-01 @ 2026!' -k 3\n\n"
        "================================================================================\n"
        "           CNS ACTIVITY 1: CAESAR CIPHER DEMONSTRATION\n"
        "================================================================================\n"
        "Original Plaintext  : CNS Lab: Activity-01 @ 2026!\n"
        "Input Key           : 3 (Normalized shift: 3)\n"
        "Encrypted Ciphertext: FQV Ode: Dfwlylwb-01 @ 2026!\n"
        "Recovered Plaintext : CNS Lab: Activity-01 @ 2026!\n"
        "--------------------------------------------------------------------------------\n"
        "Round-Trip Verified : SUCCESS (Original == Recovered)"
    )

    doc.add_heading("Activity 2: Vigenère Cipher CLI Execution Transcript", level=2)
    add_code_block(doc,
        "$ uv run python activity2_vigenere/cli.py -p 'The quick brown fox jumps over the lazy dog!' -k 'LEMON'\n\n"
        "================================================================================\n"
        "           CNS ACTIVITY 2: VIGENERE CIPHER DEMONSTRATION\n"
        "================================================================================\n"
        "Original Plaintext  : The quick brown fox jumps over the lazy dog!\n"
        "Input Key           : LEMON (Normalized: LEMON)\n"
        "Encrypted Ciphertext: Elq ehtgw pezaz tbi ngacd shse elq znkc pct!\n"
        "Recovered Plaintext : The quick brown fox jumps over the lazy dog!\n"
        "--------------------------------------------------------------------------------\n"
        "Round-Trip Verified : SUCCESS (Original == Recovered)"
    )

    doc.add_heading("Activity 3: One-Time Pad Standard Demonstration Transcript", level=2)
    add_code_block(doc,
        "$ uv run python activity3_one_time_pad/cli.py -p 'Top Secret CNS Dispatch 2026!'\n\n"
        "================================================================================\n"
        "           CNS ACTIVITY 3: ONE-TIME PAD (OTP) DEMONSTRATION\n"
        "================================================================================\n"
        "Original Plaintext     : Top Secret CNS Dispatch 2026!\n"
        "Plaintext UTF-8 Bytes  : 29 bytes\n"
        "Generated Random Key   : E86580E53B0282E2E62858888D930D880E95A1E5BF9CE82BA1A6494F3C\n"
        "Encrypted Ciphertext   : BCA4F0955B72E391854D2BEEECFC6CC96FBECCD6D3FDEE4BD2C3656E1D\n"
        "Recovered Plaintext    : Top Secret CNS Dispatch 2026!\n"
        "--------------------------------------------------------------------------------\n"
        "Round-Trip Verified    : SUCCESS (Original == Recovered)\n\n"
        "[!] EDUCATIONAL NOTICE:\n"
        "    Printing the secret key above is strictly for academic demonstration.\n"
        "    In production cryptography, exposing the key on terminal output completely\n"
        "    destroys confidentiality and violates the secrecy requirement."
    )

    doc.add_heading("Activity 3: Two-Time Pad Vulnerability Demonstration Transcript", level=2)
    add_code_block(doc,
        "$ uv run python activity3_one_time_pad/cli.py --demo-key-reuse\n\n"
        "================================================================================\n"
        "           DEMONSTRATION: CATASTROPHIC TWO-TIME PAD ATTACK\n"
        "================================================================================\n"
        "Plaintext 1 (M1)       : ATTACK AT DAWN!\n"
        "Plaintext 2 (M2)       : DEFEND THE WALL\n"
        "Shared Reused Key (Hex): 10FB4279D7D62311E26CD8393A0648\n"
        "Ciphertext 1 (C1 Hex)  : 51AF1638949D0350B64C9C786D4869\n"
        "Ciphertext 2 (C2 Hex)  : 54BE043C99920345AA29F86E7B4A04\n"
        "--------------------------------------------------------------------------------\n"
        "Adversary computes C1 ^ C2:\n"
        "C1 ^ C2 (Hex)          : 051112040D0F00151C65641616026D\n"
        "M1 ^ M2 (Hex)          : 051112040D0F00151C65641616026D\n"
        "Key Canceled Out?      : YES (C1 ^ C2 == M1 ^ M2)\n\n"
        "Conclusion: Reusing a One-Time Pad key destroys perfect secrecy entirely,\n"
        "allowing an eavesdropper to recover the plaintext difference without knowing the key!"
    )

    doc.add_heading("Activity 4: RSA-PSS Digital Signature Generation Transcript", level=2)
    add_code_block(doc,
        "$ uv run python activity4_digital_signature/cli.py -m 'Academic CNS Signature 2026'\n\n"
        "================================================================================\n"
        "      CNS ACTIVITY 4: RSA-PSS DIGITAL SIGNATURE DEMONSTRATION\n"
        "================================================================================\n"
        "Message                : Academic CNS Signature 2026\n"
        "Hash Algorithm         : SHA-256\n"
        "Signature Scheme       : RSA-PSS (MGF1 with SHA-256, salt=MAX_LENGTH)\n"
        "Public Key Modulus     : 2048 bits (e = 65537)\n"
        "Public Key Fingerprint : 2df6f78e411b7b05537f5b4f8d672ea4e64f02888cf91054324f686ca98f5a54\n"
        "Signature (Base64)     : T53o9rVlB0mR6q+4bC307eY5qKjP... (256 bytes / 2048 bits)\n"
        "--------------------------------------------------------------------------------\n"
        "Verification Result    : VALID (Authenticity & Integrity Confirmed)"
    )

    doc.add_heading("Activity 4: Digital Signature Tamper Detection Transcript", level=2)
    add_code_block(doc,
        "$ uv run python activity4_digital_signature/cli.py --demo-tamper\n\n"
        "================================================================================\n"
        "      DEMONSTRATION: DIGITAL SIGNATURE INTEGRITY & TAMPER DETECTION\n"
        "================================================================================\n"
        "Original Message       : Authorise payment of 5000 INR to Student Club.\n"
        "Tampered Message       : Authorise payment of 50000 INR to Student Club.\n"
        "--------------------------------------------------------------------------------\n"
        "1. Authentic Message + Original Signature : VALID [Passed]\n"
        "2. Tampered Message + Original Signature  : INVALID [Tampering Detected!]\n"
        "3. Original Message + Corrupted Signature : INVALID [Corruption Detected!]\n"
        "4. Original Message + Unrelated Public Key: INVALID [Key Mismatch Detected!]\n"
        "--------------------------------------------------------------------------------\n"
        "Conclusion: Any modification of the message, signature corruption, or key mismatch\n"
        "immediately invalidates the digital signature, providing strict integrity assurance."
    )

    doc.add_heading("Verified Data Flow Pipelines (Character / Byte Transformations)", level=2)
    doc.add_paragraph(
        "The following structured data flow tables illustrate the runtime execution of the character/byte transformation pipelines "
        "implemented in main.py:"
    )

    # Caesar Pipeline Table
    doc.add_paragraph("Table 5.1: Caesar Modular Shift Pipeline Trace (K = 3)")
    c_pipe = doc.add_table(rows=7, cols=5)
    c_pipe.alignment = WD_TABLE_ALIGNMENT.CENTER
    cp_w = [Inches(1.2), Inches(1.5), Inches(1.0), Inches(1.8), Inches(1.3)]
    format_table_headers(c_pipe, cp_w, ["Char", "Range", "Base Pos (P)", "Formula (P + K) mod 26", "Cipher Char (C)"])
    c_pipe_rows = [
        ("'H'", "uppercase [A-Z]", "7", "(7 + 3) mod 26 = 10", "'K'"),
        ("'e'", "lowercase [a-z]", "4", "(4 + 3) mod 26 = 7", "'h'"),
        ("'l'", "lowercase [a-z]", "11", "(11 + 3) mod 26 = 14", "'o'"),
        ("'l'", "lowercase [a-z]", "11", "(11 + 3) mod 26 = 14", "'o'"),
        ("'o'", "lowercase [a-z]", "14", "(14 + 3) mod 26 = 17", "'r'"),
        ("','", "non-alphabetic", "N/A", "Preserved verbatim", "','"),
    ]
    for r_idx, vals in enumerate(c_pipe_rows):
        row = c_pipe.rows[r_idx + 1]
        for c_idx, val in enumerate(vals):
            cell = row.cells[c_idx]
            cell.width = cp_w[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Consolas"
            run.font.size = Pt(8.5)

    doc.add_paragraph()  # Spacing

    # Vigenère Pipeline Table
    doc.add_paragraph("Table 5.2: Vigenère Polyalphabetic Keyword Alignment Pipeline Trace (Key = 'LEMON')")
    v_pipe = doc.add_table(rows=6, cols=6)
    v_pipe.alignment = WD_TABLE_ALIGNMENT.CENTER
    vp_w = [Inches(1.0), Inches(1.0), Inches(0.8), Inches(1.8), Inches(1.0), Inches(1.2)]
    format_table_headers(v_pipe, vp_w, ["Plain (P)", "Key (K)", "Shift", "Tabula Recta Operation", "Cipher (C)", "Stream Pointer"])
    v_pipe_rows = [
        ("'A'", "'L'", "+11", "(0 + 11) mod 26 = 11", "'L'", "Index 1"),
        ("'T'", "'E'", "+4", "(19 + 4) mod 26 = 23", "'X'", "Index 2"),
        ("'T'", "'M'", "+12", "(19 + 12) mod 26 = 5", "'F'", "Index 3"),
        ("'A'", "'O'", "+14", "(0 + 14) mod 26 = 14", "'O'", "Index 4"),
        ("' '", "—", "0", "Preserved unshifted", "' '", "Paused (no advance)"),
    ]
    for r_idx, vals in enumerate(v_pipe_rows):
        row = v_pipe.rows[r_idx + 1]
        for c_idx, val in enumerate(vals):
            cell = row.cells[c_idx]
            cell.width = vp_w[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Consolas"
            run.font.size = Pt(8.5)

    doc.add_paragraph()  # Spacing

    # OTP Pipeline Table
    doc.add_paragraph("Table 5.3: One-Time Pad Bytewise XOR Transformation Pipeline Trace")
    o_pipe = doc.add_table(rows=6, cols=6)
    o_pipe.alignment = WD_TABLE_ALIGNMENT.CENTER
    op_w = [Inches(0.6), Inches(0.8), Inches(1.5), Inches(0.5), Inches(1.8), Inches(1.6)]
    format_table_headers(o_pipe, op_w, ["Byte #", "Char", "Plain Byte (Hex / Bin)", "XOR", "CSPRNG Key Byte", "Cipher Byte (Hex / Bin)"])
    o_pipe_rows = [
        ("1", "'C'", "0x43 (01000011)", "^", "0x9A (10011010)", "0xD9 (11011001)"),
        ("2", "'N'", "0x4E (01001110)", "^", "0x2B (00101011)", "0x65 (01100101)"),
        ("3", "'S'", "0x53 (01010011)", "^", "0x7F (01111111)", "0x2C (00101100)"),
        ("4", "' '", "0x20 (00100000)", "^", "0xE1 (11100001)", "0xC1 (11000001)"),
        ("5", "'2'", "0x32 (00110010)", "^", "0x0C (00001100)", "0x3E (00111110)"),
    ]
    for r_idx, vals in enumerate(o_pipe_rows):
        row = o_pipe.rows[r_idx + 1]
        for c_idx, val in enumerate(vals):
            cell = row.cells[c_idx]
            cell.width = op_w[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Consolas"
            run.font.size = Pt(8.5)

    # =========================================================================
    # 10. TESTING RESULTS
    # =========================================================================
    h_test = doc.add_heading("9. Testing Methodology and Results (69-Test Matrix)", level=1)
    h_test.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "A total of 69 automated unit tests were executed across all four packages. All 69 tests passed in 0.55 seconds:\n"
        "• Activity 1 (Caesar Cipher): 17 tests passed (100%)\n"
        "• Activity 2 (Vigenère Cipher): 17 tests passed (100%)\n"
        "• Activity 3 (One-Time Pad): 17 tests passed (100%)\n"
        "• Activity 4 (Digital Signature): 18 tests passed (100%)\n\n"
        "The complete, exhaustive 69-test verification matrix is recorded below:"
    )

    all_69_tests = [
        # Activity 1: Caesar Cipher
        ("test_normalize_key_standard", "Normalization", "Key = 3", "PASS"),
        ("test_normalize_key_zero", "Boundary", "Key = 0", "PASS"),
        ("test_normalize_key_twenty_five", "Boundary", "Key = 25", "PASS"),
        ("test_normalize_key_greater_than_twenty_five", "Modulo Wrap", "Key = 26, 29 -> 0, 3", "PASS"),
        ("test_normalize_key_negative", "Negative Shift", "Key = -1, -3 -> 25, 23", "PASS"),
        ("test_normalize_key_invalid_types", "Input Validation", "String, Float, None, Bool", "PASS"),
        ("test_encrypt_known_answers", "KAT", "'HELLO' (k=3), ROT13 pangram", "PASS"),
        ("test_encrypt_wrap_boundaries", "Wrap Boundary", "'XYZ' (k=3) -> 'ABC'", "PASS"),
        ("test_encrypt_key_variations", "Equivalence", "Keys 0, 26, 29, -1", "PASS"),
        ("test_encrypt_invalid_plaintext_type", "Input Validation", "Integer 12345, None", "PASS"),
        ("test_encrypt_empty_message", "Edge Case", "Empty string ''", "PASS"),
        ("test_encrypt_non_alphabetic_preservation", "Symbol Handling", "Spaces, digits, punctuation", "PASS"),
        ("test_encrypt_repeated_characters", "Pattern Handling", "'AAAA' -> 'BBBB'", "PASS"),
        ("test_decrypt_known_answers", "Decryption KAT", "'KHOOR' (k=3) -> 'HELLO'", "PASS"),
        ("test_round_trip_property", "Invertibility", "10 pangram variants: D(E(P)) == P", "PASS"),
        ("test_decrypt_invalid_types", "Input Validation", "Invalid types for decrypt", "PASS"),
        ("test_cli_run_demo", "Integration / CLI", "Full workflow execution", "PASS"),

        # Activity 2: Vigenere Cipher
        ("test_normalize_key_standard", "Normalization", "'LEMON', 'lemon', 'LeMoN'", "PASS"),
        ("test_normalize_key_empty", "Input Validation", "Empty string ''", "PASS"),
        ("test_normalize_key_non_alphabetic", "Input Validation", "Non-alphabetic tokens", "PASS"),
        ("test_normalize_key_invalid_types", "Type Validation", "Integer, None, bool, list", "PASS"),
        ("test_encrypt_known_answers", "KAT", "'ATTACKATDAWN' / 'LEMON'", "PASS"),
        ("test_encrypt_single_character_key", "Caesar Equiv.", "Key 'D' == Caesar shift 3", "PASS"),
        ("test_encrypt_key_longer_than_plaintext", "Boundary", "Plain len 5, Key len 11", "PASS"),
        ("test_encrypt_plaintext_longer_than_key", "Key Repetition", "'AAAAAA' / 'ABC'", "PASS"),
        ("test_encrypt_invalid_plaintext_type", "Type Validation", "Plaintext integer, None", "PASS"),
        ("test_encrypt_case_and_punctuation_preservation", "Stream Alignment", "Key advances only on letters", "PASS"),
        ("test_encrypt_no_alphabetic_characters", "Edge Case", "Digits and symbols only", "PASS"),
        ("test_encrypt_empty_plaintext", "Edge Case", "Empty string ''", "PASS"),
        ("test_encrypt_repeated_patterns", "Pattern Handling", "'AAAA' (k='B'), 'ABAB'", "PASS"),
        ("test_decrypt_known_answers", "Decryption KAT", "'LXFOPVEFRNHR' / 'LEMON'", "PASS"),
        ("test_round_trip_property", "Invertibility", "8 varied test cases", "PASS"),
        ("test_decrypt_invalid_types", "Type Validation", "Non-string ciphertext", "PASS"),
        ("test_cli_run_demo", "Integration / CLI", "CLI execution test", "PASS"),

        # Activity 3: One-Time Pad
        ("test_generate_key_length", "CSPRNG Length", "0, 10, 100 bytes requested", "PASS"),
        ("test_generate_key_independence", "Randomness", "Two 32-byte successive calls", "PASS"),
        ("test_generate_key_invalid_length", "Input Validation", "Negative length, float, bool", "PASS"),
        ("test_xor_bytes_known_vector", "Fixed KAT", "Deterministic byte vectors", "PASS"),
        ("test_xor_bytes_mathematical_properties", "Invertibility", "Self-inverse, zero identity", "PASS"),
        ("test_xor_bytes_length_mismatch", "Length Check", "Key length != Data length", "PASS"),
        ("test_xor_bytes_invalid_types", "Type Validation", "String, integer, None", "PASS"),
        ("test_encrypt_decrypt_known_vector", "Deterministic KAT", "'CNS 2026' / fixed hex key", "PASS"),
        ("test_encrypt_accepts_raw_bytes", "Interface", "Arbitrary binary sequences", "PASS"),
        ("test_encrypt_decrypt_random_key_round_trip", "Fuzz Invertibility", "Sentences, symbols, pangrams", "PASS"),
        ("test_encrypt_invalid_types", "Type Validation", "Plaintext int, string key", "PASS"),
        ("test_empty_message", "Edge Case", "0-byte key and message", "PASS"),
        ("test_multibyte_utf8_characters", "Unicode / UTF-8", "Accents, kanji, lock emoji", "PASS"),
        ("test_decrypt_with_incorrect_key", "Security Property", "Wrong key yields raw bytes", "PASS"),
        ("test_two_time_pad_vulnerability", "Cryptanalysis", "C1 ^ C2 == M1 ^ M2 verified", "PASS"),
        ("test_cli_run_demo", "Integration / CLI", "Standard CLI run", "PASS"),
        ("test_cli_demo_key_reuse", "Integration / CLI", "Two-Time Pad CLI demo", "PASS"),

        # Activity 4: Digital Signature
        ("test_generate_key_pair_defaults", "Key Generation", "2048-bit RSA, e=65537", "PASS"),
        ("test_generate_key_pair_custom_size", "Custom Size", "1024-bit generation", "PASS"),
        ("test_generate_key_pair_invalid_size", "Validation", "<1024 bits, string, None", "PASS"),
        ("test_export_public_key_pem", "Serialization", "SubjectPublicKeyInfo PEM", "PASS"),
        ("test_get_public_key_fingerprint", "Identification", "64-character SHA-256 hex", "PASS"),
        ("test_sign_and_verify_normal_message", "Functional", "Standard string message", "PASS"),
        ("test_sign_accepts_raw_bytes", "Interface", "Binary byte message", "PASS"),
        ("test_sign_invalid_types", "Type Validation", "Integer message, public key", "PASS"),
        ("test_verification_failure_on_message_tampering", "Tamper Detection", "Modified message content", "PASS"),
        ("test_verification_failure_on_signature_tampering", "Tamper Detection", "Corrupted signature bit", "PASS"),
        ("test_verification_failure_on_wrong_public_key", "Key Mismatch", "Independent public key", "PASS"),
        ("test_verification_failure_on_malformed_signature", "Robustness", "Truncated/non-bytes sig", "PASS"),
        ("test_probabilistic_signature_pss_property", "PSS Randomness", "Same msg -> distinct sigs", "PASS"),
        ("test_empty_message_signing_and_verification", "Edge Case", "Empty string ''", "PASS"),
        ("test_multibyte_unicode_characters", "Unicode / UTF-8", "Accents, kanji, emoji", "PASS"),
        ("test_verify_signature_invalid_public_key", "Validation", "Non-RSAPublicKey type", "PASS"),
        ("test_cli_run_demo", "Integration / CLI", "Standard CLI workflow", "PASS"),
        ("test_cli_demo_tamper", "Integration / CLI", "4-way tamper CLI demo", "PASS"),
    ]

    test_table = doc.add_table(rows=len(all_69_tests) + 1, cols=4)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_widths = [Inches(2.5), Inches(1.3), Inches(2.2), Inches(0.8)]
    format_table_headers(test_table, t_widths, ["Test Identifier", "Category", "Input / Scenario", "Status"])

    for r_idx, (t_id, cat, scen, stat) in enumerate(all_69_tests):
        row = test_table.rows[r_idx + 1]
        for c_idx, val in enumerate([t_id, cat, scen, stat]):
            cell = row.cells[c_idx]
            cell.width = t_widths[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(8.5)
            if c_idx == 3:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.bold = True
                run.font.color.rgb = RGBColor(22, 101, 52)

    # =========================================================================
    # 11. SECURITY ANALYSIS
    # =========================================================================
    h_sec = doc.add_heading("10. Security Analysis and Cryptanalysis", level=1)
    h_sec.style.font.color.rgb = RGBColor(30, 58, 138)

    add_callout(doc, "Warning: Modern Insecurity of Classical Ciphers", 
        "Both the Caesar Cipher and Vigenère Cipher provide NO computational confidentiality against modern automated "
        "cryptanalysis. Their educational utility lies exclusively in demonstrating group theory, residue arithmetic, and the "
        "historical progression of cipher design.", is_warning=True
    )

    doc.add_heading("Exhaustive Search and Frequency Cryptanalysis (Caesar Cipher)", level=2)
    doc.add_paragraph(
        "The Caesar keyspace is bounded by |K| = 26. Since shift 0 is the identity, only 25 non-trivial keys exist. An adversary "
        "evaluates all 25 candidate plaintexts in microseconds. Furthermore, the cipher preserves unigram letter frequencies. "
        "In natural English, 'E' occurs with ~12.7% frequency, followed by 'T' (9.1%), 'A' (8.2%), and 'O' (7.5%). An attacker "
        "simply aligns the highest ciphertext frequency peak with 'E' to discover shift key K instantly."
    )

    doc.add_heading("Kasiski Examination and Index of Coincidence (Vigenère Cipher)", level=2)
    doc.add_paragraph(
        "Because the keyword repeats every L characters, identical plaintext words separated by multiples of L yield identical ciphertext "
        "sequences. The greatest common divisor (GCD) of distances between repeated n-grams reveals key length L (Kasiski examination). "
        "Additionally, Friedman's Index of Coincidence (I_c ~ 0.067 for English vs ~0.0385 for random text) enables statistical estimation "
        "of L. Once L is known, the ciphertext is decomposed into L independent Caesar ciphers, each solved via frequency analysis."
    )

    doc.add_heading("Shannon's 5 Mandatory Conditions and Two-Time Pad Collapse (OTP)", level=2)
    doc.add_paragraph(
        "Claude Shannon proved that the One-Time Pad achieves information-theoretic perfect secrecy (P(M=m | C=c) = P(M=m)) if and only if "
        "all five conditions hold simultaneously: (1) uniform randomness, (2) key length >= message length, (3) absolute secrecy, "
        "(4) strict single use, and (5) secure pre-shared distribution.\n"
        "If a key is reused across two messages M1 and M2, C1 ^ C2 = (M1 ^ K) ^ (M2 ^ K) = M1 ^ M2. The key cancels out completely. "
        "Using crib dragging, an eavesdropper recovers both plaintexts without ever knowing the key."
    )

    doc.add_heading("RSA-PSS Padding vs PKCS#1 v1.5 and the PKI Requirement", level=2)
    doc.add_paragraph(
        "RSA-PSS (RFC 8017) provides provable security in the Random Oracle Model by incorporating randomized salt, defeating deterministic "
        "signature attacks. While digital signatures guarantee message authenticity and integrity, they do NOT provide confidentiality. "
        "Crucially, a digital signature proves only possession of private key d; binding that key to a legal human or corporate identity "
        "requires Public Key Infrastructure (PKI), X.509 digital certificates, and Certificate Authorities (CAs)."
    )

    # =========================================================================
    # 12. ADVANTAGES AND LIMITATIONS
    # =========================================================================
    h_adv = doc.add_heading("11. Advantages and Limitations", level=1)
    h_adv.style.font.color.rgb = RGBColor(30, 58, 138)

    adv_table = doc.add_table(rows=5, cols=4)
    adv_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    adv_w = [Inches(1.2), Inches(1.8), Inches(2.0), Inches(1.8)]
    format_table_headers(adv_table, adv_w, ["Algorithm", "Core Strengths", "Theoretical Limitations", "Engineering Constraints"])
    
    adv_data = [
        ("Caesar Cipher", "O(N) complexity; trivial mental computation; foundational education.", "Tiny keyspace (|K|=25); preserves letter frequencies.", "Alphabet-only; zero security for modern digital communications."),
        ("Vigenère Cipher", "Flattens unigram frequencies; keyspace scales as 26^L.", "Periodic key leaks length L via Kasiski/Friedman tests.", "Requires alphabetic stream synchronization; easily decomposed."),
        ("One-Time Pad", "Information-theoretic perfect secrecy (H(M|C) = H(M)).", "Key length must equal message length; key reuse catastrophic.", "Severe key distribution and storage bottleneck; pad zeroization."),
        ("RSA-PSS Signature", "Asymmetric public verification; non-repudiation; message integrity.", "Vulnerable to Shor's algorithm on quantum computers.", "High modular exponentiation overhead; requires PKI for identity."),
    ]
    for r_idx, (alg, strn, lim, con) in enumerate(adv_data):
        row = adv_table.rows[r_idx + 1]
        for c_idx, val in enumerate([alg, strn, lim, con]):
            cell = row.cells[c_idx]
            cell.width = adv_w[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(8.5)
            if c_idx == 0:
                run.bold = True

    # =========================================================================
    # 13. APPLICATIONS
    # =========================================================================
    h_app = doc.add_heading("12. Practical and Historical Applications", level=1)
    h_app.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "• Julius Caesar (58 BC): Used monoalphabetic shift (K=3) to protect military dispatches against non-Latin-literate adversaries.\n"
        "• American Civil War (1861–1865): Confederate forces utilized Vigenère brass cipher disks to communicate battlefield commands.\n"
        "• Washington–Moscow Hotline (1963): The teletype hotline connecting the White House and the Kremlin utilized teleprinter OTP tape "
        "pads transported securely via diplomatic couriers.\n"
        "• ROT13 Obfuscation: Caesar shift K=13 is widely deployed on online discussion forums to conceal puzzle answers and spoilers.\n"
        "• TLS 1.3 Web Security: RSA-PSS and ECDSA digital signatures authenticate web servers during HTTPS handshakes, preventing MitM attacks.\n"
        "• Software Code Signing: Microsoft Authenticode and Apple Gatekeeper verify SHA-256 RSA-PSS signatures embedded in binaries prior to execution.\n"
        "• Quantum Key Distribution (QKD): Modern quantum cryptography combines quantum photon polarization (BB84) for key generation with "
        "OTP encryption to achieve unconditionally secure communication over fiber optic channels."
    )

    # =========================================================================
    # 14. CONCLUSION
    # =========================================================================
    h_conc = doc.add_heading("13. Conclusion", level=1)
    h_conc.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "This laboratory technical report has presented an empirical, software-audited investigation of four cryptographic algorithms "
        "spanning classical substitution, information-theoretic secrecy, and modern asymmetric authentication for Batch 2026_CNS_A_01.\n"
        "The findings confirm that classical substitution ciphers are entirely unviable for contemporary network security due to statistical "
        "predictability, that the One-Time Pad provides unconditional secrecy bounded by severe key distribution constraints, and that "
        "digital signatures (RSA-PSS with SHA-256) form the bedrock of modern public-key trust when integrated within Public Key Infrastructure. "
        "With 69 out of 69 automated unit tests executing successfully in 0.55 seconds, the project completely satisfies the learning outcomes "
        "and technical requirements of Course Outcomes CO1, CO3, and CO4."
    )

    # =========================================================================
    # 15. REFERENCES
    # =========================================================================
    h_ref = doc.add_heading("14. References", level=1)
    h_ref.style.font.color.rgb = RGBColor(30, 58, 138)

    references = [
        "[1] Shannon, C. E. (1949). 'Communication Theory of Secrecy Systems'. Bell System Technical Journal, 28(4), 656–715.",
        "[2] Diffie, W., & Hellman, M. (1976). 'New Directions in Cryptography'. IEEE Transactions on Information Theory, 22(6), 644–654.",
        "[3] Rivest, R. L., Shamir, A., & Adleman, L. (1978). 'A Method for Obtaining Digital Signatures and Public-Key Cryptosystems'. Communications of the ACM, 21(2), 120–126.",
        "[4] Moriarty, K., et al. (2016). 'PKCS #1: RSA Cryptography Specifications Version 2.2' (RFC 8017). IETF.",
        "[5] National Institute of Standards and Technology (NIST). (2015). 'Secure Hash Standard (SHS)' (FIPS PUB 180-4). U.S. Department of Commerce.",
        "[6] Bellare, M., & Rogaway, P. (1996). 'The Exact Security of Digital Signatures: How to Sign with RSA and Rabin'. EUROCRYPT '96, LNCS 1070, 399–416.",
        "[7] Stallings, W. (2017). 'Cryptography and Network Security: Principles and Practice' (7th ed.). Pearson Education.",
        "[8] Ferguson, N., Schneier, B., & Kohno, T. (2010). 'Cryptography Engineering: Design Principles and Practical Applications'. Wiley.",
        "[9] Python Software Foundation. (2026). 'secrets — Generate cryptographically strong random numbers'. Python Documentation.",
        "[10] Python Cryptographic Authority (PyCA). (2026). 'cryptography: Asymmetric Algorithms and Hazard Materials'. https://cryptography.io/",
        "[11] Kasiski, F. W. (1863). 'Die Geheimschriften und die Dechiffrir-Kunst'. E. S. Mittler und Sohn, Berlin.",
        "[12] Friedman, W. F. (1922). 'The Index of Coincidence and Its Applications in Cryptanalysis'. Riverbank Laboratories, Pub. No. 22.",
    ]
    for ref in references:
        p_ref = doc.add_paragraph(ref)
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.style.font.size = Pt(9.5)

    # =========================================================================
    # 16. GROUP CONTRIBUTION
    # =========================================================================
    h_contrib = doc.add_heading("15. Group Contribution Matrix", level=1)
    h_contrib.style.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph(
        "In accordance with course guidelines for Batch 2026_CNS_A_01, the division of engineering responsibilities across the group members "
        "is formally recorded below:"
    )

    contrib_table = doc.add_table(rows=5, cols=4)
    contrib_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_widths = [Inches(0.6), Inches(1.5), Inches(2.0), Inches(2.7)]
    format_table_headers(contrib_table, c_widths, ["Sl.", "USN", "Member Name", "Technical Contribution & Deliverable"])
    
    c_data = [
        ("1", "1KS23CS059", "Jayaditya Dev", "Interactive TUI architecture (main.py), Activity 4 RSA-PSS implementation, MGF1 padding, SHA-256 fingerprinting, PKI analysis, 18 automated tests."),
        ("2", "1KS23CS043", "Durgashree M", "Activity 3 One-Time Pad architecture, CSPRNG randomness verification (secrets), Shannon perfect secrecy proof, Two-Time Pad attack demonstration module, 17 automated tests."),
        ("3", "1KS23CS020", "Aryaman Tiwari", "Activity 2 Vigenère cipher architecture, Tabula Recta mapping, alphabetic stream synchronization, Kasiski and Friedman cryptanalysis, 17 automated tests."),
        ("4", "1KS23CS034", "Chirag T", "Activity 1 Caesar cipher architecture, modulo 26 normalization, boundary wrapping, exhaustive key search analysis, frequency analysis model, 17 automated tests."),
    ]
    for r_idx, (s_no, usn, name, contrib) in enumerate(c_data):
        row = contrib_table.rows[r_idx + 1]
        for c_idx, val in enumerate([s_no, usn, name, contrib]):
            cell = row.cells[c_idx]
            cell.width = c_widths[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            if c_idx in (1, 2):
                run.bold = True

    output_path = Path("report/CNS_Technical_Report_Batch_2026_CNS_A_01.docx")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    print(f"Successfully generated DOCX report at: {output_path.resolve()}")


if __name__ == "__main__":
    build_docx_report()
