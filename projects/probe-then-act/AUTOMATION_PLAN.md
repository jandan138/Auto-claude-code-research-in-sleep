# Probe-Then-Act: ARIS Automation Plan (Revised)

> **Target project:** `/home/zhuzihou/dev/probe-then-act/`
> **Paper:** "Probe-Then-Act: Active Tactile System Identification for Robust Cross-Material Robot Tool Use in Multi-Physics Simulation"
> **Target venue:** IEEE T-RL (deadline 2026-04-30)
> **Start date:** 2026-04-03
> **Current date:** 2026-04-08 (Day 5 of 27)
> **Remaining:** 22 days
>
> **Revised 2026-04-08:** Scope reduced from 8 methods to 3. Task validated as Config D edge-push.

---

## Project Summary

A robot learning method paper: the robot performs short active probing actions to infer hidden material properties, then adapts its manipulation policy accordingly. Evaluated on a cross-material multi-physics benchmark in Genesis simulator (Franka Panda + MPM materials).

**Core hypothesis:** Active probing + latent belief inference > reactive baseline under hidden physics.

---

## Current Status (Day 5)

| Item | Status |
|---|---|
| GPU | RTX 4090 24GB (WSL2) |
| Genesis venv | `/home/zhuzihou/dev/Genesis/.venv/` Python 3.11 |
| PyTorch | 2.11.0+cu126 |
| Task | Edge-push (Config D: particle y=0.02) |
| Control | JointResidualWrapper (bypasses IK) |
| Gate 0 | **PASSED** — Sand 32%, Snow 87%, EP 70% |
| Gate 2 | **PASSED** — IK/controller bypassed |
| Gate 4 | **PENDING RETEST** with Config D |
| Core method | 0% implemented (all stubs) |

### Key Discoveries (Days 1-5)
- Scoop-lift-dump infeasible (MPM no adhesion) → pivoted to edge-push
- Cartesian-delta → IK → PD controller broken → bypassed with JointResidualWrapper
- Config D (particle y=0.02) gives 55pp material gap: Sand 32%, Snow 87%, EP 70%
- No-op and random baselines confirm task non-triviality
- Paper scope reduced: 3 methods (M1, M7, M8) instead of 8

---

## Revised Paper Scope

### Methods (3 instead of 8)

| Method | Role | Status |
|---|---|---|
| **M1: Reactive PPO** | Lower bound (no probe, no belief) | Ready (retrain with Config D) |
| **M7: Probe-Then-Act** | Our method (probe → belief → adaptive control) | Stub — needs ~5 days implementation |
| **M8: Privileged Teacher** | Upper bound (knows material params) | Ready (train_teacher.py works) |

### Dropped
- M2 (RNN-PPO), M3 (DomainRand), M4 (Fixed-Probe), M5 (Material Router), M6 (Ours-no-uncertainty)
- Level-and-Fill task (Task B)
- Risk head / uncertainty calibration
- 5-seed sweeps (use 3 seeds)

### Material Splits

| Split | Materials | Purpose |
|---|---|---|
| **ID (training)** | Sand (32% scripted) | Hardest material — train here |
| **OOD-Material** | Snow (87%), ElastoPlastic (70%) | Unseen material families |
| **OOD-Params** | Sand with extreme E/nu/rho | Same family, shifted params |

### Paper Claims (reduced)
1. "Fixed manipulation strategy varies by 55pp across materials" — Config D data
2. "Active probing enables material-adaptive control" — M7 > M1 on OOD
3. "Cross-material Genesis MPM benchmark" — benchmark contribution

---

## Revised ARIS Execution Schedule

### Phase 1 — Days 1-5: Environment + Infrastructure (DONE)
- Code scaffold, Genesis env, scripted baselines, training infra
- IK/controller diagnosis + JointResidualWrapper
- Config D material-discriminative task design
- Gate 0 PASSED, Gate 2 PASSED

### Phase 2 — Days 5-8: Gate 4 + Baselines

```bash
# Gate 4 retest (Config D)
python pta/scripts/launch_gate4.py  # Expect sand 32% → pass

# M1 Reactive baseline
python pta/scripts/train_teacher.py --total-timesteps 500000 --exp-name m1_reactive

# M8 Teacher baseline
python pta/scripts/train_teacher.py --use-privileged --total-timesteps 500000 --exp-name m8_teacher
```

### Phase 3 — Days 8-13: Core Method Implementation (Manual)

Implement from stubs:
1. `pta/models/belief/latent_belief_encoder.py` — probe traces → (z, sigma)
2. `pta/models/policy/task_policy.py` — belief-conditioned action
3. Probe phase integration in episode flow
4. `pta/training/distill/offline_distill.py` — teacher → student
5. `pta/scripts/train_m7.py` — M7 training script

### Phase 4 — Day 13: `/experiment-bridge` (Optional)

```bash
/experiment-bridge "docs/09_NEXT_STEPS_PLAN.md" — compact: true
```

If core method is ready, use ARIS to automate remaining training runs.

### Phase 5 — Days 14-16: Evaluation

```bash
# OOD evaluation on 3 materials × 3 methods × 3 seeds
python pta/scripts/run_ood_eval.py
```

### Phase 6 — Day 16: `/auto-review-loop`

```bash
/auto-review-loop "Probe-Then-Act cross-material edge-push" — compact: true
```

### Phase 7 — Days 16-22: `/paper-writing`

```bash
/paper-writing "NARRATIVE_REPORT.md" — venue: IEEE_JOURNAL, human checkpoint: true
```

### Phase 8 — Days 22-27: Buffer + Submission

---

## Revised Experiment Matrix

| Split | M1 (Reactive) | M7 (Ours) | M8 (Teacher) |
|---|---|---|---|
| ID: Sand | ✓ (3 seeds) | ✓ (3 seeds) | ✓ (3 seeds) |
| OOD-Material: Snow | ✓ (3 seeds) | ✓ (3 seeds) | ✓ (3 seeds) |
| OOD-Material: EP | ✓ (3 seeds) | ✓ (3 seeds) | ✓ (3 seeds) |
| OOD-Params: Sand-extreme | ✓ (3 seeds) | ✓ (3 seeds) | — |
| **Ablation: No-Probe** | — | ✓ (2 seeds) | — |
| **Ablation: No-Belief** | — | ✓ (2 seeds) | — |

Total runs: ~30 (vs. original ~300+)

---

## Critical Path (Revised)

```
Day 5-8:   Gate 4 retest + M1/M8 baselines
               ↓
Day 8-13:  Implement core method (M7)        ← HIGHEST RISK
               ↓
Day 13-16: Train M7 + OOD eval + ablations
               ↓
Day 16-22: /auto-review-loop + /paper-writing
               ↓
Day 22-27: Buffer + submit
```

---

## Risk Register (Updated)

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| Gate 4 fails with Config D | Blocks all | Low (scripted = 32%) | Adjust geometry further |
| Belief encoder doesn't help (M7 ≈ M1) | Weak paper | Medium | Ensure OOD materials are genuinely different |
| Core method implementation > 5 days | Delays paper | Medium | Simplify: MLP encoder, scripted probes only |
| Training too slow for 3-seed sweeps | Delays eval | Medium | Use Vast.ai for parallel runs |
| Paper timeline too tight | Miss deadline | Medium | Start outline Day 14; use ARIS pipeline |

---

## ARIS Input Files Status

| File | Phase | Status |
|---|---|---|
| `RESEARCH_BRIEF.md` | 0 | DONE |
| `CLAUDE.md` | 1 | DONE |
| `docs/09_NEXT_STEPS_PLAN.md` | 3 | DONE (revised plan) |
| `results/main_results.csv` | 5 | TODO (after training) |
| `NARRATIVE_REPORT.md` | 7 | TODO (after eval) |

---

## Documentation Index

| Doc | Content | Updated |
|---|---|---|
| `docs/00_PROJECT_BRIEF.md` | Paper positioning, abstract, contributions | 04-03 |
| `docs/04_VALIDATION_GATES.md` | Gate status tracker | 04-07 |
| `docs/05_TINY_TASK_OVERFIT_PROTOCOL.md` | Overfit protocol, experiment matrix | 04-07 |
| `docs/07_CURRENT_BLOCKERS_AND_ACTIONS.md` | Current blockers + action plan | 04-07 |
| `docs/08_48HR_SPRINT_RESULTS.md` | IK/controller sprint results | 04-07 |
| `docs/09_NEXT_STEPS_PLAN.md` | **Active execution plan** | 04-07 |
| `docs/10_TASK_DESIGN_INVESTIGATION.md` | Config D + material sweep + validation | 04-08 |
| `docs/11_BOWL_TOOL_INVESTIGATION.md` | Bowl tool feasibility (future Task B) | 04-08 |
