# Probe-Then-Act: ARIS Automation Plan (Revised v3)

> **Target project:** `/home/zhuzihou/dev/probe-then-act/`
> **Paper:** "Probe-Then-Act: Active Tactile System Identification for Robust Cross-Material Robot Tool Use in Multi-Physics Simulation"
> **Target venue:** IEEE T-RL (deadline 2026-04-30)
> **Start date:** 2026-04-03
> **Current date:** 2026-04-26 (Day 23 of 27)
> **Remaining:** 4 days
>
> **Revised 2026-04-15:** 500K baselines FAILED. Root cause diagnosed (obs missing particles, reward asymmetry, residual too large). Plan revised for hotfix → re-validate → retrain path.
> **Revised 2026-04-26:** Gate 4 has been promoted and formal M1/M7 training completed. Corrected OOD evaluation completed after resumable recovery, but result-to-claim found the original broad PTA claims unsupported. The selected next direction is Option 1, ablation-first diagnosis, before paper writing.

---

## Project Summary

A robot learning method paper: the robot performs short active probing actions to infer hidden material properties, then adapts its manipulation policy accordingly. Evaluated on a cross-material multi-physics benchmark in Genesis simulator (Franka Panda + MPM materials).

**Core hypothesis:** Active probing + latent belief inference > reactive baseline under hidden physics.

---

## Current Status (Day 23)

| Item | Status |
|---|---|
| GPU | RTX 4090 24GB (WSL2) |
| Genesis venv | `/home/zhuzihou/dev/Genesis/.venv/` Python 3.11 |
| PyTorch | 2.11.0+cu126 |
| Task | Edge-push (Config D: particle y=0.02) |
| Control | JointResidualWrapper (bypasses IK) |
| Gate 0 | **PASSED** — Sand 32%, Snow 87%, EP 70% |
| Gate 2 | **PASSED** — IK/controller bypassed |
| Gate 4 | **PASSED** — post-hotfix reruns reached 100% success and ~0.399 transfer |
| Core method | **IMPLEMENTED** (LatentBeliefEncoder, ProbePhaseWrapper, train_m7.py) |
| 500K baselines | **COMPLETE** — M1 3 seeds, M7 3 seeds, M8 seed=42 available |
| Corrected OOD eval | **COMPLETE** — 35/35 rows, result-to-claim negative |
| DLC acceleration | **READY FOR DSW DRY-RUN** — executable layer lives in probe repo only |

### Day 23 OOD Blocker Resolved; Current Research Blocker

Corrected OOD eval was stuck in a cron restart loop. Episode-level NaN handling worked, but long Genesis eval processes were being OOM-killed at roughly 12 GB RSS before `run_ood_eval_v2.py` reached its final CSV write. The evaluator now persists each completed `(method, seed, split)` row immediately and refreshes aggregate results, so OOM restarts preserve progress.

**Automatic research decision:** Option 1 selected. Do not proceed to paper writing. Run ablation-first diagnosis (`m7_noprobe`, `m7_nobelief`) and only retain PTA claims if the mechanism can be repaired or narrowed.

**Current blocker:** broad Probe-Then-Act claims are not supported by corrected OOD v2. The next evidence gate is ablation OOD, not paper writing.

**Plans and runbooks:**
- `/home/zhuzihou/dev/probe-then-act/.worktrees/aris-resume-stage-d/refine-logs/EXPERIMENT_PLAN.md`
- `/home/zhuzihou/dev/probe-then-act/.worktrees/aris-resume-stage-d/docs/30_records/DLC_EXECUTION_RUNBOOK.md`
- `/home/zhuzihou/dev/probe-then-act/.worktrees/aris-resume-stage-d/docs/superpowers/plans/2026-04-26-dlc-execution-layer.md`

### Historical Critical Blockers (Discovered Day 12; resolved by hotfix)
1. **Obs missing particle info** — policy is blind to task state
2. **Reward positive/negative asymmetry** — spill penalty 50x transfer reward per %
3. **residual_scale=0.2 too large** — policy destroys base trajectory
4. **Base trajectory missing settle segment** — 90 dead steps at end
5. **Delta reward never validated** — introduced with known failure, pushed to 500K

---

## Revised Paper Scope

### Methods (3 instead of 8)

| Method | Role | Status |
|---|---|---|
| **M1: Reactive PPO** | Lower bound (no probe, no belief) | Complete; corrected OOD baseline available |
| **M7: Probe-Then-Act** | Probe → belief → adaptive control | Implemented and trained; corrected OOD broad-claim verdict is negative |
| **M8: Privileged Teacher** | Upper bound (knows material params) | Seed-42 reference available |

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

### Candidate Paper Claims
1. "Fixed manipulation strategy varies by 55pp across materials" — Config D data.
2. "Cross-material Genesis MPM benchmark" — benchmark contribution.
3. "Active probing enables material-adaptive control" — currently blocked because corrected OOD v2 shows M7 does not beat M1 broadly; only retain a narrowed version if ablations repair or explain the mechanism.

---

## Revised ARIS Execution Schedule (v3 — post-diagnosis)

### Phase 1 — Days 1-5: Environment + Infrastructure (DONE)
- Code scaffold, Genesis env, scripted baselines, training infra
- IK/controller diagnosis + JointResidualWrapper
- Config D material-discriminative task design
- Gate 0 PASSED, Gate 2 PASSED

### Phase 2 — Days 5-14: Baselines + Failure (DONE — FAILED)
- 500K M1/M8 training completed → **all runs non-functional**
- M7 core method implemented but never trained
- Root cause investigation completed (two rounds, 10 independent agents)

### Phase 2.5 — Days 12-14: HOTFIX (DONE)

The P0 hotfix sequence completed before Gate 4 promotion: particle observations,
cumulative reward restoration, spill/transfer rebalance, 80-step settle segment,
and residual scale `0.05` are now part of the active experiment stack.

### Phase 3 — Days 14-17: Retrain (if hotfix validates)

```bash
# M1 Reactive baseline (3 seeds × 500K)
python pta/scripts/train_baselines.py --method m1 --seed 42 --total-timesteps 500000

# M8 Teacher baseline (3 seeds × 500K)
python pta/scripts/train_baselines.py --method m8 --seed 42 --total-timesteps 500000
```

Add entropy_coef=0.001 at this stage if Stage 1 results are marginal.

### Phase 4 — Days 17-23: M7 Training + Eval

```bash
# M7 Probe-Then-Act (3 seeds × 500K)
python pta/scripts/train_m7.py --seed 42 --total-timesteps 500000

# Corrected OOD v2 is complete; reruns should use the resumable evaluator
python pta/scripts/run_ood_eval_v2.py
```

Current status: M7 training and corrected OOD evaluation are complete. Result-to-claim is negative for the original broad PTA claims, so the next phase is ablation-first diagnosis.

### Phase 5 — Days 20-22: Ablation-First Diagnosis

```bash
python pta/scripts/train_m7.py --ablation no_probe --seed 42 --total-timesteps 500000 --residual-scale 0.05
python pta/scripts/train_m7.py --ablation no_probe --seed 0 --total-timesteps 500000 --residual-scale 0.05
python pta/scripts/train_m7.py --ablation no_probe --seed 1 --total-timesteps 500000 --residual-scale 0.05
python pta/scripts/train_m7.py --ablation no_belief --seed 42 --total-timesteps 500000 --residual-scale 0.05
python pta/scripts/train_m7.py --ablation no_belief --seed 0 --total-timesteps 500000 --residual-scale 0.05
python pta/scripts/train_m7.py --ablation no_belief --seed 1 --total-timesteps 500000 --residual-scale 0.05
```

Optional DSW/PAI-DLC route after the repos are uploaded to a DLC-capable DSW
machine:

```bash
python pta/scripts/dlc/submit_jobs.py --suite smoke
python pta/scripts/dlc/submit_jobs.py --suite ablation --variants no_probe --seeds 0 1
python pta/scripts/dlc/submit_jobs.py --suite ablation --variants no_belief --seeds 42 0 1
python pta/scripts/dlc/submit_jobs.py --suite ood-ablation
```

Do not submit `m7_noprobe seed=42` to DLC while local R001 is still running
unless that local run is explicitly abandoned or isolated.

After these six checkpoints exist, rerun corrected resumable OOD v2 and run result-to-claim again before any paper-facing claim.

### Phase 6 — Days 22-27: Conditional `/paper-writing` + Submission

```bash
/paper-writing "NARRATIVE_REPORT.md" — venue: IEEE_JOURNAL, human checkpoint: true
```

Only enter this phase if ablation result-to-claim supports a narrowed,
defensible PTA mechanism claim.

---

## Revised Experiment Matrix

| Split | M1 (Reactive) | M7 (Ours) | M8 (Teacher) |
|---|---|---|---|
| ID: Sand | ✓ (3 seeds) | ✓ (3 seeds) | ✓ (1 seed) |
| OOD-Material: Snow | ✓ (3 seeds) | ✓ (3 seeds) | ✓ (1 seed) |
| OOD-Material: EP | ✓ (3 seeds) | ✓ (3 seeds) | ✓ (1 seed) |
| OOD-Params: Sand-extreme | ✓ (3 seeds) | ✓ (3 seeds) | — |
| **Ablation: No-Probe** | — | running/schedulable (3 seeds) | — |
| **Ablation: No-Belief** | — | schedulable (3 seeds) | — |

Total runs: ~30 (vs. original ~300+)

---

## Critical Path (Revised v3)

```
Day 23:     corrected OOD + result-to-claim (negative)
               ↓
Now:        R001 local m7_noprobe seed=42 is running
               ↓
DSW/DLC:    optional smoke + remaining ablation train jobs
               ↓
Next:       corrected OOD with m7_noprobe/m7_nobelief
               ↓
Gate:       result-to-claim again before any paper writing
```

The deadline buffer is now dominated by compute availability and ablation interpretation, not the old hotfix gate.

---

## Risk Register (Updated Day 23)

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| **Hotfix doesn't help (50K still fails)** | Blocks all | **Resolved** | Gate 4 promoted |
| **OOD eval OOM restart loop** | Blocks result-to-claim | **Resolved** | Resumable OOD completed `35/35` rows |
| Belief encoder doesn't help (M7 worse than M1 on most splits) | Blocks paper claims | High | Run `m7_noprobe` / `m7_nobelief`; pivot if mechanism is not salvageable |
| 15-day timeline too tight post-setback | Miss deadline | High | Start outline Day 18; use ARIS `/paper-writing` pipeline |
| Core method implementation > 5 days | N/A | **RESOLVED** — M7 implemented Day 5 |
| Training too slow for 3-seed sweeps | Delays eval | Medium | Use PAI-DLC from DSW for parallel ablation workers |
| Duplicate local/DLC ablation submission | Wastes GPU and confuses tracking | Medium | Keep R001 local; submit only missing seeds or isolate result roots |

---

## ARIS Input Files Status

| File | Phase | Status |
|---|---|---|
| `RESEARCH_BRIEF.md` | 0 | DONE |
| `CLAUDE.md` | 1 | DONE |
| `docs/20_planning/09_NEXT_STEPS_PLAN.md` | 3 | DONE (revised plan) |
| `results/main_results.csv` | 5 | COMPLETE for corrected OOD v2; refresh after ablation OOD |
| `NARRATIVE_REPORT.md` | 7 | TODO (after eval) |

---

## Documentation Index

| Doc | Content | Updated |
|---|---|---|
| `docs/00_foundation/00_PROJECT_BRIEF.md` | Paper positioning, abstract, contributions | 04-03 |
| `docs/10_protocols/04_VALIDATION_GATES.md` | Gate status tracker | 04-07 |
| `docs/10_protocols/05_TINY_TASK_OVERFIT_PROTOCOL.md` | Overfit protocol, experiment matrix | 04-07 |
| `docs/20_planning/07_CURRENT_BLOCKERS_AND_ACTIONS.md` | Current blockers + action plan | 04-07 |
| `docs/30_records/08_48HR_SPRINT_RESULTS.md` | IK/controller sprint results | 04-07 |
| `docs/20_planning/09_NEXT_STEPS_PLAN.md` | **Active execution plan** | 04-07 |
| `docs/40_investigations/10_TASK_DESIGN_INVESTIGATION.md` | Config D + material sweep + validation | 04-08 |
| `docs/40_investigations/11_BOWL_TOOL_INVESTIGATION.md` | Bowl tool feasibility (future Task B) | 04-08 |
| `docs/30_records/DLC_EXECUTION_RUNBOOK.md` | DSW/PAI-DLC submitter and worker boundary | 04-26 |
