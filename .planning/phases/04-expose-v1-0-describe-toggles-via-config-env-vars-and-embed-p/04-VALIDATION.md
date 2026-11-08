---
phase: 4
slug: expose-v1-0-describe-toggles-via-config-env-vars-and-embed-p
status: final
nyquist_compliant: true
wave_0_complete: true
created: 2026-07-06
audited: 2026-07-07
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.2 (+ pytest-asyncio, asyncio_mode="auto") |
| **Config file** | `pyproject.toml` `[tool.pytest.ini_options]` (existing) |
| **Quick run command** | `python -m pytest tests/unittest/test_org_toggles_env_override.py tests/unittest/test_config_env_override.py tests/unittest/test_org_template_changes_embed.py -q` |
| **Full suite command** | `python -m pytest tests/unittest -q` |
| **Estimated runtime** | ~30 seconds (quick) / ~3 min (full) |

*Config/embed test file names are provisional — planner finalizes them. Existing analog files: `test_org_toggles_env_override.py`, `test_org_template_prepend.py`.*

---

## Sampling Rate

- **After every task commit:** Run quick command
- **After every plan wave:** Run full suite command
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

> No REQ-IDs mapped to this phase (phase_req_ids: null). Rows are keyed to the
> capability areas from RESEARCH.md `## Validation Architecture`; the planner
> refines Task IDs / plan / wave to match the finalized PLAN.md.

| Task ID | Plan | Wave | Capability | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status | Evidence |
|---------|------|------|------------|------------|-----------------|-----------|-------------------|-------------|--------|---------|
| 04-01-01 | 01 | 1 | config__* dual-read (all 4 toggles) | — | N/A | unit | `pytest tests/unittest/test_org_toggles_env_override.py tests/unittest/test_config_env_override.py -q` | ✅ | ✅ green | `test_config_env_flips_enable_org_template`, `test_config_env_flips_enable_conventional_title`, `test_fork_toggle_falls_through_when_neither_set` |
| 04-01-02 | 01 | 1 | PR_DESCRIPTION__* backward-compat still flips toggles | — | N/A | unit | `pytest tests/unittest/test_org_toggles_env_override.py -q` | ✅ | ✅ green | `test_env_var_flips_enable_conventional_title`, `test_env_var_flips_enable_org_template`, `test_pr_description_env_still_flips_toggle` |
| 04-01-03 | 01 | 1 | config.* precedence over pr_description.* | — | N/A | unit | `pytest tests/unittest/test_config_env_override.py -q` | ✅ | ✅ green | `test_config_env_wins_over_pr_description` |
| 04-01-04 | 01 | 1 | use_description_markers load-time mirror reaches upstream | — | N/A | unit | `pytest tests/unittest/test_config_env_override.py -q` | ✅ | ✅ green | `test_mirror_copies_config_use_description_markers`, `test_mirror_noop_when_config_unset` |
| 04-02-01 | 02 | 2 | `## Changes` embed fills walkthrough + diagram markers | — | N/A | unit | `pytest tests/unittest/test_org_template_changes_embed.py -q` | ✅ | ✅ green | `test_render_fills_walkthrough_and_diagram` |
| 04-02-02 | 02 | 2 | block has no forbidden literals (File/Diagram Walkthrough) | — | N/A | unit | `pytest tests/unittest/test_org_template_changes_embed.py -q` | ✅ | ✅ green | `test_render_has_no_forbidden_literals`, `test_render_has_no_unfilled_markers` |
| 04-02-03 | 02 | 2 | enable_pr_agent_output=false suppresses default body | — | N/A | unit | `pytest tests/unittest/test_org_template_changes_embed.py -q` | ✅ | ✅ green | `test_suppression_on_returns_only_block` |
| 04-02-04 | 02 | 2 | enable_pr_agent_output=true renders default body below block | — | N/A | unit | `pytest tests/unittest/test_org_template_changes_embed.py -q` | ✅ | ✅ green | `test_suppression_off_renders_default_body` |
| 04-02-05 | 02 | 2 | byte-identical when enable_org_template=false (regression) | — | N/A | unit | `pytest tests/unittest/test_org_template_changes_embed.py tests/unittest/test_describe_byte_identical_when_off.py -q` | ✅ | ✅ green | `test_byte_identical_when_org_template_off` |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

All 9 rows verified green on 2026-07-07: 42 passed, 0 failed across the 5 phase test files (`test_org_toggles_env_override.py`, `test_config_env_override.py`, `test_org_template_changes_embed.py`, `test_org_template_prepend.py`, `test_describe_byte_identical_when_off.py`).

---

## Wave 0 Requirements

- [ ] `tests/unittest/test_config_env_override.py` — fresh-Dynaconf tests for `CONFIG__*` dual-read + mirror (new)
- [ ] `tests/unittest/test_org_template_changes_embed.py` — `## Changes` embed + `enable_pr_agent_output` suppression (new)
- [ ] Existing infrastructure (pytest + `tests/unittest/`) covers env-override and prepend regression — no framework install needed.

*Existing analog files (`test_org_toggles_env_override.py`, `test_org_template_prepend.py`) supply the fresh-Dynaconf and prepend patterns to mirror.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Live GitLab MR renders single org body with `## Changes` (walkthrough + mermaid) | — | Requires a real GitLab MR + LLM `describe` run; not reproducible in unit tests | On a GitLab MR: `CONFIG__ENABLE_ORG_TEMPLATE=true CONFIG__ENABLE_PR_AGENT_OUTPUT=false python -m pr_agent.cli --pr_url=<MR> describe`; confirm one org-formatted body with What/Why, Note/Risk, Checklist, and a `## Changes` section showing the file walkthrough + mermaid diagram |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s (42 tests in ~11s)
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-07-07

---

## Validation Audit 2026-07-07

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

VALIDATION.md was left in `draft` / `nyquist_compliant: false` at plan time and never updated post-execution. Audit ran State A: existing tests cross-referenced against all 9 capability rows. Every row maps to ≥1 named green test in the phase test files. Full green run confirmed (42 passed, 0 failed). No auditor subagent spawned — no gaps to fill (workflow: "No gaps → skip to Step 6"). Only deferred item is the live GitLab MR check (Manual-Only, not unit-testable).
