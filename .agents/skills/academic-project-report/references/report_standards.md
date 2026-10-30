# Academic Report Quality Standards & Formatting Invariants

This reference document outlines the strict academic formatting standards, layout rules, and quality invariants established through the peer-review and faculty audit of university-grade engineering technical reports (specifically adhering to VTU / KSIT guidelines).

---

## 1. Page Geometry & Typography

| Parameter | Specification | Purpose / Standard |
| :--- | :--- | :--- |
| **Paper Size** | A4 (`a4paper`) | Standard university submission format |
| **Margins** | `left=0.85in, right=0.85in, top=0.9in, bottom=0.9in` | Balanced printable area for binding and presentation |
| **Base Font** | Times New Roman (`mathptmx`) at 12pt | Academic standard for VTU/IEEE documentation |
| **Line Spacing** | 1.5 spacing (`\usepackage{setspace}\onehalfspacing`) | Standard reading spacing required by university rubrics |
| **Paragraph Break** | `\emergencystretch{2em}` | Avoids hyphenation clipping on right margin |

### Monospace Identifier Protection
Always include the following definition in the LaTeX preamble:
```latex
\renewcommand{\texttt}[1]{{\normalfont #1}}
```
**Why this matters**: In default LaTeX, `\texttt` uses Computer Modern Typewriter font which does not hyphenate or wrap well within narrow columns. Long filenames (e.g. `activity_1_caesar/caesar.py`) or class names spill outside the 0.85" margin. Overriding `\texttt` to use the normal Times New Roman serif font prevents margin overflow completely.

---

## 2. Header and Footer Rules

- **Institutional Colors**: Primary brand color is maroon (`\definecolor{ksitmaroon}{RGB}{128, 0, 0}`).
- **Running Rules**: Top header rule and bottom footer rule of thickness `1.8pt` in institutional maroon.
- **Header Left**: Bold project title (`\textbf{\fontsize{10}{12}\selectfont Implementation and Analysis of ...}`).
- **Footer Left**: Department and College affiliation (`\fontsize{10}{12}\selectfont Dept. of CSE, K.S. Institute of Technology`).
- **Footer Right**: Page number (`\fontsize{10}{12}\selectfont Page \thepage`).

> [!IMPORTANT]
> **PAGINATION & RULE ACTIVATION INVARIANT**:
> - Preliminary pages (Title Page, Abstract, Table of Contents, List of Figures, List of Tables) must use Roman numerals (`\pagenumbering{roman}`) and pagestyle `preliminary` (**zero header rules, zero footer rules**).
> - Running maroon header and footer rules activate **strictly on Chapter 1 (page 1, Arabic numbering)** where `\pagenumbering{arabic}` is called.

---

## 3. Preliminary Pages & Grid Tables

All preliminary indices must use boxed grid tables with light gray headers (`#F0F0F0`):

### Table of Contents Grid Format
```latex
\begin{table}[h!]
\centering
\fontsize{10.5}{13.5}\selectfont
\begin{tabular}{|c|p{4.7in}|c|}
\hline
\rowcolor{tableheader}
\textbf{Chapter No.} & \multicolumn{1}{c|}{\textbf{Title}} & \textbf{Page No.} \\
\hline
& \textbf{ABSTRACT} & \textbf{i} \\
\hline
\textbf{1.} & \textbf{INTRODUCTION AND OBJECTIVES} & \textbf{1} \\
...
\end{tabular}
\end{table}
```

- Apply identical grid table formatting to **List of Figures** and **List of Tables**.

---

## 4. Flowcharts & Architectural Diagrams (TikZ Standards)

- **Vector Rendering**: All process flowcharts and architectural pipelines must be drawn using native TikZ vector graphics (`\begin{tikzpicture}`).
- **Separation of Pipelines**: Never merge two distinct algorithmic pipelines onto the same page if it causes node overlap or cramped decision trees.
- **Page Layout**: When starting a flowchart section:
  1. Add an introductory narrative paragraph detailing the data transformations, state changes, and error paths.
  2. Center the TikZ diagram directly underneath.
  3. Ensure at least `0.30cm` to `0.40cm` vertical spacing between nodes.
  4. Label all decision branches clearly (`Yes`, `No`).

```latex
\begin{figure}[h!]
\centering
\begin{tikzpicture}[node distance=1.1cm, auto]
    \node [flowblock, fill=ksitmaroon!12] (title) {\textbf{Activity Pipeline: Algorithm Name}};
    \node [processblock, below=0.35cm of title] (input) {Input Message $M$, Key $K$};
    \node [decisionblock, below=0.50cm of input] (check) {Is Key Valid?};
    \node [processblock, below=0.60cm of check] (transform) {Execute Transformation};
    \node [processblock, right=1.2cm of check] (error) {Raise ValueError};

    \draw [line] (title) -- (input);
    \draw [line] (input) -- (check);
    \draw [line] (check) -- node [right, font=\scriptsize] {Yes} (transform);
    \draw [line] (check) -- node [above, font=\scriptsize] {No} (error);
\end{tikzpicture}
\caption{Architectural Pipeline Flowchart for Algorithm}
\end{figure}
```

---

## 5. Code Listings & Dedicated Pages (Chapter 4)

- **One Dedicated Page Per Major Algorithm**: In Chapter 4, provide a dedicated page for each primary algorithm.
- **Composition**:
  - Top: Subheading and theoretical summary of the method.
  - Middle: High-resolution code snippet image or styled `listings` block.
  - Bottom: In-depth commentary explaining line-by-line mechanics, modular arithmetic, edge-case handling, and cryptographic principles.
- **Eliminate Empty Space**: If an image leaves vertical blank space, supplement with a character/byte data flow trace table or algorithmic invariant description.

---

## 6. Runtime Demonstrations & Execution Screenshots (Chapter 5)

- Every implemented activity must have verified runtime evidence in Chapter 5.
- Provide clear callouts and captions explaining:
  - Input arguments provided.
  - Runtime execution steps and verification logs.
  - Proof of invertibility or edge-case handling (e.g. tamper detection).
- Placeholders generated via `create_placeholders.py` should be used during initial scaffolding and replaced with actual terminal captures.

---

## 7. Testing & Verification Matrix (Chapter 6)

- Present automated test results in an exhaustive tabular matrix:
  - Columns: `Test ID`, `Target Module`, `Test Category` (KAT, Edge Wrapping, Tamper Detection, Invertibility), `Sample Input`, `Expected Result`, `Pass/Fail`.
- Include total test count, total execution time, and pass rate (e.g. *69 of 69 tests passed in 0.55s*).

---

## 8. Tone, Terminology & Prohibited Jargon

- **Academic Tone**: Write with rigorous technical depth, mathematical formalism, and empirical clarity.
- **Prohibited Software Engineering Jargon**:
  - Do NOT reference internal meta-development concepts like *"Architecture Decision Records (ADRs)"*, *"git branch strategies"*, *"sprint backlog tickets"*, or *"scrum ceremonies"* in college technical reports.
  - Replace them with academic equivalents: *"Architectural Design Rationale"*, *"Modular Repository Organization"*, and *"System Specifications"*.

---

## 9. End Matter Standards

- **References**: Numbered IEEE citation format (`[1]`, `[2]`).
- **Group Contribution Matrix**: Explicit table documenting each team member's name, USN, and deliverable ownership.
- **Final Project Presentation Photograph**:
  - Must occupy the **final page** of the document.
  - Display the official project defense / presentation photograph with institutional caption.
  - Do NOT duplicate student detail tables on this photo page.
