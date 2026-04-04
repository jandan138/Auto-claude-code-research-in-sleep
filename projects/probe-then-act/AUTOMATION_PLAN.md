# Probe-Then-Act: ARIS Automation Plan

> **Target project:** `/home/zhuzihou/dev/probe-then-act/`
> **Paper:** "Probe-Then-Act: Active Tactile System Identification for Robust Cross-Material Robot Tool Use in Multi-Physics Simulation"
> **Target venue:** IEEE T-RL (IROS 2026 / CASE 2026 transfer, deadline 2026-04-30)
> **Start date:** 2026-04-03
> **Duration:** 27 days compressed (original 8-week plan)

---

## Project Summary

A robot learning method paper: the robot performs short active probing actions to infer hidden material properties, then adapts its manipulation policy accordingly. Evaluated on a cross-material multi-physics benchmark in Genesis simulator (Franka Panda + MPM materials).

**Core hypothesis:** Active probing + latent belief + uncertainty-aware control > reactive / recurrent / domain-randomization baselines under hidden physics.

---

## System State Snapshot (2026-04-03)

| Item | Status |
|---|---|
| GPU | RTX 4090 24GB (WSL2) |
| Genesis venv | `/home/zhuzihou/dev/Genesis/.venv/` Python 3.11.14 |
| PyTorch | 2.6.0+cu124 (needs upgrade to >= 2.8.0) |
| WSL2 rendering | OpenGL/EGL needs fix for headless |
| Package manager | `uv` available |
| Disk | 916 GB free |
| Project code | Zero — docs only |

**Key Genesis code references:**
- `Genesis/examples/manipulation/grasp_env.py` — vectorized RL env template
- `Genesis/examples/coupling/sand_wheel.py` — MPM-rigid coupling pattern
- `Genesis/examples/sensors/tactile_elastomer_franka.py` — Franka tactile sensing

---

## ARIS Skill Execution Schedule

### Phase 0 — Day 1: `/research-lit` + `/novelty-check`

```bash
# In probe-then-act project directory
/research-lit "active tactile probing latent belief robot manipulation deformable materials hidden physics 2025 2026"
```

Then:
```bash
/novelty-check
# Input: the Probe-Then-Act proposal from docs/00_PROJECT_BRIEF.md
```

**Purpose:** Confirm no 2025-2026 concurrent work blocks our contribution.
**If competitor found:** Adjust positioning before proceeding.

---

### Phase 1 — Days 2-5: Manual Environment + Code Scaffold

Not ARIS-automated. Build from `docs/01_REPO_BLUEPRINT.md`:

1. Initialize git, set up venv, install dependencies
2. Scaffold `pta/` package (~100 files)
3. Build Scoop-and-Transfer environment (Genesis MPM + Franka)
4. Scripted baselines to validate metrics
5. Write `CLAUDE.md` for ARIS conventions

**Exit gate:** 100 stable steps, scripted scoop works, metrics correct.

---

### Phase 2 — Days 5-11: Baselines + Teacher (manual RL training)

Train 5 methods on local RTX 4090:
- M1: Reactive PPO
- M2: RNN-PPO
- M3: Domain Randomization PPO
- M4: Fixed-Probe + PPO
- M8: Privileged Teacher (upper bound)

**ARIS prep:** Write `refine-logs/EXPERIMENT_PLAN.md` for Phase 3.

---

### Phase 3 — Day 11: `/experiment-bridge`

```bash
/experiment-bridge "refine-logs/EXPERIMENT_PLAN.md" — compact: true
```

**What it does:**
1. Reads experiment plan with claim-driven roadmap
2. Implements remaining training code (M5 Material Router, M6 Ours-no-uncertainty, M7 Probe-Then-Act)
3. Sends code to GPT-5.4 for cross-review
4. Auto-deploys training runs
5. Sanity-first: smallest experiment first

**Expected input file:** `refine-logs/EXPERIMENT_PLAN.md` containing:
- Claim → experiment mapping
- Method configurations
- GPU budget per run
- Success criteria per experiment

---

### Phase 4 — Day 17: `/auto-review-loop`

```bash
/auto-review-loop "Probe-Then-Act cross-material robustness evaluation" — compact: true
```

**What it does:**
1. GPT-5.4 reviews all experiment results
2. Identifies weak claims, missing experiments, statistical issues
3. Claude fixes issues, reruns experiments
4. Re-review (up to 4 rounds)
5. Target: score >= 6/10

**Expected inputs (auto-discovered):**
- `results/tables/main_results.csv`
- `results/tables/ablation_results.csv`
- Training logs in `logs/`
- `EXPERIMENT_LOG.md` or `findings.md` (compact mode)

---

### Phase 5 — Day 21-24: Consolidation (semi-manual)

- 5-seed sweeps, confidence intervals
- Level-and-Fill task (conditional on Scoop-Transfer success)
- Failure taxonomy + qualitative videos
- Write `NARRATIVE_REPORT.md` for paper pipeline

---

### Phase 6 — Day 24: `/paper-writing`

```bash
/paper-writing "NARRATIVE_REPORT.md" — venue: IEEE_JOURNAL, human checkpoint: true
```

**What it does:**
1. Phase 1: Paper plan (outline, contribution mapping)
2. Phase 2: Figure generation (method overview, result plots, failure gallery)
3. Phase 3: LaTeX section writing with DBLP/CrossRef citation verification
4. Phase 4: Compile PDF
5. Phase 5: 2-round GPT-5.4 improvement loop

**T-RL format constraints:**
- 12 pages max (Transactions format)
- Abstract <= 200 words
- Double-anonymous
- Multimedia zip <= 60 MB

---

## ARIS Input Files Checklist

Files to prepare in `probe-then-act/` for ARIS consumption:

| File | Phase | Status | Template |
|---|---|---|---|
| `RESEARCH_BRIEF.md` | 0 | TODO — convert from `docs/00_PROJECT_BRIEF.md` | `templates/RESEARCH_BRIEF_TEMPLATE.md` |
| `CLAUDE.md` | 1 | TODO | — |
| `refine-logs/EXPERIMENT_PLAN.md` | 3 | TODO — write after baselines | `templates/EXPERIMENT_PLAN_TEMPLATE.md` |
| `EXPERIMENT_LOG.md` | 4 | Auto-generated during training | `templates/EXPERIMENT_LOG_TEMPLATE.md` |
| `findings.md` | 4 | Auto-generated during eval | `templates/FINDINGS_TEMPLATE.md` |
| `NARRATIVE_REPORT.md` | 6 | TODO — write after consolidation | `templates/NARRATIVE_REPORT_TEMPLATE.md` |

---

## Critical Path

```
Day 1-2:  /research-lit + /novelty-check + env setup
              ↓
Day 2-5:  Code scaffold + Genesis environment  ← HIGHEST RISK
              ↓
Day 5-11: Baseline training (manual RL)
              ↓
Day 11-17: /experiment-bridge → main method
              ↓
Day 17-21: /auto-review-loop → OOD + ablations
              ↓
Day 21-24: Consolidation + NARRATIVE_REPORT.md
              ↓
Day 24-27: /paper-writing → submit
```

---

## Risk Register

| Risk | Impact | Fallback |
|---|---|---|
| Genesis MPM unstable in WSL2 | Blocks all | Option A: rigid-body + hidden friction/mass. Option B: SoftGym/PlasticineLab. Option C: single material + param variation |
| PyTorch upgrade breaks Genesis | Blocks all | Pin to Genesis-compatible version |
| 27 days too tight | Miss deadline | Skip Level-and-Fill, reduce to 3 seeds, narrow claims |
| Single RTX 4090 bottleneck | Slow training | Use `/vast-gpu` for parallel seed sweeps |
| Weak OOD improvement | Weak paper | Strengthen splits, narrow claims, invest in better evaluation not fancier architecture |

---

## Experiment Matrix (from `03_EXPERIMENT_PROTOCOL.md`)

| Task | Split | Methods |
|---|---|---|
| Scoop-Transfer | ID | M1, M2, M3, M4, M6, M7, M8 |
| Scoop-Transfer | OOD-Material | M1, M2, M3, M4, M6, M7 |
| Scoop-Transfer | OOD-Tool | M1, M2, M3, M4, M6, M7 |
| Scoop-Transfer | OOD-Sensor | M1, M2, M3, M4, M6, M7 |
| Level-Fill | ID | M1, M2, M6, M7, M8 |
| Level-Fill | OOD-Material | M1, M2, M6, M7 |
| Level-Fill | OOD-Tool | M1, M2, M6, M7 |

**Methods key:** M1=Reactive PPO, M2=RNN-PPO, M3=DomainRand PPO, M4=Fixed-Probe+PPO, M5=Material Router, M6=Ours-no-uncertainty, M7=Probe-Then-Act, M8=Privileged Teacher

---

## Quick-Start Commands

```bash
# Step 1: Navigate to project
cd /home/zhuzihou/dev/probe-then-act

# Step 2: Literature check (ARIS)
/research-lit "active tactile probing latent belief robot manipulation deformable materials 2025 2026"
/novelty-check

# Step 3: After baselines are trained, run experiment bridge (ARIS)
/experiment-bridge "refine-logs/EXPERIMENT_PLAN.md" — compact: true

# Step 4: After experiments complete, run review loop (ARIS)
/auto-review-loop "Probe-Then-Act" — compact: true

# Step 5: After consolidation, write paper (ARIS)
/paper-writing "NARRATIVE_REPORT.md" — venue: IEEE_JOURNAL, human checkpoint: true
```
