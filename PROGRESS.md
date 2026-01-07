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

### Commit 2: Configuration
- Created `polecat/config.py` with constants (URLs, timezone, term, timeouts)
- Created `requirements.txt` with dependencies

### Commit 3: Browser Module
- Created `polecat/browser.py` with Playwright setup
- `launch_browser()` — launches headful Chromium
- `create_page()` — creates page with default timeouts
- `wait_for_login()` — navigates to dashboard, waits for SSO completion
- `wait_for_term_selection()` — prompts user to select term, waits for confirmation

---

## In Progress
- None (awaiting commit)

---

## Up Next
1. `scrapers.py` — Course discovery from dashboard
2. `scrapers.py` — Date extraction (Source A: Key dates, Source B: Assessment guidance)
3. `parsers.py` — Date/text parsing utilities
4. `calendar_gen.py` — ICS file generation
5. `main.py` — CLI orchestrator
6. Unit tests for parsers and calendar generation

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
