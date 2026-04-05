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
| 2026-04-05 | Phase 3.5: Teacher v2 (2M steps) | IN PROGRESS | PID 1008295, staged reward, checkpoint every 100K |

## Git Log (probe-then-act)

```
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
| Python (.py) | 126 |
| YAML (.yaml) | 22 |
| Markdown (.md) | 10 |
| CSV (.csv) | 1 |

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
