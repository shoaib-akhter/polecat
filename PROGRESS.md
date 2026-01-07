# Polecat Development Progress Log

## Current Status
**Phase:** 1 (Calendar Automation)
**Last Updated:** 2025-01-07

---

## Completed

### Commit 1: Project Structure
- Created `polecat/` package directory
- Created `tests/` directory
- Created `PROGRESS.md` (this file)
- Created `polecat/__init__.py`

---

## In Progress
- None (awaiting commit)

---

## Up Next
1. `config.py` — Constants (base URL, timezone, term)
2. `browser.py` — Playwright setup + SSO login wait
3. `scrapers.py` — Course discovery from dashboard
4. `scrapers.py` — Date extraction (Source A: Key dates, Source B: Assessment guidance)
5. `parsers.py` — Date/text parsing utilities
6. `calendar_gen.py` — ICS file generation
7. `main.py` — CLI orchestrator
8. Unit tests for parsers and calendar generation

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-01-07 | Hardcode "Lent" term | Current term, simplifies initial build |
| 2025-01-07 | Manual term dropdown selection | Simpler, less brittle, matches human-in-the-loop philosophy |
| 2025-01-07 | Skip session persistence | Simpler for Phase 1, can add later |
| 2025-01-07 | Prioritize Source B on conflicts | More precise exam times, but flag conflicts for user |
| 2025-01-07 | UK timezone (Europe/London) | JBS is in Cambridge, UK |

---

## Notes
- User must complete SSO manually in headful browser
- User must select "Lent" from term dropdown manually, then confirm in terminal
- Output `.ics` written to current working directory with full path displayed
