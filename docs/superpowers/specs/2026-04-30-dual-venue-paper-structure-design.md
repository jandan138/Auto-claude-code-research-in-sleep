# Dual-Venue Paper Directory Structure Design

**Date**: 2026-04-30  
**Project**: Probe-Then-Act T-RL / NeurIPS Paper  
**Status**: Design approved, ready for implementation  

## Problem Statement

The Probe-Then-Act paper currently targets IEEE T-RL but may also be submitted to NeurIPS. The two venues require:
- Different LaTeX document classes (IEEEtran vs article+neurips_2025)
- Different content framing (robotics vs machine learning)
- Potentially different section organization
- Different bibliography styles (IEEEtran.bst vs plainnat)

The current flat `paper/` structure cannot support both venues without manual duplication.

## Design Decisions

### 1. Architecture: Shared Core + Venue Overlay

Use a shared core of sections/figures with venue-specific override directories. Unlike the initially proposed TEXINPUTS overlay (rejected by multi-agent review as fragile), this design uses **explicit relative paths** in each venue's `main.tex`.

### 2. Path Resolution: Explicit Relative Paths

Each venue's `main.tex` directly declares which files it includes:
- `../../shared/sections/X.tex` for shared content
- `sections/X.tex` for venue-specific overrides

This is explicit, debuggable, and works on Overleaf/arXiv without environment variables.

### 3. Build System: latexmk + Makefile

Use `latexmk` with the `-cd` flag from each venue directory. Makefile uses `$(shell find ...)` for dependency tracking instead of `$(wildcard)`.

---

## Directory Structure

```
probe-then-act/paper/
├── shared/                          # Cross-venue shared content
│   ├── sections/
│   │   ├── 0_abstract.tex
│   │   ├── 3_method.tex
│   │   ├── 4_experiments.tex
│   │   └── 7_conclusion.tex
│   ├── figures/
│   │   ├── fig2_main_comparison.pdf
│   │   ├── fig3_ablation.pdf
│   │   ├── fig4_seed_distribution.pdf
│   │   ├── TABLE_1_main_results.tex
│   │   ├── TABLE_2_ablation.tex
│   │   ├── TABLE_3_benchmark.tex
│   │   ├── gen_fig1_hero.py
│   │   ├── gen_fig2_main_comparison.py
│   │   ├── gen_fig3_ablation.py
│   │   ├── gen_fig4_seed_distribution.py
│   │   ├── gen_fig5_scene_schematic.py
│   │   ├── gen_tables.py
│   │   ├── paper_plot_style.py
│   │   └── genesis_renders/
│   ├── math_commands.tex
│   └── references.bib
│
├── venues/                          # Venue-specific content
│   ├── ieee-trl/
│   │   ├── main.tex                 # IEEEtran[journal] template
│   │   ├── preamble.tex             # Package loads, theorem defs, graphicspath
│   │   ├── sections/                # Override layer (only differing sections)
│   │   │   ├── 1_introduction.tex
│   │   │   ├── 2_related_work.tex
│   │   │   ├── 5_results.tex
│   │   │   └── 6_discussion.tex
│   │   └── build/                   # Build artifacts (gitignored)
│   │
│   └── neurips/
│       ├── main.tex                 # \usepackage[preprint]{neurips_2025}
│       ├── preamble.tex             # Package loads, macro shims, graphicspath
│       ├── sections/                # Override layer
│       │   ├── 1_introduction.tex
│       │   ├── 2_related_work.tex
│       │   ├── 5_results.tex
│       │   └── A_appendix.tex       # NeurIPS-specific appendix
│       └── build/                   # Build artifacts (gitignored)
│
├── Makefile                         # Build entry point
├── scripts/
│   ├── flatten.py                   # arXiv/Overleaf flattening
│   └── Dockerfile                   # Reproducible TeX Live build
└── README.md                        # Directory guide + build instructions
```

---

## Venue Entry Points

### IEEE T-RL (`venues/ieee-trl/main.tex`)

```latex
\documentclass[journal]{IEEEtran}
\input{preamble}                    % Venue-specific preamble
\input{../../shared/math_commands}   % Shared math commands

\title{Probe-Then-Act: ...}
\author{Anonymous Authors}

\begin{document}
\maketitle

\begin{abstract}
\input{../../shared/sections/0_abstract}
\end{abstract}

\begin{IEEEkeywords}
robot learning, active perception, material-adaptive manipulation, multi-physics simulation, deformable object manipulation
\end{IEEEkeywords}

\input{sections/1_introduction}      % Local override
\input{sections/2_related_work}      % Local override
\input{../../shared/sections/3_method}
\input{../../shared/sections/4_experiments}
\input{sections/5_results}           % Local override
\input{sections/6_discussion}        % Local override
\input{../../shared/sections/7_conclusion}

\bibliographystyle{IEEEtran}
\bibliography{../../shared/references}
\end{document}
```

**Citation compatibility note**: IEEEtran uses `\usepackage{cite}` (compressed numerical) while NeurIPS uses `natbib` (author-year). Shared sections should use `\cite{}` which works in both contexts (natbib backward-compatible with `\cite{key}`).

### NeurIPS (`venues/neurips/main.tex`)

```latex
\documentclass{article}
\usepackage[preprint]{neurips_2025}
\input{preamble}                    % Venue-specific preamble
\input{../../shared/math_commands}   % Shared math commands

\title{Probe-Then-Act: ...}

\begin{document}
\maketitle

\begin{abstract}
\input{../../shared/sections/0_abstract}
\end{abstract}

\input{sections/1_introduction}      % Local override
\input{sections/2_related_work}      % Local override
\input{../../shared/sections/3_method}
\input{../../shared/sections/4_experiments}
\input{sections/5_results}           % Local override
\input{../../shared/sections/7_conclusion}

\newpage
\appendix
\input{sections/A_appendix}          % NeurIPS-specific appendix

\bibliography{../../shared/references}
\bibliographystyle{plainnat}
\end{document}
```

---

## Preamble Design

### IEEE T-RL (`venues/ieee-trl/preamble.tex`)

```latex
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

% Theorems (IEEE style: continuous numbering)
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

### NeurIPS (`venues/neurips/preamble.tex`)

```latex
% Note: neurips_2025 template already loads hyperref
% Math
\usepackage{amsmath,amssymb,amsfonts,amsthm,mathtools}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% Typography (skip hyperref -- already in template)
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

% cleveref must be loaded AFTER hyperref and AFTER newtheorem
\usepackage[capitalize,noabbrev]{cleveref}

% Theorems (NeurIPS style: per-section numbering)
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

% Conditional marker for inline venue differences
\newcommand{\isneurips}{1}

% Figure paths
\graphicspath{{../../shared/figures/}{./figures/}}
```

---

## Build System

### Makefile

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

### Key Makefile Features

| Feature | Implementation |
|---------|---------------|
| `-cd` flag | `latexmk -cd` changes to source dir before building, making `../../shared/` paths resolve correctly; also ensures BibTeX runs from source dir, not `build/` |
| Dependency tracking | `$(shell find ...)` captures all source files; recompiles when any shared or local file changes |
| Parallel safety | `make -j` safe because venues have no shared write targets |
| Build isolation | Each venue's `build/` directory is gitignored; clean with `make clean` |
| Page count check | `make check` runs `texcount` on both venues |

### .latexmkrc (per-venue)

Each venue directory should contain a `.latexmkrc` to enforce consistent behavior:

```perl
# venues/ieee-trl/.latexmkrc
$out_dir = 'build';
$pdf_mode = 1;
$bibtex_use = 2;  # Run bibtex when needed
```

---

## Flatten Script (`scripts/flatten.py`)

For arXiv submission, a flattening script inlines all `\input{}` commands and copies figures to produce a single-directory zip.

### Algorithm

1. Parse `venues/<venue>/main.tex` line-by-line
2. For each `\input{path}`: resolve relative to `main.tex`, read file, recursively process nested `\input{}`s, replace with inlined content
3. For `\bibliography{../../shared/references}`: look for `venues/<venue>/build/main.bbl` (pre-generated by `latexmk`), inline as `\input{main.bbl}` then inline the `.bbl` content
4. For `\includegraphics{path}`: resolve via `\graphicspath`, copy to `output/figures/`, rewrite path to `figures/filename.pdf`
5. Strip `%` comments and `\todo{}` macros (arXiv auto-TeX compatibility)
6. Output: `output/main.tex` + `output/figures/*.pdf`

### Pre-requisite

```bash
make neurips   # Generates main.bbl via latexmk + bibtex
python3 scripts/flatten.py --venue neurips --output arxiv-submission/
```

---

## Venue Macros (`shared/venue_macros.tex`)

For small inline differences (e.g., caption length, section names), define venue-specific macros in a shared file rather than scattering `\ifdefined` throughout:

```latex
% shared/venue_macros.tex
% This file is \input by each venue's preamble.tex
% Venue-specific values are set in preamble.tex before \input{venue_macros}

% Abstract length hint
\ifdefined\isneurips
  \newcommand{\abstractmaxwords}{250}
\else
  \newcommand{\abstractmaxwords}{200}
\fi

% Section opener (IEEE has \IEEEPARstart, NeurIPS has nothing special)
\ifdefined\isneurips
  \newcommand{\secstart}[1]{#1}
\else
  \newcommand{\secstart}[1]{\IEEEPARstart{#1}{}}
\fi
```

```latex
% venues/neurips/preamble.tex
\newcommand{\isneurips}{1}
\input{../../shared/venue_macros}
```

**Principle**: Minimize inline conditions. File-level overrides are preferred. Venue macros are only for unavoidable single-line differences.

## Inline Venue Differences (Deprecated Pattern)

Avoid scattering `\ifdefined` throughout shared sections:

```latex
% BAD: Hard to find and maintain
\ifdefined\isneurips
  \caption{Short caption.}
\else
  \caption{Long caption with details.}
\fi
```

Instead, either:
1. Use `\venuecaption{short}{long}` defined in `venue_macros.tex`
2. Create a venue-specific file override

---

## Docker Support (Optional)

```dockerfile
# scripts/Dockerfile
FROM texlive/texlive:TL2023
RUN apt-get update && apt-get install -y texcount python3
WORKDIR /paper
COPY . .
CMD ["make", "all"]
```

```bash
# Build both venues in Docker
docker build -f scripts/Dockerfile -t pta-paper .
docker run --rm -v $(PWD):/paper pta-paper
```

---

## Migration Path

Current structure:
```
paper/
├── main.tex
├── main_template.tex
├── math_commands.tex
├── references.bib
├── sections/
│   ├── 0_abstract.tex
│   ├── 1_introduction.tex
│   ├── 2_related_work.tex
│   ├── 3_method.tex
│   ├── 4_experiments.tex
│   ├── 5_results.tex
│   ├── 6_discussion.tex
│   └── 7_conclusion.tex
└── figures/
```

Migration steps:

1. `mkdir -p paper/{shared/{sections,figures},venues/{ieee-trl,neurips}/{sections,figures,build},scripts}`
2. Move: `paper/sections/*.tex` → `paper/shared/sections/`, `paper/figures/*` → `paper/shared/figures/`, `paper/math_commands.tex` → `paper/shared/`, `paper/references.bib` → `paper/shared/`
3. Copy current `paper/main.tex` to `paper/venues/ieee-trl/main.tex`, rewrite `\input` paths
4. Create `paper/venues/ieee-trl/preamble.tex` from current preamble
5. Create `paper/venues/neurips/main.tex` from NeurIPS template
6. Create `paper/venues/neurips/preamble.tex` with macro shims
7. Write `Makefile`, `scripts/flatten.py`, `README.md`
8. Test: `make ieee-trl` should produce identical output to current PDF

---

## Gitignore

```
# paper/.gitignore
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

# Generated PDF backups (keep only latest in version control if desired)
# main_round*.pdf
```

---

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Shared section edit accidentally breaks one venue | Build both with `make all` after any shared edit; CI can enforce this |
| NeurIPS template loads hyperref late, breaking cleveref | Test-compile both venues after any preamble change; patch template if needed |
| arXiv flattening fails on complex `\input` nesting | `flatten.py` recursively processes nested inputs; tested before submission |
| Figure paths differ between venues | `\graphicspath` lists both shared and local; local shadows shared |
| Two venues diverge over time | README.md documents which files are shared vs override; code review for shared edits |

---

## Open Questions

1. **NeurIPS template availability**: The design assumes `neurips_2025.sty` is available. If NeurIPS 2026 template differs significantly, preamble may need updates.
2. **Overleaf compatibility**: Explicit relative paths (`../../shared/`) work on Overleaf but require uploading the entire `paper/` directory. The flatten script produces a single-directory version for this purpose.
3. **Figure format divergence**: If NeurIPS requires different figure formats (PNG vs PDF), `gen_*.py` scripts may need venue-specific output modes.
