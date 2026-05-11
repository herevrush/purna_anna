# Work Routing

How to decide who handles what.

## Routing Table

| Work Type | Route To | Examples |
|-----------|----------|----------|
| Next.js pages, components, UI | Rusty | Product listings, cart UI, checkout flow, styling |
| Python / FastAPI / REST APIs | Linus | Endpoints, auth, business logic, background tasks |
| Database schemas, models, queries | Basher | Product catalog schema, order models, migrations |
| Testing, CI/CD, Docker, infra | Livingston | pytest suites, GitHub Actions, Dockerfiles, deploy |
| Architecture, ADRs, code review | Danny | Tech decisions, PR reviews, system design |
| Scope & priorities | Danny | What to build next, trade-offs |
| Session logging | Scribe | Automatic — never needs routing |

## Issue Routing

| Label | Action | Who |
|-------|--------|-----|
| `squad` | Triage: analyze issue, assign `squad:{member}` label | Lead |
| `squad:{name}` | Pick up issue and complete the work | Named member |

### How Issue Assignment Works

1. When a GitHub issue gets the `squad` label, the **Lead** triages it — analyzing content, assigning the right `squad:{member}` label, and commenting with triage notes.
2. When a `squad:{member}` label is applied, that member picks up the issue in their next session.
3. Members can reassign by removing their label and adding another member's label.
4. The `squad` label is the "inbox" — untriaged issues waiting for Lead review.

## Rules

1. **Eager by default** — spawn all agents who could usefully start work, including anticipatory downstream work.
2. **Scribe always runs** after substantial work, always as `mode: "background"`. Never blocks.
3. **Quick facts → coordinator answers directly.** Don't spawn an agent for "what port does the server run on?"
4. **When two agents could handle it**, pick the one whose domain is the primary concern.
5. **"Team, ..." → fan-out.** Spawn all relevant agents in parallel as `mode: "background"`.
6. **Anticipate downstream work.** If a feature is being built, spawn the tester to write test cases from requirements simultaneously.
7. **Issue-labeled work** — when a `squad:{member}` label is applied to an issue, route to that member. The Lead handles all `squad` (base label) triage.

## Work Type → Agent

| Work Type | Primary | Secondary |
|-----------|---------|----------|
| Architecture, decisions, review | Danny | — |
| Next.js, React, UI/UX | Rusty | — |
| Python, FastAPI, APIs | Linus | — |
| Database, models, queries | Basher | — |
| Testing, CI/CD, infra | Livingston | — |

