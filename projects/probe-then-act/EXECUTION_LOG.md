# Probe-Then-Act: Execution Log

> Auto-updated progress tracker for the ARIS automation pipeline.

## Timeline

| Date | Phase | Status | Key Output |
|------|-------|--------|------------|
| 2026-04-03 | Phase 0.1: Skills install | DONE | 25 ARIS skills → ~/.claude/skills/ |
| 2026-04-03 | Phase 0.2: Env setup | DONE | PyTorch 2.11+cu126, Genesis OK, MPM smoke test passed |
| 2026-04-03 | Phase 0.3: Literature check | DONE | No direct competitor. Report: docs/05_NOVELTY_CHECK_REPORT.md |
| 2026-04-03 | Phase 0.4: ARIS inputs | DONE | RESEARCH_BRIEF.md, CLAUDE.md created |
| 2026-04-03 | Phase 1.1: Code scaffold | DONE | 126 .py + 22 .yaml files |
| 2026-04-04 | Phase 1.2: Genesis env | DONE | ScoopTransfer: 100 steps, 0 NaN, 400 particles |
| 2026-04-04 | Phase 1.3: Scripted baselines | DONE | run_scripted_baseline.py (396 lines) |
| 2026-04-04 | Phase 2: Training infra | DONE | PPO/RNN-PPO/DomainRand CLI, SB3 pipeline |
| 2026-04-04 | Phase 2.1: M1 Reactive PPO | DONE | 100K steps, reward=-44.94, expl_var=0.98 |
| 2026-04-04 | BLOCKER FIX | DONE | AABB z=0, action_scale 0.05, horizon 500, reward shaping |
| 2026-04-04 | Phase 2.2: M2 RNN-PPO | DONE | 500K steps, 6h13m, 22 FPS, best reward=-6.89 |
| 2026-04-04 | Phase 2.6: EXPERIMENT_PLAN | DONE | refine-logs/EXPERIMENT_PLAN.md written |
| 2026-04-04 | Week 1 Deliverable | DONE | docs/Week1_environment_bootstrap.md |
| 2026-04-04 | NaN FIX | DONE | ctrl_dt 5e-3→2e-3, substeps 25, NaN guard in step() |
| 2026-04-04 | GPU OPT | DONE | GenesisBatchedVecEnv, 5x speedup with n_envs=4 |
| 2026-04-04→05 | Phase 2.3: M3 DomainRand PPO | DONE | 500K steps, 7h08m, 19 FPS, reward=-7.98 |
| 2026-04-05 | Phase 2.4: M4 Fixed-Probe PPO | DONE | 500K steps, 7h49m, 17 FPS, reward=-6.55 (best baseline!) |
| 2026-04-05 | Phase 2.5: M8v2 Teacher PPO | DONE | 500K steps, 6h45m, 20 FPS, reward=-7.81 |
| 2026-04-05 | Phase 2.6: Commit stability fixes | DONE | NaN guard, ctrl_dt fix, VecEnv rename |
| 2026-04-05 | Phase 3.0: Eval infrastructure | DONE | split loaders + eval_policy + eval_ood + CLI |
| 2026-04-05 | Phase 3.1: OOD eval (horizon fix) | DONE | Aligned eval horizon=200 with training |
| 2026-04-05 | Phase 3.2: Full OOD evaluation | DONE | 5 methods x 7 materials x 10 episodes |
| 2026-04-05 | Phase 3.3: M1 Gate FAILED | BLOCKER | 0% success at 500K — reward shaping needed |
| 2026-04-05 | Phase 3.4: Staged reward shaping | DONE | 4-phase reward: approach→scoop→lift→transfer |
| 2026-04-05→06 | Phase 3.5: Teacher v2 (2M steps) | STOPPED | 981K/2M, best=-6.81@230K, plateau 750K steps |
| 2026-04-06 | Phase 3.5 Diagnosis | BLOCKER | Approach-only local optimum; entropy divergence (std 1→2.1); 0% success |
| 2026-04-06 | Phase 3.6: Multi-angle literature research | DONE | 5 agents, report: refine-logs/LITERATURE_RESEARCH_REPORT.md |
| 2026-04-06 | **BLOCKER: Physical feasibility** | CRITICAL | Parallel-jaw gripper cannot scoop — need custom scoop tool |
| 2026-04-06 | M1 Pivot Plan | DONE | refine-logs/M1_FAILED_PIVOT_PLAN.md |
| 2026-04-06 | Phase 4.0–4.6: Edge-push infra | DONE | Gate 0 PASSED (42.2% transfer), wrappers, reward shaping |
| 2026-04-06 | Phase 4.7: Reward v1 bug fix | DONE | Cumulative→delta reward, particle placement fix |
| 2026-04-06→07 | Phase 4.8: E1 Teacher PPO (v1–v4) | DONE | v1-v3 config bugs; v4 ran 10K/20K, no learning (reward ±3 of baseline) |
| 2026-04-07 | Phase 4.8c: E2 Cartesian residual RL | FAILED | IK y-axis inversion — EE can't reach particles via Cartesian deltas |
| 2026-04-07 | **BLOCKER: IK y-axis inversion** | CRITICAL | Genesis DLS IK inverts y-direction for Franka at home config |
| 2026-04-07 | **48-HOUR SPRINT** | DONE | Agent team (3 agents) diagnostic + implementation sprint |
| 2026-04-07 | Sprint Task 1: Controller A/B test | DONE | `set_qpos` 10.65% transfer; `control_dofs_position` **0%** (z-div 0.68m) |
| 2026-04-07 | Sprint Task 2: IK minimal repro | DONE | NOT Genesis bug — single-step DLS coupling artifact. Iterative IK 8/8 correct |
| 2026-04-07 | Sprint Go/No-Go | **GO** | Joint-space residual confirmed as path forward |
| 2026-04-07 | Sprint Task 3: JointResidualWrapper | DONE | `pta/envs/wrappers/joint_residual_wrapper.py` — bypasses IK, uses set_qpos |
| 2026-04-07 | Sprint Task 4: Scripted demos | DONE | 20 episodes → `checkpoints/demos/scripted_joint_demos.npz` (1.45 MB) |
| 2026-04-07 | Sprint Task 5: Gate 4 residual PPO v1 | DONE | scale=0.1, reward -2.09@20K (= scripted baseline). 12.5% transfer |
| 2026-04-07 | Sprint Task 6: Gate 4 residual PPO v2 | DONE | scale=0.2, best reward -1.20@20K. 12-15% transfer |
| 2026-04-07 | **Gate 2 (Implementation)** | **PASSED** | IK/controller issues diagnosed + bypassed |
| 2026-04-07 | **Gate 4 (Tiny-Task)** | **PARTIAL** | Learner reaches baseline (12.5%) but not 30% target |
| 2026-04-07 | **NEW BLOCKER** | ACTIVE | Base trajectory quality (~12.5% vs. 30% target) |

## Phase 4: M1 Pivot — Edge-Push Task Redesign

> **Canonical plan**: `refine-logs/M1_FAILED_PIVOT_PLAN.md`
> **Validation gates**: `docs/04_VALIDATION_GATES.md`
> **Tiny-task protocol**: `docs/05_TINY_TASK_OVERFIT_PROTOCOL.md`

**Core pivot**: Scoop-lift-dump infeasible in Genesis MPM (particles don't adhere to rigid scoop during traverse). Redesigned as **edge-push task**: elevated platform + scoop pushes particles off +y edge into target below.

### Gate 0 — Physical Feasibility: **PASSED** (2026-04-06)
| Step | Task | Status | Result |
|------|------|--------|--------|
| 4.0 | Design scoop MJCF (panda_scoop.xml, 7-DOF) | **DONE** | DOF=7, scoop link OK, no NaN |
| 4.0b | Scoop-lift-dump feasibility testing | **FAILED** | MPM particles cannot adhere during traverse |
| 4.0c | Edge-push task layout design + integration | **DONE** | Elevated platform + target below edge |
| 4.1 | Scripted edge-push → verify transfer | **DONE** | **42.2% transfer, 9.0% spill, 5/5 repeatable** |
| 4.2 | Freeze sand-only tiny-task config | **DONE** | configs/overfit/sand_tiny_task.yaml |

**Gate 0 metrics (Sequence E, 5 episodes):**
```
transfer_efficiency: 0.4221 ± 0.0006  (threshold: ≥0.30) ✓
spill_ratio:         0.0902 ± 0.0004  (threshold: ≤0.20) ✓
repeatability:       5/5 consistent   (threshold: ≥2)     ✓
NaN/crash:           0               (threshold: 0)       ✓
```

### Gate 0 Key Findings
1. **MPM grid_density=128** required (64 too coarse for scoop-particle coupling)
2. **Scoop captures 146 particles** at LIFT_LOW but **all fall off during traverse** (any method: IK, joint-space, PD)
3. **Root cause**: MPM rigid-particle coupling = friction only, no adhesion. Horizontal acceleration > friction cone → spill
4. **Edge-push works** because gravity does the transfer (particles fall off platform edge)

### Steps 4.3–4.6 — Training Infrastructure: **DONE** (2026-04-06)
| Step | Task | Status |
|------|------|--------|
| 4.3 | ReducedActionWrapper (7D → 3D position-only) | **DONE** |
| 4.4 | ActionRepeatWrapper (repeat=25, policy@20Hz) | **DONE** |
| 4.5 | PPO fix (ent_coef=0.0, use_sde=True, log_std_init=-1.0) | **DONE** |
| 4.6 | Reward rebalance for edge-push | **DONE** |
| 4.6b | GymWrapper auto obs_dim detection | **DONE** |
| 4.6c | train_teacher.py wrapper stack support | **DONE** |

**Reward structure (edge-push, v2 — delta-based, 2026-04-06):**
```
approach:  -0.01 * dist_to_source              (guidance only, unchanged)
push:       5.0 * max(0, delta_mean_particle_y) (DELTA per step, was cumulative)
transfer:  20.0 * max(0, delta_transfer_frac)   (DELTA per step, was cumulative)
spill:     -2.0 * spill_frac                    (increased from -1.0)
time:      -0.001                               (increased from -0.0001)
success:   10.0 one-shot at ≥30% transfer       (was 50.0 every step)
```
**Reward v1 bug**: cumulative r_transfer + r_push gave random/zero-action policy +920 reward (particles auto-fell off edge). Fixed by delta-based rewards + moving particles to platform center (y: 0.03→-0.03).

### Gate 4 — Tiny-Task Overfit: **BLOCKED** — IK y-axis inversion

| Step | Task | Status | Result |
|------|------|--------|--------|
| 4.7 | Reward v1 bug fix (cumulative → delta) | **DONE** | Zero-action: +920 → -40 |
| 4.7b | Particle placement fix (y=0.03→-0.03) | **DONE** | Particles no longer auto-fall |
| 4.7c | Target/source bbox overlap fix | **DONE** | Clamped target y_min to platform edge |
| 4.8 | E1v1-v3: budget/horizon fixes | **DONE** | v1: 2M pol steps killed; v2: horizon=80 bug; v3: horizon=2000 OK |
| 4.8b | E1v4: Teacher PPO with delta reward | **DONE** | 10K/20K steps, reward -38±3, 0% transfer, **no learning** |
| 4.8c | E2: Cartesian-delta residual RL | **FAILED** | IK y-axis inversion blocks EE from reaching particles |
| 4.9 | Re-evaluate: success_rate ≥ 70% | **BLOCKED** | Need action space redesign first |

### E1 Teacher PPO Results (2026-04-06→07)

**E1v4** (delta reward, 20K policy steps, killed at 10K):
```
Eval curve (policy steps → mean reward):
  1K: -39.61   2K: -39.48   3K: -37.74   4K: -35.65
  5K: -41.50   6K: -39.50   7K: -37.04   8K: -37.27
  9K: -38.57   10K: -49.84
Random baseline: ~-39.6
Best: -35.65 @4K (only approach improvement, never triggered r_push/r_transfer)
```
**Diagnosis**: PPO oscillated ±3 around baseline. clip_fraction mostly 0, explained_variance ~0. Policy learned weak approach improvement but never discovered push action.

### Critical Finding: IK Y-Axis Inversion (2026-04-07)

**Discovery**: Genesis damped-least-squares IK for Franka Panda **inverts the y-axis** from home configuration. Commanding EE delta (dx=0, dy=-0.45, dz=0) moves EE in +y direction.

**Evidence**: Proportional controller targeting particles at y=-0.03 produces EE trajectory going to y=+0.08→+0.10.

**Impact**: 
- Explains why E1 PPO couldn't learn push: even correct Cartesian actions are mapped to wrong direction
- ReducedActionWrapper (3D Cartesian delta) is fundamentally broken for y-axis control
- Scripted baseline works because it uses `robot.set_qpos()` (joint-space), bypassing IK

**Next step**: Switch to **joint-space action space** (7D joint delta, no IK) or **BC warmstart** from scripted demos.

## 48-Hour Diagnostic Sprint (2026-04-07)

> Full report: `docs/08_48HR_SPRINT_RESULTS.md`

### Team Structure
3-agent team (`pta-sprint`): sprint-lead (coordinator), controller-diag (A/B test + demos), ik-fix (IK repro + wrapper + training).

### Key Results

**Controller A/B Test** (`results/controller_replay_ab_test.csv`):
- Mode A (`set_qpos`): 10.65% transfer, EE reaches y=0.41
- Mode B (`control_dofs_position`): **0% transfer**, EE z-divergence 0.68m, y lags 0.21m
- Verdict: PD controller completely fails for this task

**IK Minimal Repro** (`docs/IK_MINIMAL_REPRO.md`):
- Single-step DLS coupling artifact: 3-35% y-gain, sign flips near zero
- Iterative DLS (50 iters): 8/8 sign matches — NOT a Genesis bug
- Genesis built-in `inverse_kinematics()`: also correct
- Jacobian J[y, J1] = +0.308 — correct

**JointResidualWrapper** (`pta/envs/wrappers/joint_residual_wrapper.py`):
- Design: `q_applied = q_base[t] + residual_scale * delta_q`
- Bypasses IK entirely, uses `robot.set_qpos()` directly
- 7D action space, 30D observation (22 base + 7 q_base + 1 step_frac)
- Two trajectories: `"edge_push"` (410 steps), `"scoop"` (215 steps)
- Smoke-tested: zero residual reproduces scripted baseline

**Gate 4 Training** (`docs/GATE4_TRAINING_REPORT.md`):
| Run | Scale | Best Reward | Transfer | vs. E1 Cartesian |
|-----|-------|-------------|----------|-------------------|
| v1 | 0.1 | -2.04 @25K | ~12.5% | 20x better |
| v2 | 0.2 | -1.20 @20K | ~12-15% | 33x better |
| E1 (old) | — | -35.65 @4K | ~0% | random baseline |

Gate 4 targets NOT MET (12.5% vs. 30%), but control stack is now validated.

### New Diagnosis
Bottleneck shifted from "broken control stack" to "base trajectory quality." The scripted edge-push only achieves ~12.5% transfer. Next: better trajectory, wider residual, curriculum.

### Files Delivered
- `pta/scripts/controller_replay_ab.py`
- `pta/scripts/ik_minimal_repro.py`
- `pta/scripts/collect_joint_demos.py`
- `pta/scripts/launch_gate4.py`, `launch_gate4_v2.py`
- `pta/envs/wrappers/joint_residual_wrapper.py`
- `pta/training/rl/train_teacher.py` (updated: `use_joint_residual` param)
- `checkpoints/demos/scripted_joint_demos.npz`
- `docs/IK_MINIMAL_REPRO.md`
- `docs/GATE4_TRAINING_REPORT.md`
- `docs/08_48HR_SPRINT_RESULTS.md`

## Git Log (probe-then-act)

```
ce5b9e8 feat: reward rebalance for edge-push + PPO fixes (ent=0, SDE)
703b26d feat: Gate 0 PASSED — edge-push task with scoop tool (42.2% transfer)
d50d244 docs: add validation gates + tiny-task protocol, renumber 05→06
c7eb0bb docs: add M1 pivot plan — feasibility-first redesign
2bc61ca fix: align eval horizon with training (pass task_config)
ec040c3 docs: literature research report — 5-agent parallel investigation
9ec22a6 feat: staged reward shaping for scoop-transfer
787f7a4 feat: GPU utilization optimization for training pipeline
5c12cf2 feat: add privileged observations for M8 Teacher
87409bf feat: add M8 Teacher training resume script
7ce3601 feat: implement M4 Fixed-Probe+PPO baseline
ab9d73c fix: guard Genesis double-init in SceneBuilder
bcc1ea3 fix: resolve AABB z-range and action scale blockers
7887c0f feat: multi-method training CLI (M1/M2/M3)
2ac498f docs: Week 1 deliverable
74bab69 feat: training infrastructure + scripted baselines
5591394 chore: add README.md and requirements.txt
7aa7bf0 docs: experiment plan for ARIS
fed0d79 feat: working Genesis environment (PASSED)
c6e7406 chore: .gitignore
0f728ff feat: scaffold (126 .py + 22 .yaml)
c7c5792 docs: novelty check report
40dbfa3 chore: ARIS input files
5308fb5 docs: initial documentation
```

## File Count

| Category | Count |
|----------|-------|
| Python (.py) | 135 |
| YAML (.yaml) | 23 |
| Markdown (.md) | 16 |
| CSV (.csv) | 3 |

## Environment Verification

```
Genesis: OK (PYOPENGL_PLATFORM=osmesa)
PyTorch: 2.11.0+cu126
CUDA: True (RTX 4090)
MPM: 400 particles, 100 steps, 0 NaN
SB3: 2.8.0
sb3-contrib: 2.8.0 (RecurrentPPO)
```

## Phase 2 Training Results — Complete Summary

| Model | Method | Steps | Runtime | FPS | Best Reward | Ep Length |
|-------|--------|-------|---------|-----|-------------|-----------|
| M1 | Reactive PPO | 100K | ~50m | ~30 | -44.94 | 200 |
| M2 | RNN-PPO | 500K | 6h13m | 22 | -6.89 | 200 |
| M3 | DomainRand PPO | 500K | 7h08m | 19 | -7.98 | 200 |
| M4 | Fixed-Probe PPO | 500K | 7h49m | 17 | **-6.55** | 160 |
| M8v2 | Teacher PPO (priv) | 500K | 6h45m | 20 | -7.81 | 200 |

**Key findings:**
- M4 (Fixed-Probe) achieved the best reward (-6.55), outperforming even the privileged Teacher (-7.81)
- M2 (RNN) is second-best (-6.89), suggesting history helps
- Teacher underperforming M4 may indicate privileged obs wrapper needs review
- M1 (no history, 100K) was worst (-44.94) — confirms need for history/probing

### M1: Reactive PPO (reactive_ppo)
- **Steps:** 100,000
- **Seed:** 42
- **Final reward:** -44.94, explained_variance=0.98
- **Checkpoint:** `checkpoints/reactive_ppo_v2/`

### M2: RNN-PPO (rnn_ppo)
- **Steps:** 500,000
- **Runtime:** 6h13m, 22 FPS
- **Seed:** 42
- **Best eval:** mean_reward=-6.89 at step 490K
- **Final eval:** mean_reward=-7.73 at step 500K
- **Checkpoint:** `checkpoints/rnn_ppo/`

### M3: Domain-Randomisation PPO (domain_rand_ppo)
- **Steps:** 500,224 / 500,000
- **Runtime:** ~7h49m, 17 FPS
- **Seed:** 42
- **Material families:** sand, snow, elastoplastic
- **Checkpoint:** `checkpoints/domain_rand_ppo/`
- **Config:** MlpPolicy, lr=3e-4, n_steps=512, batch_size=256, n_epochs=5, net_arch=[256,256]

### M4: Fixed-Probe PPO (fixed_probe_ppo)
- **Steps:** 500,224 / 500,000
- **Runtime:** ~7h49m, 17 FPS
- **Seed:** 42
- **Final eval:** mean_reward=-6.55, mean_ep_length=160
- **Checkpoint:** `checkpoints/fixed_probe_ppo/`
- **Config:** MlpPolicy, lr=3e-4, n_steps=512, batch_size=256, n_epochs=5, net_arch=[256,256]

### M8v2: Teacher PPO (privileged observations)
- **Steps:** 500,096 / 500,000
- **Runtime:** 6h44m55s, 20 FPS
- **Seed:** 42
- **Final eval:** mean_reward=-7.81, mean_ep_length=200
- **Final metrics:** approx_kl=0.042, clip_fraction=0.335, std=1.93, explained_variance=1.0
- **Checkpoint:** `checkpoints/teacher/scoop_transfer_teacher_final`
- **Config:** MlpPolicy, lr=3e-4, n_steps=128, batch_size=64, n_epochs=10, net_arch=[256,256]
- **Obs dim:** 44 (37-D proprio + 7-D privileged material params via PrivilegedObsWrapper)

### Training Infrastructure Notes
- **GPU:** NVIDIA RTX 4090 (single GPU, sequential training)
- **Platform:** WSL2, PYOPENGL_PLATFORM=osmesa
- **Genesis:** MPM + Rigid coupling, 400 particles, substeps=25, ctrl_dt=2e-3
- **Robot:** Franka Panda (MJCF), 7-DOF arm + 2-DOF gripper
- **IK:** Damped least squares (lambda=0.01)
- **Reward:** transfer_frac * 1.0 + spill_frac * (-0.5) + (-0.001) + distance_shaping + success_bonus(5.0)

## Next ARIS Skill Invocations

| Skill | Input | When |
|-------|-------|------|
| `/experiment-bridge` | refine-logs/EXPERIMENT_PLAN.md | After baselines trained (~Day 11) |
| `/auto-review-loop` | Experiment results | After OOD eval (~Day 17) |
| `/paper-writing` | NARRATIVE_REPORT.md | After consolidation (~Day 24) |

## Phase 3 OOD Evaluation Results (500K baseline)

**Eval config:** horizon=200 (matched training), 10 episodes/material, deterministic=True

### ID Split (sand, snow, elastoplastic)

| Method | ID Return | Success | Spill |
|--------|-----------|---------|-------|
| **M4 Fixed-Probe** | **-6.54** | 0.0% | 0.000 |
| M3 DomainRand | -7.91 | 0.0% | 0.000 |
| M8 Teacher | -7.81 | 0.0% | 0.000 |
| M2 RNN-PPO | -8.41 | 0.0% | 0.000 |
| M1 Reactive | -8.53 | 0.0% | 0.000 |

### OOD-Material Split (snow, sand_extreme, elast_extreme, liquid)

| Method | OOD Return (avg) | Liquid Return | Liquid Spill |
|--------|------------------|---------------|--------------|
| **M4 Fixed-Probe** | **-17.45** | -48.68 | 0.741 |
| M3 DomainRand | -18.70 | -50.05 | 0.741 |
| M8 Teacher | -18.38 | -49.98 | 0.741 |
| M2 RNN-PPO | -18.94 | -50.54 | 0.741 |
| M1 Reactive | -19.06 | -50.66 | 0.741 |

### Key Findings
- **All methods 0% success rate** at 500K steps — policies haven't learned actual scoop-transfer
- **M4 (Fixed-Probe) consistently best** across ID and OOD, matching training rankings
- **Liquid OOD creates massive gap**: ~-50 return, 74% spill (physics-driven, not policy-driven)
- **Teacher underperforms M4** — privileged obs not helping at this training stage
- **Spill=0.741 on liquid is deterministic**: liquid flows out by gravity, robot barely moves
- **Next step**: Extend training to 2M-10M steps + staged reward shaping

## Phase 3.5: Teacher v2 Training — Post-Mortem

### Setup
- **Method**: Teacher PPO with privileged obs (44-D), staged reward shaping
- **Staged reward**: approach(-0.1*dist) + scoop(0.3*depth) + lift(0.5*n_lifted/total) + transfer(1.0*frac) + carry(-0.05*dist_target)
- **Hyperparams**: lr=3e-4, n_steps=128, batch=64, n_epochs=10, ent_coef=0.01, horizon=200
- **Total steps run**: 981K / 2M (stopped early)
- **Runtime**: ~9 hours, ~19 FPS

### Learning Curve
| Steps | Eval Reward | std | Phase |
|-------|-------------|-----|-------|
| 0-100K | -7.72 → -7.18 | 1.0→1.2 | Rapid approach learning |
| 100-230K | -7.18 → -6.81 | 1.2→1.5 | Approach refinement |
| 230-500K | -6.81 → -6.97 | 1.5→2.0 | **Plateau + regression** |
| 500-981K | -6.97 → ~-6.9 | 2.0→2.1 | Oscillation, no progress |

### Root Causes
1. **Approach-only local optimum**: Policy learned to minimize distance to source (approach reward ~-0.1*dist) but never discovered scoop action. Approach reward dominates because it is always available; scoop reward requires specific preconditions (EE below particle surface + near source xy).
2. **Entropy divergence**: ent_coef=0.01 drove action std from 1.0 to 2.1 over 981K steps. High std → noisy actions → unable to execute precise scoop motion even if discovered.
3. **Sparse scoop signal**: Scoop reward (0.3 * depth) requires EE to be within 0.15m xy AND below particle surface z=0.15. Random exploration with std=2 rarely hits this narrow precondition.
4. **Unknown**: Whether Franka gripper can physically complete scoop-transfer in this Genesis MPM setup has NOT been verified with a scripted trajectory.

### Checkpoints Saved
```
checkpoints/teacher_v2_staged/
  best/best_model.zip           (best eval, ~230K steps)
  scoop_transfer_teacher_{100K,200K,300K,400K,500K,600K}_steps.zip
```

### Open Questions for Literature Research
1. How do other MPM/deformable manipulation papers handle reward design?
2. Is scripted-then-RL (demo-guided) standard for granular manipulation?
3. What action spaces work for scooping tasks? (delta EE vs waypoints vs joint torques)
4. How to verify physical feasibility before RL training?
5. Are there existing Genesis/MPM scooping examples to reference?
