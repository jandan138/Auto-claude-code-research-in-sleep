# Dual-Venue Paper Directory Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the Probe-Then-Act paper directory to support dual-venue submission (IEEE T-RL + NeurIPS) with shared core content and venue-specific overrides.

**Architecture:** Shared sections/figures in `paper/shared/` with venue-specific `main.tex` entry points in `paper/venues/{ieee-trl,neurips}/`. Each venue declares explicit relative paths to shared or local files. Build via `latexmk` with `-cd` flag, orchestrated by Makefile.

**Tech Stack:** LaTeX, latexmk, BibTeX, Python 3, bash

**Working Directory:** `/home/zhuzihou/dev/probe-then-act/paper/`

---

## File Map

| File | Status | Responsibility |
|------|--------|---------------|
| `paper/shared/sections/*.tex` | Create (move from `paper/sections/`) | Shared paper sections |
| `paper/shared/figures/*` | Create (move from `paper/figures/`) | Shared figures + gen scripts |
| `paper/shared/math_commands.tex` | Create (move) | Shared math macros |
| `paper/shared/references.bib` | Create (move) | Shared bibliography |
| `paper/shared/venue_macros.tex` | Create | Venue-conditional macro definitions |
| `paper/venues/ieee-trl/main.tex` | Create | IEEE T-RL entry point |
| `paper/venues/ieee-trl/preamble.tex` | Create | IEEE-specific packages + graphicspath |
| `paper/venues/ieee-trl/.latexmkrc` | Create | latexmk config for IEEE build |
| `paper/venues/ieee-trl/sections/*.tex` | Create (copy from shared, then modify) | IEEE-specific section overrides |
| `paper/venues/neurips/main.tex` | Create | NeurIPS entry point |
| `paper/venues/neurips/preamble.tex` | Create | NeurIPS packages + macro shims |
| `paper/venues/neurips/.latexmkrc` | Create | latexmk config for NeurIPS build |
| `paper/venues/neurips/sections/*.tex` | Create (copy from shared, then modify) | NeurIPS-specific section overrides |
| `paper/Makefile` | Create | Build orchestration |
| `paper/scripts/flatten.py` | Create | arXiv/Overleaf flattening |
| `paper/README.md` | Create | Directory guide + build instructions |
| `paper/.gitignore` | Create | Git ignore rules |

---

## Pre-Flight Check

- [ ] **Verify current paper compiles**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
pdflatex -interaction=nonstopmode main.tex
# Expected: main.pdf generated, no fatal errors
ls -la main.pdf
```

- [ ] **Backup current state**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
cp main.pdf main_backup_before_restructure.pdf
git add -A && git commit -m "chore: backup paper state before dual-venue restructure"
# Expected: clean commit on current branch
```

---

## Task 1: Create Directory Skeleton

**Files:**
- Create directories (no files yet)

- [ ] **Step 1: Create all directories**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
mkdir -p shared/{sections,figures}
mkdir -p venues/{ieee-trl,neurips}/{sections,figures,build}
mkdir -p scripts
# Expected: directories exist
ls -R shared venues scripts
```

- [ ] **Step 2: Commit skeleton**

```bash
cd /home/zhuzihou/dev/probe-then-act
git add paper/shared paper/venues paper/scripts
git commit -m "chore: create dual-venue directory skeleton"
```

---

## Task 2: Move Shared Content

**Files:**
- Move: `paper/sections/*.tex` → `paper/shared/sections/`
- Move: `paper/figures/*` → `paper/shared/figures/`
- Move: `paper/math_commands.tex` → `paper/shared/`
- Move: `paper/references.bib` → `paper/shared/`

- [ ] **Step 1: Move sections**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
mv sections/*.tex shared/sections/
rmdir sections  # should be empty now
ls shared/sections/
# Expected: 0_abstract.tex through 7_conclusion.tex
```

- [ ] **Step 2: Move figures and support files**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
mv figures/* shared/figures/
rmdir figures
mv math_commands.tex shared/
mv references.bib shared/
ls shared/
# Expected: sections/, figures/, math_commands.tex, references.bib
```

- [ ] **Step 3: Verify nothing left in old locations**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
ls sections/ 2>/dev/null || echo "sections/ removed (correct)"
ls figures/ 2>/dev/null || echo "figures/ removed (correct)"
ls math_commands.tex 2>/dev/null || echo "math_commands.tex moved (correct)"
ls references.bib 2>/dev/null || echo "references.bib moved (correct)"
```

- [ ] **Step 4: Commit moves**

```bash
cd /home/zhuzihou/dev/probe-then-act
git add -A
git commit -m "chore: move shared content to paper/shared/"
```

---

## Task 3: Create IEEE T-RL Venue Entry Point

**Files:**
- Create: `paper/venues/ieee-trl/preamble.tex`
- Create: `paper/venues/ieee-trl/main.tex`
- Create: `paper/venues/ieee-trl/.latexmkrc`

- [ ] **Step 1: Write IEEE preamble**

Create `paper/venues/ieee-trl/preamble.tex`:

```latex
% IEEE T-RL Preamble
% Venue-specific package configuration

% Math
\usepackage{amsmath,amssymb,amsfonts,amsthm,mathtools}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% Typography
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{nicefrac}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{multirow}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{cite}
\usepackage[capitalize,noabbrev]{cleveref}

% Theorems (continuous numbering)
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}[theorem]{Proposition}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{assumption}[theorem]{Assumption}
\crefname{assumption}{Assumption}{Assumptions}
\Crefname{assumption}{Assumption}{Assumptions}

% Figure paths: shared first, then local overrides
\graphicspath{{../../shared/figures/}{./figures/}}
```

- [ ] **Step 2: Write IEEE main.tex**

Create `paper/venues/ieee-trl/main.tex`:

```latex
% Probe-Then-Act: IEEE T-RL submission
\documentclass[journal]{IEEEtran}

\input{preamble}
\input{../../shared/math_commands}

\title{Probe-Then-Act: Learning Material-Adaptive\\Manipulation through Active Tactile Exploration\\in Multi-Physics Simulation}

\author{Anonymous Authors}

\begin{document}

\maketitle

\begin{abstract}
\input{../../shared/sections/0_abstract}
\end{abstract}

\begin{IEEEkeywords}
robot learning, active perception, material-adaptive manipulation, multi-physics simulation, deformable object manipulation
\end{IEEEkeywords}

\input{sections/1_introduction}
\input{sections/2_related_work}
\input{../../shared/sections/3_method}
\input{../../shared/sections/4_experiments}
\input{sections/5_results}
\input{sections/6_discussion}
\input{../../shared/sections/7_conclusion}

\bibliographystyle{IEEEtran}
\bibliography{../../shared/references}

\end{document}
```

- [ ] **Step 3: Write IEEE .latexmkrc**

Create `paper/venues/ieee-trl/.latexmkrc`:

```perl
$out_dir = 'build';
$pdf_mode = 1;
$bibtex_use = 2;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error';
```

- [ ] **Step 4: Copy current sections as IEEE overrides**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
cp shared/sections/1_introduction.tex venues/ieee-trl/sections/
cp shared/sections/2_related_work.tex venues/ieee-trl/sections/
cp shared/sections/5_results.tex venues/ieee-trl/sections/
cp shared/sections/6_discussion.tex venues/ieee-trl/sections/
ls venues/ieee-trl/sections/
# Expected: 4 section files (the overrides)
```

- [ ] **Step 5: Test IEEE compilation**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper/venues/ieee-trl
latexmk -cd -pdf -outdir=build main.tex
# Expected: builds successfully, main.pdf in build/
ls build/main.pdf
```

- [ ] **Step 6: Commit IEEE venue**

```bash
cd /home/zhuzihou/dev/probe-then-act
git add paper/venues/ieee-trl
git commit -m "feat: create IEEE T-RL venue entry point"
```

---

## Task 4: Create NeurIPS Venue Entry Point

**Files:**
- Create: `paper/venues/neurips/preamble.tex`
- Create: `paper/venues/neurips/main.tex`
- Create: `paper/venues/neurips/.latexmkrc`

- [ ] **Step 1: Copy NeurIPS style file**

```bash
# Copy from ARIS templates
cp /home/zhuzihou/.claude/skills/paper-write/templates/neurips_2025.sty \
   /home/zhuzihou/dev/probe-then-act/paper/venues/neurips/ 2>/dev/null || \
echo "neurips_2025.sty not found - will need to download from neurips.cc"
# If not found, download: wget https://media.neurips.cc/Conferences/NeurIPS2025/neurips_2025.sty
```

- [ ] **Step 2: Write NeurIPS preamble**

Create `paper/venues/neurips/preamble.tex`:

```latex
% NeurIPS Preamble
% Venue-specific package configuration + macro shims

% Note: neurips_2025 template loads hyperref
% Math
\usepackage{amsmath,amssymb,amsfonts,amsthm,mathtools}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% Typography (hyperref already loaded by template)
\usepackage{url}
\usepackage{booktabs}
\usepackage{nicefrac}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{multirow}
\usepackage{algorithm}
\usepackage{algorithmic}

% cleveref must be last (after hyperref and newtheorem)
\usepackage[capitalize,noabbrev]{cleveref}

% Theorems (per-section numbering for NeurIPS article class)
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{assumption}[theorem]{Assumption}
\crefname{assumption}{Assumption}{Assumptions}
\Crefname{assumption}{Assumption}{Assumptions}

% Macro shim: IEEE-specific commands → no-ops
\newcommand{\IEEEPARstart}[2]{#1#2}

% Venue marker for conditional macros
\newcommand{\isneurips}{1}

% Figure paths
\graphicspath{{../../shared/figures/}{./figures/}}
```

- [ ] **Step 3: Write NeurIPS main.tex**

Create `paper/venues/neurips/main.tex`:

```latex
% Probe-Then-Act: NeurIPS submission
\documentclass{article}
\usepackage[preprint]{neurips_2025}

\input{preamble}
\input{../../shared/math_commands}

\title{Probe-Then-Act: Learning Material-Adaptive\\Manipulation through Active Tactile Exploration\\in Multi-Physics Simulation}

\author{%
  Anonymous Author$^1$ \\ \texttt{anonymous@institution.edu}
}

\begin{document}

\maketitle

\begin{abstract}
\input{../../shared/sections/0_abstract}
\end{abstract}

\input{sections/1_introduction}
\input{sections/2_related_work}
\input{../../shared/sections/3_method}
\input{../../shared/sections/4_experiments}
\input{sections/5_results}
\input{../../shared/sections/7_conclusion}

\newpage
\appendix
\input{sections/A_appendix}

\bibliography{../../shared/references}
\bibliographystyle{plainnat}

\end{document}
```

- [ ] **Step 4: Write NeurIPS .latexmkrc**

Create `paper/venues/neurips/.latexmkrc`:

```perl
$out_dir = 'build';
$pdf_mode = 1;
$bibtex_use = 2;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error';
```

- [ ] **Step 5: Create NeurIPS section overrides (initially copies)**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
cp shared/sections/1_introduction.tex venues/neurips/sections/
cp shared/sections/2_related_work.tex venues/neurips/sections/
cp shared/sections/5_results.tex venues/neurips/sections/
# Create empty appendix placeholder
touch venues/neurips/sections/A_appendix.tex
echo "% NeurIPS Appendix - TODO: add appendix content" > venues/neurips/sections/A_appendix.tex
ls venues/neurips/sections/
# Expected: 1_introduction.tex, 2_related_work.tex, 5_results.tex, A_appendix.tex
```

- [ ] **Step 6: Test NeurIPS compilation**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper/venues/neurips
latexmk -cd -pdf -outdir=build main.tex
# Expected: may fail on first run if neurips_2025.sty missing
# If neurips_2025.sty is missing, download it first:
# wget https://media.neurips.cc/Conferences/NeurIPS2025/neurips_2025.sty
ls build/main.pdf
```

- [ ] **Step 7: Commit NeurIPS venue**

```bash
cd /home/zhuzihou/dev/probe-then-act
git add paper/venues/neurips
git commit -m "feat: create NeurIPS venue entry point"
```

---

## Task 5: Create Build System

**Files:**
- Create: `paper/Makefile`

- [ ] **Step 1: Write Makefile**

Create `paper/Makefile`:

```makefile
# Dual-venue LaTeX paper build system
# Usage: make ieee-trl | make neurips | make all | make clean | make check

VENUES := ieee-trl neurips
SHARED_DIR := shared
SHARED_SRCS := $(shell find $(SHARED_DIR) -type f \( -name '*.tex' -o -name '*.pdf' -o -name '*.bib' -o -name '*.py' \) 2>/dev/null)

# Generate build rules for each venue
define VENUE_RULE
$(1)_MAIN := venues/$(1)/main.tex
$(1)_LOCAL := $(shell find venues/$(1) -type f \( -name '*.tex' -o -name '*.sty' -o -name '*.cls' \) 2>/dev/null)
$(1)_PDF := venues/$(1)/build/main.pdf
$(1)_BUILDDIR := venues/$(1)/build

$$($(1)_PDF): $$($(1)_MAIN) $$($(1)_LOCAL) $(SHARED_SRCS) | $$($(1)_BUILDDIR)
	@cd venues/$(1) && latexmk -cd -pdf -outdir=build -interaction=nonstopmode -halt-on-error main.tex

$$($(1)_BUILDDIR):
	@mkdir -p $$@

.PHONY: $(1) clean-$(1)
$(1): $$($(1)_PDF)
	@echo "=== $(1) built: $$($(1)_PDF) ==="

clean-$(1):
	@cd venues/$(1) && latexmk -C -outdir=build 2>/dev/null || true
	@rm -rf $$($(1)_BUILDDIR)

endef

$(foreach v,$(VENUES),$(eval $(call VENUE_RULE,$(v))))

.PHONY: all clean check arxiv
all: $(foreach v,$(VENUES),$(v))

clean: $(foreach v,$(VENUES),clean-$(v))

check:
	@echo "=== IEEE T-RL page count ==="
	@texcount -inc -total venues/ieee-trl/main.tex 2>/dev/null || echo "texcount not installed"
	@echo ""
	@echo "=== NeurIPS page count ==="
	@texcount -inc -total venues/neurips/main.tex 2>/dev/null || echo "texcount not installed"

arxiv:
	@python3 scripts/flatten.py --venue neurips --output arxiv-submission/
```

- [ ] **Step 2: Test Makefile - build IEEE**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
make clean-ieee-trl
make ieee-trl
# Expected: builds successfully
ls venues/ieee-trl/build/main.pdf
```

- [ ] **Step 3: Test Makefile - build NeurIPS**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
make clean-neurips
make neurips
# Expected: builds successfully (if neurips_2025.sty available)
ls venues/neurips/build/main.pdf
```

- [ ] **Step 4: Test Makefile - build all**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
make clean
make all
# Expected: both PDFs built
ls venues/ieee-trl/build/main.pdf venues/neurips/build/main.pdf
```

- [ ] **Step 5: Commit Makefile**

```bash
cd /home/zhuzihou/dev/probe-then-act
git add paper/Makefile
git commit -m "feat: add dual-venue Makefile"
```

---

## Task 6: Create Flatten Script for arXiv

**Files:**
- Create: `paper/scripts/flatten.py`

- [ ] **Step 1: Write flatten.py**

Create `paper/scripts/flatten.py`:

```python
#!/usr/bin/env python3
"""Flatten a dual-venue LaTeX paper for arXiv/Overleaf submission.

Usage:
    python scripts/flatten.py --venue neurips --output arxiv-submission/

Prerequisites:
    1. Build the venue first: make neurips
    2. This generates venues/<venue>/build/main.bbl via latexmk + bibtex
"""

import argparse
import re
import shutil
import sys
from pathlib import Path


def resolve_input_path(input_path: str, base_dir: Path, venues_dir: Path) -> Path | None:
    """Resolve a \input{path} to an actual file."""
    # Try relative to base_dir first
    p = (base_dir / input_path).resolve()
    if p.exists():
        return p
    # Try relative to venues/<venue>/
    p = (venues_dir / input_path).resolve()
    if p.exists():
        return p
    # Try with .tex extension
    for base in [base_dir, venues_dir]:
        p = (base / (input_path + ".tex")).resolve()
        if p.exists():
            return p
    return None


def resolve_figure_path(fig_path: str, base_dir: Path) -> Path | None:
    """Resolve \includegraphics{path} using graphicspath."""
    # Common figure extensions
    extensions = ["", ".pdf", ".png", ".jpg", ".eps"]
    # Try relative to base_dir
    for ext in extensions:
        p = (base_dir / (fig_path + ext)).resolve()
        if p.exists():
            return p
    # Try shared/figures/
    shared_figures = base_dir.parents[1] / "shared" / "figures"
    for ext in extensions:
        p = (shared_figures / (fig_path + ext)).resolve()
        if p.exists():
            return p
    return None


def inline_file(content: str, base_dir: Path, venues_dir: Path, processed: set) -> str:
    """Recursively inline \input{} commands."""
    # Pattern: \input{path} (no extension or with .tex)
    pattern = r"\\input\{([^}]+)\}"

    def replace_input(match):
        input_path = match.group(1)
        resolved = resolve_input_path(input_path, base_dir, venues_dir)
        if resolved is None:
            print(f"Warning: could not resolve \\input{{{input_path}}}", file=sys.stderr)
            return match.group(0)  # Keep original

        resolved = resolved.resolve()
        if resolved in processed:
            return f"% Already inlined: {input_path}\n"
        processed.add(resolved)

        inner_content = resolved.read_text(encoding="utf-8")
        # Recursively process nested inputs
        inner_content = inline_file(inner_content, resolved.parent, venues_dir, processed)
        return f"% --- BEGIN {input_path} ---\n{inner_content}\n% --- END {input_path} ---\n"

    return re.sub(pattern, replace_input, content)


def process_bibliography(content: str, venue_dir: Path) -> str:
    """Replace \bibliography{} with inlined .bbl content."""
    build_dir = venue_dir / "build"
    bbl_file = build_dir / "main.bbl"

    if not bbl_file.exists():
        print(f"Error: {bbl_file} not found. Build the venue first with 'make <venue>'.", file=sys.stderr)
        sys.exit(1)

    bbl_content = bbl_file.read_text(encoding="utf-8")
    # Replace \bibliography{...} and \bibliographystyle{...} with .bbl content
    content = re.sub(r"\\bibliographystyle\{[^}]+\}\n?", "", content)
    content = re.sub(r"\\bibliography\{[^}]+\}\n?", f"\n{bbl_content}\n", content)
    return content


def copy_figures(content: str, output_dir: Path, base_dir: Path) -> str:
    """Copy figures to output dir and rewrite paths."""
    fig_dir = output_dir / "figures"
    fig_dir.mkdir(exist_ok=True)

    pattern = r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}"

    def replace_fig(match):
        fig_path = match.group(1)
        resolved = resolve_figure_path(fig_path, base_dir)
        if resolved is None:
            print(f"Warning: could not resolve figure {fig_path}", file=sys.stderr)
            return match.group(0)

        # Copy to output figures dir
        dest = fig_dir / resolved.name
        shutil.copy2(resolved, dest)
        return match.group(0).replace(fig_path, f"figures/{resolved.name}")

    return re.sub(pattern, replace_fig, content)


def strip_comments(content: str) -> str:
    """Remove LaTeX comments (but not escaped %)."""
    lines = []
    for line in content.split("\n"):
        # Remove comments, but keep \%
        # Simple approach: split on unescaped %
        result = []
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            result.append(line[i])
            i += 1
        cleaned = "".join(result).rstrip()
        if cleaned:
            lines.append(cleaned)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Flatten LaTeX paper for arXiv")
    parser.add_argument("--venue", required=True, choices=["ieee-trl", "neurips"])
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    paper_dir = Path(__file__).parent.parent.resolve()
    venue_dir = paper_dir / "venues" / args.venue
    main_tex = venue_dir / "main.tex"
    output_dir = Path(args.output).resolve()

    if not main_tex.exists():
        print(f"Error: {main_tex} not found", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Read main.tex
    content = main_tex.read_text(encoding="utf-8")

    # Inline all \input{} commands recursively
    content = inline_file(content, venue_dir, venue_dir, set())

    # Process bibliography (inline .bbl)
    content = process_bibliography(content, venue_dir)

    # Copy figures and rewrite paths
    content = copy_figures(content, output_dir, venue_dir)

    # Strip comments
    content = strip_comments(content)

    # Write flattened main.tex
    output_tex = output_dir / "main.tex"
    output_tex.write_text(content, encoding="utf-8")

    print(f"Flattened paper written to: {output_dir}/")
    print(f"  - {output_tex}")
    print(f"  - {output_dir}/figures/")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Make executable and test**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
chmod +x scripts/flatten.py
# Build first to generate .bbl
make neurips
# Then flatten
python3 scripts/flatten.py --venue neurips --output /tmp/test-flatten/
# Expected: /tmp/test-flatten/main.tex and /tmp/test-flatten/figures/*.pdf
ls /tmp/test-flatten/
ls /tmp/test-flatten/figures/ | head -5
```

- [ ] **Step 3: Test flattened compilation**

```bash
cd /tmp/test-flatten
pdflatex -interaction=nonstopmode main.tex
# Expected: compiles without fatal errors (may have warnings)
ls main.pdf
```

- [ ] **Step 4: Commit flatten script**

```bash
cd /home/zhuzihou/dev/probe-then-act
git add paper/scripts/flatten.py
git commit -m "feat: add arXiv flatten script"
```

---

## Task 7: Create Supporting Files

**Files:**
- Create: `paper/shared/venue_macros.tex`
- Create: `paper/.gitignore`
- Create: `paper/README.md`

- [ ] **Step 1: Write venue_macros.tex**

Create `paper/shared/venue_macros.tex`:

```latex
% Venue-conditional macros
% \input by each venue's preamble.tex after setting venue markers

% Abstract length hint (IEEE: 200 words, NeurIPS: 250 words)
\ifdefined\isneurips
  \newcommand{\abstractmaxwords}{250}
\else
  \newcommand{\abstractmaxwords}{200}
\fi

% Section opener shim
\ifdefined\isneurips
  \newcommand{\secstart}[1]{#1}
\else
  \newcommand{\secstart}[1]{\IEEEPARstart{#1}{}}
\fi
```

- [ ] **Step 2: Update both preambles to include venue_macros**

In `paper/venues/ieee-trl/preamble.tex`, add at the end:
```latex
\input{../../shared/venue_macros}
```

In `paper/venues/neurips/preamble.tex`, add after `\newcommand{\isneurips}{1}`:
```latex
\input{../../shared/venue_macros}
```

- [ ] **Step 3: Write .gitignore**

Create `paper/.gitignore`:

```gitignore
# Build artifacts
venues/*/build/
arxiv-submission/

# LaTeX intermediate files
*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
*.toc

# Python
__pycache__/
*.pyc

# OS
.DS_Store
```

- [ ] **Step 4: Write README.md**

Create `paper/README.md`:

```markdown
# Probe-Then-Act Paper

Dual-venue LaTeX paper structure supporting IEEE T-RL and NeurIPS submission.

## Directory Structure

```
paper/
├── shared/               # Cross-venue shared content
│   ├── sections/         # Default sections
│   ├── figures/          # Shared figures + generation scripts
│   ├── math_commands.tex # Shared math macros
│   ├── references.bib    # Shared bibliography
│   └── venue_macros.tex  # Venue-conditional macros
├── venues/
│   ├── ieee-trl/         # IEEE T-RL entry point
│   └── neurips/          # NeurIPS entry point
└── scripts/
    └── flatten.py        # arXiv flattening
```

## Build

```bash
# Build IEEE T-RL version
make ieee-trl

# Build NeurIPS version
make neurips

# Build both
make all

# Clean build artifacts
make clean

# Check page counts
make check
```

## How Overrides Work

Each venue's `main.tex` explicitly declares which files to include:
- `../../shared/sections/X.tex` = shared content
- `sections/X.tex` = venue-specific override

If a venue doesn't need to override a section, it references the shared version.

## Adding a Venue-Specific Section Override

1. Copy from shared: `cp shared/sections/X.tex venues/<venue>/sections/`
2. Modify `venues/<venue>/sections/X.tex`
3. Ensure `venues/<venue>/main.tex` references `sections/X.tex` (not `../../shared/sections/X.tex`)

## arXiv Submission

```bash
make neurips  # Generates .bbl
make arxiv    # Flattens to arxiv-submission/
```

The flattened directory contains a single `main.tex` with all inputs inlined and figures copied.
```

- [ ] **Step 5: Commit supporting files**

```bash
cd /home/zhuzihou/dev/probe-then-act
git add paper/shared/venue_macros.tex paper/.gitignore paper/README.md
git add paper/venues/*/preamble.tex  # Updated preambles
git commit -m "feat: add venue macros, gitignore, and README"
```

---

## Task 8: Final Verification

- [ ] **Step 1: Clean build both venues**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
make clean
make all
# Expected: both PDFs generated
ls -la venues/ieee-trl/build/main.pdf
ls -la venues/neurips/build/main.pdf
```

- [ ] **Step 2: Verify IEEE PDF matches original**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
# Compare page count
pdfinfo venues/ieee-trl/build/main.pdf | grep Pages
pdfinfo main_backup_before_restructure.pdf | grep Pages
# Expected: same page count (or very close)
```

- [ ] **Step 3: Verify NeurIPS PDF is valid**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
pdfinfo venues/neurips/build/main.pdf | grep Pages
# Expected: valid PDF with reasonable page count
```

- [ ] **Step 4: Test flatten script end-to-end**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
make clean-neurips
make neurips
rm -rf arxiv-submission/
python3 scripts/flatten.py --venue neurips --output arxiv-submission/
cd arxiv-submission
pdflatex -interaction=nonstopmode main.tex
# Expected: compiles, main.pdf generated
ls main.pdf
```

- [ ] **Step 5: Final commit**

```bash
cd /home/zhuzihou/dev/probe-then-act
git add -A
git commit -m "feat: dual-venue paper structure complete"
```

---

## Post-Implementation Cleanup

- [ ] **Remove old backup file**

```bash
cd /home/zhuzihou/dev/probe-then-act/paper
rm -f main_backup_before_restructure.pdf
```

- [ ] **Verify git status is clean**

```bash
cd /home/zhuzihou/dev/probe-then-act
git status
# Expected: clean working tree
```

---

## Spec Coverage Check

| Spec Requirement | Task |
|-----------------|------|
| Directory skeleton (shared + venues) | Task 1 |
| Move shared content | Task 2 |
| IEEE T-RL entry point with explicit paths | Task 3 |
| NeurIPS entry point with macro shims | Task 4 |
| Makefile with -cd flag | Task 5 |
| Flatten script for arXiv | Task 6 |
| venue_macros.tex | Task 7 |
| .gitignore | Task 7 |
| README.md | Task 7 |
| Build verification | Task 8 |

---

## Notes for Implementer

1. **NeurIPS style file**: The neurips_2025.sty may need to be downloaded from neurips.cc if not already in the ARIS templates.
2. **Path sensitivity**: All `../../shared/` paths assume the venue `main.tex` is exactly 2 levels below `paper/`. Do not change directory nesting without updating paths.
3. **BibTeX**: The shared `references.bib` must be pre-processed by BibTeX for each venue separately (different .bst files). This is handled by latexmk automatically.
4. **Figure generation**: The `gen_*.py` scripts in `shared/figures/` should still work from that location. If they have hardcoded output paths, update them.
