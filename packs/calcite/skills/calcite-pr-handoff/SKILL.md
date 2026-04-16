---
name: calcite-pr-handoff
description: Use when a Calcite patch is implemented or nearly implemented and needs durable cross-session PR review context plus a final readiness audit.
---

# Calcite PR Handoff

Turn a near-final Calcite patch into a durable handoff artifact for later-session
review.

## Core Rules

- One PR should present one coherent invariant or one tightly coupled invariant
  set. Split follow-up work explicitly instead of hiding it in the narrative.
- This skill owns the final reviewer-style readiness audit; there is no separate
  readiness skill.
- Pull forward the issue brief and the final impact map. Do not rely on chat
  history as the handoff artifact.
- Briefs are shared multi-agent artifacts. Preserve existing entries and append
  timestamped coordination notes when another agent may resume the work.
  Record active claims for files or surfaces when work is split across agents.
- Do not claim readiness without fresh verification evidence.
- Preserve the final PR branch and worktree; this skill does not merge, discard,
  or prompt for finish-menu options.

## Bring

- Current diff or branch
- Root-cause or semantic-contract explanation
- Validation commands and current results
- Active issue brief path

## Workflow

1. Confirm that the PR scope is coherent. If it mixes bug fix, discussion item,
   and compatibility work, split the narrative and note the follow-up branch or
   issue.
2. Re-state the final invariant, exact scope, and explicit non-goals.
3. Pull in the final impact map:
   changed mechanism, sibling sites, dependent surfaces, preserved invariants,
   and deferred areas.
4. Audit reviewer-risk items:
   - source-level fix versus symptom patch
   - redundant helpers, fake hooks, fallback paths, or duplicated logic
   - no-op churn
   - under-explained behavior changes
   - stale, missing, or redundant tests on touched surfaces
   - comment quality on changed lines
5. Audit touched-surface fallout:
   `iq`, XML golden, `failFilter`, runtime-output, plan-output, row-type,
   error-text, and similar expectation surfaces when relevant.
6. Run the needed fresh verification and record exact results.
   For upstream-ready Calcite handoff, include targeted validation for the
   touched surfaces and `./gradlew clean build` unless the user explicitly
   scoped validation differently. If the clean build was not run or failed,
   report not ready.
7. Create or update a PR brief in
   `$HOME/.e6/skills/artifacts/calcite/pr-briefs/`
   using
   `$HOME/.e6/skills/e6-skills/shared/templates/calcite/PR-BRIEF-TEMPLATE.md`.
   If the brief already exists, re-read the latest file, update it in place,
   and append a coordination-log entry instead of overwriting another agent's
   notes.
8. End with a short later-session review summary:
   invariant, key touched surfaces, why it is correct, and deferred follow-ups.

## Required Outputs

- PR brief path
- Final invariant summary
- Validation evidence with exact commands
- Final branch and worktree location
- Reviewer-risk notes
- Touched-surface findings
- Deferred follow-up list
- Recommendation: ready, needs fixes, or split
- Later-session review summary
