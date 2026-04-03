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
| 2026-04-04 | Phase 2.1: M1 Reactive PPO | TRAINING v2 | Fixed env, 100K steps running (~50 min) |
| 2026-04-04 | BLOCKER FIX | DONE | AABB z=0, action_scale 0.05, horizon 500, reward shaping |
| 2026-04-04 | Phase 2.6: EXPERIMENT_PLAN | DONE | refine-logs/EXPERIMENT_PLAN.md written |
| 2026-04-04 | Week 1 Deliverable | DONE | docs/Week1_environment_bootstrap.md |

## Git Log (probe-then-act)

```
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

## Next ARIS Skill Invocations

| Skill | Input | When |
|-------|-------|------|
| `/experiment-bridge` | refine-logs/EXPERIMENT_PLAN.md | After baselines trained (~Day 11) |
| `/auto-review-loop` | Experiment results | After OOD eval (~Day 17) |
| `/paper-writing` | NARRATIVE_REPORT.md | After consolidation (~Day 24) |
