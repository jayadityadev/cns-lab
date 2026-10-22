"""Cryptography and Network Security (CNS) Laboratory Suite.

Batch No: 2026_CNS_A_01
Interactive Terminal User Interface (TUI) & Unified CLI Entrypoint.
"""

import os
import sys
import subprocess
from pathlib import Path

# Ensure stdout handles UTF-8 properly across diverse console environments
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich import box

# Module imports
from activity1_caesar.cli import main as caesar_cli_main
from activity1_caesar.caesar import encrypt as caesar_encrypt, decrypt as caesar_decrypt, normalize_key as caesar_norm_key

from activity2_vigenere.cli import main as vigenere_cli_main
from activity2_vigenere.vigenere import encrypt as vigenere_encrypt, decrypt as vigenere_decrypt, normalize_key as vigenere_norm_key

from activity3_one_time_pad.cli import main as otp_cli_main, demo_key_reuse as otp_demo_key_reuse
from activity3_one_time_pad.otp import generate_key as otp_generate_key, encrypt as otp_encrypt, decrypt as otp_decrypt

from activity4_digital_signature.cli import main as ds_cli_main, demo_tamper as ds_demo_tamper
from activity4_digital_signature.signature import (
    generate_key_pair as ds_generate_key_pair,
    sign_message as ds_sign_message,
    verify_signature as ds_verify_signature,
    get_public_key_fingerprint as ds_fingerprint,
)

console = Console()

MENU_ITEMS = [
    ("Activity 1: Caesar Cipher", "Classical Monoalphabetic Substitution [CO1]"),
    ("Activity 2: Vigenère Cipher", "Polyalphabetic Tabula Recta Substitution [CO4]"),
    ("Activity 3: One-Time Pad (OTP)", "Information-Theoretic Perfect Secrecy via CSPRNG [CO3]"),
    ("Activity 4: Digital Signature", "RSA-PSS with SHA-256 Authenticity & Integrity [CO3]"),
    ("Run Automated Test Suite", "Execute all 69 automated tests across all activities"),
    ("Exit", "Quit the CNS Laboratory TUI"),
]


def render_caesar_pipeline(plaintext: str, norm_k: int) -> Table:
    """Render character-by-character modular shift data flow pipeline."""
    table = Table(
        title="[bold cyan]Data Flow Pipeline: Modular Shift Mechanics (Character Sample)[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        expand=True,
    )
    table.add_column("Input Char", style="bold white", justify="center")
    table.add_column("Alphabet Range", style="dim", justify="center")
    table.add_column("Base Pos (P)", style="yellow", justify="center")
    table.add_column("Shift (+K)", style="cyan", justify="center")
    table.add_column("Transformation: (P + K) mod 26", style="bright_blue", justify="center")
    table.add_column("Cipher Char (C)", style="bold bright_yellow", justify="center")

    sample_text = plaintext[:8]
    for ch in sample_text:
        if 'a' <= ch <= 'z':
            pos = ord(ch) - ord('a')
            new_pos = (pos + norm_k) % 26
            out_ch = chr(new_pos + ord('a'))
            table.add_row(f"'{ch}'", "lowercase [a-z]", str(pos), f"+{norm_k}", f"({pos} + {norm_k}) % 26 = {new_pos}", f"'{out_ch}'")
        elif 'A' <= ch <= 'Z':
            pos = ord(ch) - ord('A')
            new_pos = (pos + norm_k) % 26
            out_ch = chr(new_pos + ord('A'))
            table.add_row(f"'{ch}'", "uppercase [A-Z]", str(pos), f"+{norm_k}", f"({pos} + {norm_k}) % 26 = {new_pos}", f"'{out_ch}'")
        else:
            table.add_row(f"'{ch}'", "non-alphabetic", "N/A", "0 (bypass)", "Preserved verbatim", f"'{ch}'")

    if len(plaintext) > 8:
        table.add_row("...", "...", "...", "...", "...", "...")
    return table


def render_vigenere_pipeline(plaintext: str, clean_key: str) -> Table:
    """Render polyalphabetic keyword stream alignment data flow pipeline."""
    table = Table(
        title="[bold magenta]Data Flow Pipeline: Polyalphabetic Key Stream Alignment (Sample)[/bold magenta]",
        box=box.ROUNDED,
        border_style="magenta",
        expand=True,
    )
    table.add_column("Plain (P)", style="bold white", justify="center")
    table.add_column("Key (K)", style="bold cyan", justify="center")
    table.add_column("Key Shift", style="cyan", justify="center")
    table.add_column("Tabula Recta Operation", style="bright_blue", justify="center")
    table.add_column("Cipher (C)", style="bold bright_magenta", justify="center")
    table.add_column("Key Stream Pointer", style="dim", justify="center")

    if not clean_key:
        return table

    key_idx = 0
    key_len = len(clean_key)
    sample_text = plaintext[:8]
    for ch in sample_text:
        if ch.isalpha():
            k_char = clean_key[key_idx % key_len]
            shift = ord(k_char) - ord('A')
            base = ord('a') if ch.islower() else ord('A')
            p_pos = ord(ch) - base
            c_pos = (p_pos + shift) % 26
            c_char = chr(c_pos + base)
            table.add_row(f"'{ch}'", f"'{k_char}'", f"+{shift}", f"({p_pos} + {shift}) % 26 = {c_pos}", f"'{c_char}'", f"Advanced to index {key_idx + 1}")
            key_idx += 1
        else:
            table.add_row(f"'{ch}'", "—", "0", "Preserved unshifted", f"'{ch}'", "Paused (no advance)")

    if len(plaintext) > 8:
        table.add_row("...", "...", "...", "...", "...", "...")
    return table


def render_otp_pipeline(plaintext: str, key_bytes: bytes) -> Table:
    """Render bytewise XOR transformation data flow pipeline."""
    msg_bytes = plaintext.encode("utf-8")
    table = Table(
        title="[bold green]Data Flow Pipeline: Bytewise XOR Transformation (Sample)[/bold green]",
        box=box.ROUNDED,
        border_style="green",
        expand=True,
    )
    table.add_column("Byte #", style="dim", justify="center")
    table.add_column("Char", style="bold white", justify="center")
    table.add_column("Plain Byte (Hex / Bin)", style="yellow", justify="center")
    table.add_column("XOR", style="bold cyan", justify="center")
    table.add_column("CSPRNG Key Byte (Hex / Bin)", style="cyan", justify="center")
    table.add_column("Cipher Byte (Hex / Bin)", style="bold bright_green", justify="center")

    sample_len = min(6, len(msg_bytes))
    for i in range(sample_len):
        m_b = msg_bytes[i]
        k_b = key_bytes[i]
        c_b = m_b ^ k_b
        ch_disp = chr(m_b) if 32 <= m_b <= 126 else f"\\x{m_b:02x}"
        table.add_row(
            str(i + 1),
            f"'{ch_disp}'",
            f"0x{m_b:02X} ({m_b:08b})",
            "^",
            f"0x{k_b:02X} ({k_b:08b})",
            f"0x{c_b:02X} ({c_b:08b})",
        )
    if len(msg_bytes) > sample_len:
        table.add_row("...", "...", "...", "^", "...", "...")
    return table


def render_ds_pipeline(message: str, fingerprint: str, signature: bytes) -> Table:
    """Render 5-stage cryptographic digital signature data flow pipeline."""
    import hashlib
    data = message.encode("utf-8")
    sha256_hash = hashlib.sha256(data).hexdigest()

    table = Table(
        title="[bold cyan]Data Flow Pipeline: 5-Stage Asymmetric Signing & Verification[/bold cyan]",
        box=box.ROUNDED,
        border_style="cyan",
        expand=True,
    )
    table.add_column("Pipeline Stage", style="bold yellow", width=14, justify="center")
    table.add_column("Operation", style="bold white", width=26)
    table.add_column("Cryptographic Data Flow & Artifact", style="dim")

    msg_preview = message if len(message) <= 30 else message[:27] + "..."
    table.add_row("Stage 1: Input", "Plaintext Message (M)", f"'{msg_preview}' ({len(data)} bytes UTF-8)")
    table.add_row("Stage 2: Hash", "SHA-256 Digest (h)", f"h = SHA-256(M) = {sha256_hash} (256 bits)")
    table.add_row("Stage 3: Padding", "RSA-PSS Salt Encoding", "Padded with cryptographically secure random salt via MGF1(SHA-256)")
    table.add_row("Stage 4: Signing", "Private Key Exponentiation", f"S = (PSS(h))^d mod n  ──▶  Signature ({len(signature)} bytes / 2048 bits)")
    table.add_row("Stage 5: Verify", "Public Key Verification", f"S^e mod n matches SHA-256(M) using Public Key (FP: {fingerprint[:16]}...)")
    return table



def wait_for_key():
    """Wait for user to press any key before returning."""
    console.print("\n[dim cyan]Press any key to return to menu...[/dim cyan]", end="")
    try:
        if sys.platform == "win32":
            import msvcrt
            msvcrt.getch()
        else:
            input()
    except Exception:
        input()


def render_header() -> Panel:
    """Render sleek top banner."""
    header_text = Text()
    header_text.append("CRYPTOGRAPHY AND NETWORK SECURITY (CNS)\n", style="bold cyan")
    header_text.append("Academic Laboratory Activity Suite  •  Batch: ", style="bold white")
    header_text.append("2026_CNS_A_01\n", style="bold yellow")
    header_text.append("Group: Jayaditya Dev  •  Durgashree M  •  Aryaman Tiwari  •  Chirag T", style="dim white")
    return Panel(header_text, box=box.ROUNDED, style="cyan", border_style="cyan")


def render_menu(selected_idx: int) -> Table:
    """Render interactive navigation menu table."""
    table = Table(box=box.ROUNDED, border_style="bright_blue", expand=True)
    table.add_column("No.", style="bold cyan", width=4, justify="center")
    table.add_column("Activity / Action", style="bold white", width=34)
    table.add_column("Theoretical Scope & Topic", style="dim")

    for idx, (title, desc) in enumerate(MENU_ITEMS):
        num_str = f"{idx + 1}"
        if idx == selected_idx:
            prefix = "▶ "
            row_style = "bold white on blue"
            table.add_row(f"{prefix}{num_str}", title, desc, style=row_style)
        else:
            table.add_row(f"  {num_str}", title, desc)

    return table


def run_activity1_tui():
    """TUI runner for Caesar Cipher."""
    console.clear()
    console.print(render_header())
    console.print(Panel("[bold cyan]ACTIVITY 1: CAESAR CIPHER DEMONSTRATION[/bold cyan]", box=box.ROUNDED))
    
    plaintext = Prompt.ask("[bold green]Enter plaintext message[/bold green]", default="CNS Activity 1: Caesar Cipher")
    while True:
        key_str = Prompt.ask("[bold green]Enter integer shift key[/bold green]", default="3")
        try:
            key = int(key_str)
            break
        except ValueError:
            console.print("[red]Invalid key: Must be an integer.[/red]")

    norm_k = caesar_norm_key(key)
    ciphertext = caesar_encrypt(plaintext, key)
    recovered = caesar_decrypt(ciphertext, key)

    res_table = Table(box=box.ROUNDED, border_style="cyan", expand=True)
    res_table.add_column("Property", style="bold yellow", width=22)
    res_table.add_column("Value", style="bold white")

    res_table.add_row("Original Plaintext", plaintext)
    res_table.add_row("Shift Key", f"{key} (Normalized: {norm_k})")
    res_table.add_row("Ciphertext", f"[bright_yellow]{ciphertext}[/bright_yellow]")
    res_table.add_row("Recovered Plaintext", recovered)
    res_table.add_row("Round-Trip Status", "[bold green]VERIFIED (Original == Recovered)[/bold green]" if plaintext == recovered else "[bold red]FAILED[/bold red]")

    console.print("\n", res_table)
    console.print("\n", render_caesar_pipeline(plaintext, norm_k))
    console.print(Panel(
        "[bold yellow]Academic Security Analysis:[/bold yellow]\n"
        "• Keyspace: Only 25 non-trivial keys (|K| = 26). Vulnerable to instantaneous brute-force search.\n"
        "• Frequency Analysis: Preserves natural language unigram frequencies, trivially broken via letter counting.\n"
        "• Modern Status: [bold red]Completely Insecure[/bold red] for modern communications.",
        title="Cryptanalysis Summary",
        border_style="yellow",
        box=box.ROUNDED,
    ))
    wait_for_key()


def run_activity2_tui():
    """TUI runner for Vigenère Cipher."""
    console.clear()
    console.print(render_header())
    console.print(Panel("[bold cyan]ACTIVITY 2: VIGENÈRE CIPHER DEMONSTRATION[/bold cyan]", box=box.ROUNDED))
    
    plaintext = Prompt.ask("[bold green]Enter plaintext message[/bold green]", default="ATTACK AT DAWN!")
    while True:
        key = Prompt.ask("[bold green]Enter alphabetic keyword[/bold green]", default="LEMON")
        try:
            clean_k = vigenere_norm_key(key)
            break
        except (ValueError, TypeError) as err:
            console.print(f"[red]Invalid key: {err}[/red]")

    ciphertext = vigenere_encrypt(plaintext, key)
    recovered = vigenere_decrypt(ciphertext, key)

    res_table = Table(box=box.ROUNDED, border_style="magenta", expand=True)
    res_table.add_column("Property", style="bold yellow", width=22)
    res_table.add_column("Value", style="bold white")

    res_table.add_row("Original Plaintext", plaintext)
    res_table.add_row("Keyword", f"{key} (Normalized: {clean_k})")
    res_table.add_row("Ciphertext", f"[bright_magenta]{ciphertext}[/bright_magenta]")
    res_table.add_row("Recovered Plaintext", recovered)
    res_table.add_row("Round-Trip Status", "[bold green]VERIFIED (Original == Recovered)[/bold green]" if plaintext == recovered else "[bold red]FAILED[/bold red]")

    console.print("\n", res_table)
    console.print("\n", render_vigenere_pipeline(plaintext, clean_k))
    console.print(Panel(
        "[bold magenta]Polyalphabetic Security Analysis:[/bold magenta]\n"
        "• Tabula Recta: Cycles through multiple Caesar shifts, flattening single-letter frequency spikes.\n"
        "• Kasiski Examination: Periodic key repetition creates identical ciphertext for identical n-grams, exposing key length L.\n"
        "• Friedman Test (Index of Coincidence): Allows statistical deduction of key length L from ciphertext coincidence.\n"
        "• Decomposition: Once L is found, reduces to L independent monoalphabetic Caesar ciphers.\n"
        "• Modern Status: [bold red]Completely Insecure[/bold red] for modern communications.",
        title="Cryptanalysis Summary",
        border_style="magenta",
        box=box.ROUNDED,
    ))
    wait_for_key()


def run_activity3_tui():
    """TUI runner for One-Time Pad."""
    console.clear()
    console.print(render_header())
    console.print(Panel("[bold cyan]ACTIVITY 3: ONE-TIME PAD (OTP) DEMONSTRATION[/bold cyan]", box=box.ROUNDED))

    choice = Prompt.ask(
        "[bold green]Select mode[/bold green]: [1] Standard CSPRNG Demonstration  [2] Demonstrate Two-Time Pad Attack",
        choices=["1", "2"],
        default="1",
    )

    if choice == "2":
        otp_demo_key_reuse()
        wait_for_key()
        return

    plaintext = Prompt.ask("[bold green]Enter plaintext message[/bold green]", default="Top Secret CNS Dispatch 2026!")
    msg_bytes = plaintext.encode("utf-8")
    key_bytes = otp_generate_key(len(msg_bytes))
    ciphertext = otp_encrypt(msg_bytes, key_bytes)
    decoded, _ = otp_decrypt(ciphertext, key_bytes)

    res_table = Table(box=box.ROUNDED, border_style="green", expand=True)
    res_table.add_column("Property", style="bold yellow", width=22)
    res_table.add_column("Value", style="bold white")

    res_table.add_row("Original Plaintext", plaintext)
    res_table.add_row("Message Bytes", f"{len(msg_bytes)} bytes")
    res_table.add_row("CSPRNG Random Key", f"[cyan]{key_bytes.hex().upper()}[/cyan]")
    res_table.add_row("Ciphertext (Hex)", f"[bright_green]{ciphertext.hex().upper()}[/bright_green]")
    res_table.add_row("Recovered Plaintext", decoded if decoded else "[red]Decoding Failed[/red]")
    res_table.add_row("Round-Trip Status", "[bold green]VERIFIED (Original == Recovered)[/bold green]" if decoded == plaintext else "[bold red]FAILED[/bold red]")

    console.print("\n", res_table)
    console.print("\n", render_otp_pipeline(plaintext, key_bytes))
    console.print(Panel(
        "[bold green]Shannon's Perfect Secrecy Analysis:[/bold green]\n"
        "• Information-Theoretic Secrecy: P(M=m | C=c) = P(M=m). Ciphertext reveals ZERO information to adversaries.\n"
        "• 5 Mandatory Conditions: (1) Uniform randomness, (2) Key length >= message, (3) Absolute secrecy,\n"
        "  (4) Strict single use (never reused), (5) Secure pre-shared pad distribution.\n"
        "• Educational Notice: [yellow]Key printed above strictly for academic instruction; exposing keys in production invalidates secrecy.[/yellow]",
        title="Information-Theoretic Security Summary",
        border_style="green",
        box=box.ROUNDED,
    ))
    wait_for_key()


def run_activity4_tui():
    """TUI runner for Digital Signature."""
    console.clear()
    console.print(render_header())
    console.print(Panel("[bold cyan]ACTIVITY 4: DIGITAL SIGNATURE DEMONSTRATION[/bold cyan]", box=box.ROUNDED))

    choice = Prompt.ask(
        "[bold green]Select mode[/bold green]: [1] Sign & Verify Message  [2] Run Tamper & Fraud Detection Demo",
        choices=["1", "2"],
        default="1",
    )

    if choice == "2":
        ds_demo_tamper()
        wait_for_key()
        return

    message = Prompt.ask("[bold green]Enter message to digitally sign[/bold green]", default="Academic CNS Signature 2026")
    with console.status("[bold cyan]Generating 2048-bit RSA key pair & signing...[/bold cyan]"):
        private_key, public_key = ds_generate_key_pair(2048)
        sig = ds_sign_message(message, private_key)
        is_valid = ds_verify_signature(message, sig, public_key)
        fp = ds_fingerprint(public_key)

    import base64
    sig_b64 = base64.b64encode(sig).decode("ascii")

    res_table = Table(box=box.ROUNDED, border_style="cyan", expand=True)
    res_table.add_column("Property", style="bold yellow", width=22)
    res_table.add_column("Value", style="bold white")

    res_table.add_row("Message Content", message)
    res_table.add_row("Signature Algorithm", "RSA-PSS (SHA-256 with MGF1, salt=MAX_LENGTH)")
    res_table.add_row("Public Key Modulus", "2048 bits (e = 65537)")
    res_table.add_row("Public Key Fingerprint", f"[cyan]{fp}[/cyan]")
    res_table.add_row("Signature (Base64)", f"[dim]{sig_b64[:60]}... ({len(sig)} bytes)[/dim]")
    res_table.add_row("Verification Result", "[bold green]VALID (Authenticity & Integrity Confirmed)[/bold green]" if is_valid else "[bold red]INVALID[/bold red]")

    console.print("\n", res_table)
    console.print("\n", render_ds_pipeline(message, fp, sig))
    console.print(Panel(
        "[bold cyan]Asymmetric Security Properties:[/bold cyan]\n"
        "• Authenticity: Confirms message originated from the holder of the corresponding private key.\n"
        "• Integrity: Modifying even one bit of the message or signature invalidates verification.\n"
        "• Non-Repudiation: Signer cannot plausibly deny signing the message if the private key was secured.\n"
        "• Signature vs Encryption: [yellow]Signatures do NOT conceal plaintext. Encryption is required for confidentiality.[/yellow]\n"
        "• PKI Requirement: Public keys prove key possession, not physical identity; identity requires trusted CAs/PKI.",
        title="Digital Signature Security Summary",
        border_style="cyan",
        box=box.ROUNDED,
    ))
    wait_for_key()


def run_full_test_suite_tui():
    """Execute the automated test suite within the TUI."""
    console.clear()
    console.print(render_header())
    console.print(Panel("[bold cyan]EXECUTING AUTOMATED TEST SUITE (ALL 4 ACTIVITIES)[/bold cyan]", box=box.ROUNDED))
    
    with console.status("[bold green]Running pytest across all test suites...[/bold green]"):
        res = subprocess.run(
            ["uv", "run", "pytest", "-v"],
            capture_output=True,
            text=True,
        )

    lines = res.stdout.strip().splitlines()
    summary_line = lines[-1] if lines else "No output"
    
    table = Table(box=box.ROUNDED, border_style="green" if res.returncode == 0 else "red", expand=True)
    table.add_column("Activity Test Suite", style="bold white")
    table.add_column("Status", justify="right")

    for line in lines:
        if "::" in line:
            parts = line.split("::")
            test_name = parts[-1].split()[0]
            status = line.split()[-2]
            suite = parts[0]
            style = "green" if "PASSED" in status else "red"
            table.add_row(f"{suite}::{test_name}", f"[{style}]{status}[/{style}]")

    console.print(table)
    status_style = "bold green" if res.returncode == 0 else "bold red"
    console.print(Panel(f"[{status_style}]{summary_line}[/{status_style}]", box=box.ROUNDED))
    wait_for_key()


def interactive_tui():
    """Main interactive TUI loop with arrow key selection."""
    selected_idx = 0
    total_items = len(MENU_ITEMS)

    # Use msvcrt on Windows for interactive arrow keys if available and stdout is a terminal
    is_interactive = sys.platform == "win32" and sys.stdin.isatty()

    if is_interactive:
        import msvcrt

        while True:
            console.clear()
            console.print(render_header())
            console.print(render_menu(selected_idx))
            console.print("[dim cyan]Navigation: Use [bold]↑ / ↓[/bold] arrow keys to move, [bold]Enter[/bold] to select, [bold]1-6[/bold] for direct jump, [bold]q[/bold] to quit.[/dim cyan]")

            key = msvcrt.getch()

            if key in (b"\x00", b"\xe0"):  # Special key prefix (arrows, function keys)
                arrow = msvcrt.getch()
                if arrow == b"H":  # Up arrow
                    selected_idx = (selected_idx - 1) % total_items
                elif arrow == b"P":  # Down arrow
                    selected_idx = (selected_idx + 1) % total_items
            elif key in (b"\r", b"\n"):  # Enter key
                if selected_idx == 0:
                    run_activity1_tui()
                elif selected_idx == 1:
                    run_activity2_tui()
                elif selected_idx == 2:
                    run_activity3_tui()
                elif selected_idx == 3:
                    run_activity4_tui()
                elif selected_idx == 4:
                    run_full_test_suite_tui()
                elif selected_idx == 5:
                    console.print("\n[bold cyan]Exiting CNS Laboratory Suite. Goodbye![/bold cyan]")
                    sys.exit(0)
            elif key in (b"q", b"Q", b"\x1b"):  # q or Esc key
                console.print("\n[bold cyan]Exiting CNS Laboratory Suite. Goodbye![/bold cyan]")
                sys.exit(0)
            elif key in (b"1", b"2", b"3", b"4", b"5", b"6"):
                choice_num = int(key.decode("ascii")) - 1
                selected_idx = choice_num
                if selected_idx == 0:
                    run_activity1_tui()
                elif selected_idx == 1:
                    run_activity2_tui()
                elif selected_idx == 2:
                    run_activity3_tui()
                elif selected_idx == 3:
                    run_activity4_tui()
                elif selected_idx == 4:
                    run_full_test_suite_tui()
                elif selected_idx == 5:
                    console.print("\n[bold cyan]Exiting CNS Laboratory Suite. Goodbye![/bold cyan]")
                    sys.exit(0)
    else:
        # Fallback for non-interactive / non-Windows environments
        while True:
            console.clear()
            console.print(render_header())
            console.print(render_menu(selected_idx))
            
            choice = Prompt.ask("\nSelect option [1-6/q]", default="1").strip().lower()
            if choice == "1":
                run_activity1_tui()
            elif choice == "2":
                run_activity2_tui()
            elif choice == "3":
                run_activity3_tui()
            elif choice == "4":
                run_activity4_tui()
            elif choice == "5":
                run_full_test_suite_tui()
            elif choice in ("6", "q", "quit", "exit"):
                console.print("\n[bold cyan]Exiting CNS Laboratory Suite. Goodbye![/bold cyan]")
                sys.exit(0)


def main():
    """Entry point dispatching either non-interactive CLI args or launching the interactive TUI."""
    args = sys.argv[1:]

    # Headless CLI argument dispatching
    if args and args[0].lower() in ("activity1", "caesar", "1"):
        sys.argv = [sys.argv[0]] + args[1:]
        caesar_cli_main()
        return

    if args and args[0].lower() in ("activity2", "vigenere", "2"):
        sys.argv = [sys.argv[0]] + args[1:]
        vigenere_cli_main()
        return

    if args and args[0].lower() in ("activity3", "otp", "3"):
        sys.argv = [sys.argv[0]] + args[1:]
        otp_cli_main()
        return

    if args and args[0].lower() in ("activity4", "signature", "ds", "4"):
        sys.argv = [sys.argv[0]] + args[1:]
        ds_cli_main()
        return

    if args and args[0] in ("-h", "--help"):
        console.print("[bold cyan]CNS Laboratory Suite - CLI Usage:[/bold cyan]")
        console.print("  [green]uv run main.py[/green]                          : Launch interactive TUI")
        console.print("  [green]uv run main.py activity1[/green] [args...]      : Execute Activity 1 (Caesar Cipher)")
        console.print("  [green]uv run main.py activity2[/green] [args...]      : Execute Activity 2 (Vigenère Cipher)")
        console.print("  [green]uv run main.py activity3[/green] [args...]      : Execute Activity 3 (One-Time Pad)")
        console.print("  [green]uv run main.py activity4[/green] [args...]      : Execute Activity 4 (Digital Signature)")
        return

    # No CLI arguments: launch the interactive TUI
    interactive_tui()


if __name__ == "__main__":
    main()
