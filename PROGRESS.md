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

### Commit 4: Scrapers Module
- Created `polecat/scrapers.py` with BeautifulSoup extraction
- Data classes: `Course`, `ExtractedDate`
- `extract_courses()` — finds course cards on dashboard (multiple selector strategies)
- `extract_key_dates()` — Source A extraction from Key dates table
- `extract_assessment_dates()` — Source B extraction from Assessment guidance text
- `scrape_course_dates()` — navigates to course and extracts from both sources

### Commit 5: Parsers Module
- Created `polecat/parsers.py` with dateparser-based parsing
- Data class: `ParsedEvent` (normalized event ready for ICS)
- `parse_date()` — flexible date parsing with UK timezone
- `extract_dates_from_text()` — regex-based date extraction from free text
- `detect_event_type()` — identifies Exam, Coursework, Deadline, etc.
- `parse_duration()` — extracts duration for end time calculation
- `parse_extracted_date()` — converts ExtractedDate to ParsedEvent(s)
- `merge_events()` — deduplicates and flags conflicts (Source B prioritized)

### Commit 6: Calendar Generation Module
- Created `polecat/calendar_gen.py` with ICS generation
- `generate_uid()` — stable UIDs via SHA256 hash to prevent duplicates on re-import
- `create_event()` — converts ParsedEvent to ics.Event (handles all-day/timed)
- `create_calendar()` — builds Calendar from list of events
- `get_output_filename()` — generates filename like `JBS_Calendar_Lent_2025.ics`
- `write_calendar()` — writes ICS file to disk
- `generate_ics()` — main entry point combining all steps

### Commit 7: CLI Orchestrator
- Created `polecat/main.py` — ties all modules together
- `print_banner()` — displays Polecat header
- `print_summary_table()` — shows extracted events in a formatted table
- `get_user_confirmation()` — y/n prompt before generating ICS
- `run()` — main workflow: login → term select → discover → scrape → parse → confirm → generate
- `main()` — entry point with error handling

### Commit 8: Unit Tests
- Created `tests/__init__.py`
- Created `tests/test_parsers.py` — 20 tests covering:
  - `parse_date()` — various date formats, edge cases
  - `extract_dates_from_text()` — single/multiple dates, no matches
  - `detect_event_type()` — exam, coursework, deadline, quiz, presentation
  - `parse_duration()` — hours, minutes, no duration
  - `is_all_day()` — midnight vs non-midnight
  - `parse_extracted_date()` — Source A and B parsing
  - `merge_events()` — no conflicts, conflict prioritization, sorting
- Created `tests/test_calendar_gen.py` — 12 tests covering:
  - `generate_uid()` — stability, uniqueness, format
  - `create_event()` — timed, all-day, end time, conflict warning, source info
  - `create_calendar()` — with events, empty
  - `get_output_filename()` — format validation
  - `write_calendar()` — file creation, content validation
  - `generate_ics()` — integration test
- Added `pytest>=7.0.0` to `requirements.txt`

---

## In Progress
- None (awaiting commit)

---

## Up Next
- Phase 1 complete! Ready for testing against live site.

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
