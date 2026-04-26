# IsaacSim-Agent: Execution Log

> Auto-updated progress tracker for the ARIS automation pipeline.

## Timeline

| Date | Phase | Status | Key Output |
|------|-------|--------|------------|
| Pre-2026-04 | Block A experiments | DONE | 174 runs, all results frozen |
| Pre-2026-04 | Paper Round 0 | DONE | 5/10, causal isolation gap identified |
| Pre-2026-04 | Paper Round 1 | DONE | 8/10, claim discipline improved |
| Pre-2026-04 | Paper Round 2 | DONE | 8/10+, Almost→Yes |
| 2026-04-04 | External expert review | DONE | Isaac Sim overclaim + mock planner framing flagged |
| 2026-04-04 | Project registered in ARIS | DONE | projects/isaacsim-agent/ created |
| 2026-04-04 | Phase 1: Wording fixes | DONE | Title, abstract, intro, setup, results, discussion, conclusion, related_work, fig1, reviewer_submission all reframed |
| 2026-04-04 | Phase 2: Compile | DONE | 8 pages, 0 undefined refs |
| 2026-04-04 | Phase 3: Review R3a | DONE | GPT-5.4 xhigh: 7.5/10, 7 issues flagged |
| 2026-04-04 | Phase 3: Fix R3a issues | DONE | All 7 issues resolved + 2 bug fixes |
| 2026-04-04 | Phase 3: Review R3b | DONE | GPT-5.4 xhigh: 8.0/10, Almost→Yes |
| 2026-04-04 | Phase 3: Review R4 | DONE | GPT-5.4 xhigh: 8.2/10, prose polish |
| 2026-04-04 | Phase 3: Review R5 | DONE | GPT-5.4 xhigh: 8.4/10, caveat normalization |
| 2026-04-04 | Phase 3: Review R6 FINAL | DONE | GPT-5.4 xhigh: **8.6/10, YES — ready** |
| 2026-04-04 | Phase 4: Final compile | DONE | 8 pages, submission-ready |

## External Review Summary (2026-04-04)

**Reviewer:** Domain expert (not automated)
**Verdict:** Paper is honest but current framing has high reject probability

### Critical Issues

1. **Isaac Sim overclaim (reject-level):** Title says "Isaac Sim" but 93% of runs are toy Python backend. Reviewer predicts this will be caught.
2. **Mock planner circularity (medium risk):** Deterministic if-else planner; P0 errors are injected, not natural. Risk of "trivial result" criticism.
3. **Figure 1 cosmetic (low risk):** AI-generated bitmap, no real sim renders.

### Prescribed Fixes

- **Fix 1:** Downgrade "Isaac Sim" in title/abstract; add backend composition disclosure in setup; add explicit limitation
- **Fix 2:** Frame mock planner as deliberate controlled-experiment design; clarify P0 errors are boundary probes; add future-work for LLM replication

### What NOT To Do

- ❌ Introduce InternUtopia for real robot experiments (1-2 month rewrite)
- ❌ Add real LLM API (rewrites all results)
- ❌ Wait for reviewer feedback (RA-L letters = likely direct reject, not major revision)

## Git Log (isaacsim-agent, recent)

```
fb800bb — AI-generated Figure 1 regeneration + LaTeX artifact cleanup
(earlier commits: Block A experiments, paper rounds 0-2)
```

## File Count

| Category | Count |
|----------|-------|
| Python (.py) | ~60+ (src + tests) |
| LaTeX (.tex) | 8 (main + 7 sections) |
| CSV (.csv) | 4 (result tables) |
| Markdown (.md) | 15+ (docs, shared, logs) |

## Next ARIS Skill Invocations

| Skill | Input | When |
|-------|-------|------|
| Manual LaTeX edits | abstract.tex, setup.tex, discussion.tex, main.tex | Immediate |
| `/paper-compile` | paper/versions/ral/ | After wording fixes |
| `/auto-review-loop` | Reframed paper | After compile passes |
| `/paper-compile` | Final version | After review passes |
