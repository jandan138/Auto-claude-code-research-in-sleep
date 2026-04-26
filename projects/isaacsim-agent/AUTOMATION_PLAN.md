# IsaacSim-Agent: ARIS Automation Plan

> **Target project:** `/home/zhuzihou/dev/isaacsim-agent/`
> **Paper:** "A Controlled Study of Planner-to-Executor Contract Design and Runtime Validation for Embodied-Agent Execution in Isaac Sim"
> **Target venue:** IEEE RA-L (Robotics and Automation Letters)
> **Start date:** 2026-04-04
> **Stage:** Paper final-edit / reframing (no new experiments)

---

## Project Summary

A controlled factorial study on how planner-to-executor contract design (P0/P1/P2) and lightweight runtime validation (R0/R1) affect embodied-agent execution. Evaluated on 21 fixed navigation + manipulation task instances with a deterministic mock planner.

**Core claim:** Contract specificity (P1/P2 vs P0) eliminates invalid actions; runtime validation (R1 vs R0) independently recovers them; P2's brief self-check retains success while reducing overhead.

**Current situation:** Paper is at Round 2 review (8/10, Almost→Yes). External review identified two critical framing issues that must be fixed before submission:
1. Title/abstract overclaim "Isaac Sim" — 93% of runs use a lightweight Python backend, not Isaac Sim
2. Mock planner framing — deterministic if-else, not a real LLM; P0 errors are injected probes, not natural LLM failures

**Strategy:** Reword title, abstract, setup, and limitations to be transparent about backend composition and mock planner nature. NO new experiments. 1-2 day effort.

---

## System State Snapshot (2026-04-04)

| Item | Status |
|---|---|
| Experiments | ALL COMPLETE — 174 runs, results frozen |
| Figures/Tables | FROZEN — data CSVs final |
| Paper | 8-page RA-L format, LaTeX compiled, Round 2 done |
| Review score | 8/10 (Almost→Yes) |
| Blocking issue | Framing mismatch (Isaac Sim overclaim + mock planner) |
| Code | Clean, 20+ test files, all passing |

---

## Critical Review Findings (External Expert)

### Issue 1: Isaac Sim Scope Mismatch (HIGH RISK — reject-level)

| Claimed | Actual |
|---|---|
| "controlled Isaac Sim boundary study" | 27/29 tasks on toy Python backend |
| Manipulation experiments | 100% toy backend, never opens Isaac Sim |
| 146 condition evaluations | ~93% pure Python memory environment |

**Predicted fatal reviewer comment:** "The title says Isaac Sim, yet 27 of 29 tasks run on a toy Python backend. This is misleading."

### Issue 2: Mock Planner Circularity (MEDIUM RISK)

- `BlockAPilotPlannerBackend` is pure if-else, no neural network
- P0 invalid actions (`move_to_goal`, `move_object`) are design-injected, not natural LLM errors
- No LLM API integration exists in the codebase
- Risk: "causal claim collapses into: when the planner is instructed to emit typed tool calls, it emits typed tool calls"

### Issue 3: Figure 1 (LOW RISK)

- Single AI-generated bitmap, no real Isaac Sim renders
- Feasible fix: use InternUtopia renders as illustrative figure (not tied to experiment data)

---

## ARIS Skill Execution Schedule

### Phase 1 — Day 1: Wording Fixes (Manual Edits)

**No ARIS skill needed.** Direct LaTeX edits to:

#### Fix 1: Downgrade "Isaac Sim" prominence

| File | Change |
|---|---|
| Title | "...in Isaac Sim" → "...in a Lightweight Simulator Setup" or "...with Mixed Toy and Isaac Sim Backends" |
| `sections/abstract.tex` | Add: "The main factorial comparisons use a lightweight deterministic reference backend; a minimal Isaac Sim slice validates that the same qualitative ordering holds in the simulator." |
| `sections/setup.tex` | New paragraph: **Backend Composition** — majority is toy backend, Isaac Sim is small validation slice |
| `sections/discussion.tex` | Limitations: "The majority of the fixed evaluation matrix runs on a lightweight deterministic reference backend rather than inside a live Isaac Sim physics stage..." |

#### Fix 2: Tighten mock planner framing

| File | Change |
|---|---|
| `sections/abstract.tex` | Add: "The deterministic backend removes model-sampling variance so the reported comparisons isolate execution-boundary design from planner-behavior variation." |
| `sections/setup.tex` | Clarify P0 invalid actions are "injected boundary probes", not natural LLM errors |
| `sections/discussion.tex` | Limitations: "Using a deterministic mock planner means invalid-action patterns are pre-specified boundary probes rather than stochastic errors from a real foundation model." |
| `sections/discussion.tex` | Future Work: "A next step is to replicate this factorial with stochastic LLM backends to test generalization." |

---

### Phase 2 — Day 1: `/paper-compile`

```bash
cd /home/zhuzihou/dev/isaacsim-agent
/paper-compile
```

Recompile after wording edits. Verify 8-page limit not exceeded.

---

### Phase 3 — Day 2: `/auto-review-loop` (1 round)

```bash
cd /home/zhuzihou/dev/isaacsim-agent
/auto-review-loop "IsaacSim-Agent reframing review" — max_rounds: 1
```

**Purpose:** Verify that the reframed wording addresses the overclaim concern. Target: reviewer no longer flags Isaac Sim mismatch or mock planner circularity as issues.

---

### Phase 4 — Day 2: Final compile + submission prep

```bash
/paper-compile
```

Package for RA-L submission.

---

## Key Files

| File | Purpose |
|---|---|
| `paper/versions/ral/main.tex` | LaTeX entry point |
| `paper/versions/ral/sections/abstract.tex` | Abstract (needs reframing) |
| `paper/versions/ral/sections/setup.tex` | Experimental setup (needs backend disclosure) |
| `paper/versions/ral/sections/discussion.tex` | Discussion/limitations (needs honest limitations) |
| `paper/versions/ral/PAPER_IMPROVEMENT_LOG.md` | Review history (Round 0→2) |
| `paper/shared/core_claim.md` | Claim boundaries |
| `paper/shared/limitations.md` | Study limitations |
| `src/isaacsim_agent/planner/mock.py` | Mock planner (reference for wording) |

---

## Risk Register

| Risk | Impact | Fallback |
|---|---|---|
| Reframed title too weak for RA-L | Lower acceptance chance | Keep "Isaac Sim" in subtitle, move primary framing to "contract design" |
| Wording changes push past 8 pages | Formatting violation | Compress existing text, remove redundant qualifiers |
| Reviewer still flags mock planner | Major revision | Add explicit "controlled experiment" framing from psychology/HCI literature |
| Figure 1 still looks AI-generated | Minor concern | Source InternUtopia renders as illustrative figure |

---

## Strategic Summary

| Option | Verdict |
|---|---|
| Submit as-is | HIGH RISK — likely reject on framing |
| Wait for reviewer feedback | DANGEROUS — RA-L rarely gives "add 1 month of experiments" revision |
| Add real LLM API | NOT FEASIBLE — rewrites entire paper |
| **Reword + tighten claims + disclose limitations** | **ONLY VIABLE PATH — 1-2 days** |

---

## Quick-Start Commands

```bash
# Step 1: Navigate to project
cd /home/zhuzihou/dev/isaacsim-agent

# Step 2: Make wording fixes (manual LaTeX edits)
# Edit: paper/versions/ral/sections/abstract.tex
# Edit: paper/versions/ral/sections/setup.tex
# Edit: paper/versions/ral/sections/discussion.tex
# Edit: paper/versions/ral/main.tex (title)

# Step 3: Compile
/paper-compile

# Step 4: Quick review loop
/auto-review-loop "IsaacSim-Agent reframing" — max_rounds: 1

# Step 5: Final compile
/paper-compile
```
