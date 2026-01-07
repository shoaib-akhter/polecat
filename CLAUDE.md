# Polecat (JBS Learning Platform Automation)

## What this repo is
Polecat automates parts of the Cambridge Judge Business School learning platform (`learn.jbs.cam.ac.uk`).

### Phase 1 (current priority)
1) User manually logs in via SSO in a visible (headful) browser session  
2) Polecat discovers courses for a user-selected term (e.g., Lent)  
3) Polecat extracts assessment/exam dates from each course (two sources)  
4) Polecat shows a sanity-check summary in terminal and asks for confirmation  
5) Polecat generates an `.ics` calendar file: `JBS_Calendar_[Term]_[Year].ics`

### Phase 2 (future scope)
- Create `[term-name]/` and per-course subfolders
- Download “Required readings” and “Notes/slides/files” into structured folders

---

## Non-negotiable constraints
- **Human-in-the-loop SSO:** do not automate login or store credentials.
- **Headful browser:** user must be able to see the browser and complete SSO.
- **Be gentle:** avoid hammering the site; prefer explicit waits over tight loops.
- **Do not leak data:** no logging of personal course content beyond what’s needed.

---

## Tech stack (expected)
- Python 3.10+
- Playwright (navigation + downloads)
- BeautifulSoup4 (HTML parsing)
- `dateparser` (date/time parsing)
- `ics` (calendar generation)

---

## How the automation should work (high level)
### 1) Browser + login checkpoint
- Launch Playwright in headful mode.
- Navigate to `https://learn.jbs.cam.ac.uk/my/`.
- Wait until the user has completed SSO and the dashboard is reachable.
  - Prefer robust conditions: `page.wait_for_url("**/my/**")` and/or a known dashboard selector. :contentReference[oaicite:2]{index=2}

### 2) Term selection + course discovery
- Term is selected via CLI prompt (e.g., “Lent”).
- Apply the dashboard filter for that term.
- Extract all visible course cards:
  - `course_name`
  - `course_url`

### 3) Date extraction for each course (dual source)
- Source A: **Key resources → Key dates** (table)
- Source B: **Module overview → Assessment guidance** (free text; preferred for precise exam times)
- Normalize into a single internal structure, e.g.:
  - `course`
  - `title` (e.g., “Exam”, “Coursework due”)
  - `start_dt`, `end_dt` (timezone-aware if time exists)
  - `all_day` (if no time)
  - `source` (A/B)
  - `url` (deep link if possible)
  - `confidence/notes` (optional, for sanity checks)

### 4) Verification + output
- Print a compact summary table (sorted by date).
- Ask: “Do these dates look correct? (y/n)”
- Only write the `.ics` file on “y”.

---

## Calendar (.ics) rules
- Use RFC 5545-compatible generation via the `ics` library. :contentReference[oaicite:3]{index=3}
- Prefer stable `UID`s to reduce duplicates on re-import (e.g., hash of course+title+datetime).
- Handle:
  - all-day events (date only)
  - timed events (datetime)
  - missing/ambiguous times (mark all-day + add note)
- Put the course URL in the event `url`/description when available.

---

## Playwright guidance (keep it resilient)
- Prefer user-facing selectors (roles/text) over brittle CSS when possible. :contentReference[oaicite:4]{index=4}
- Always use explicit waits for navigation and dynamic content. :contentReference[oaicite:5]{index=5}
- Keep scraping separate from navigation: navigate with Playwright, parse with BeautifulSoup using `page.content()`.

### Optional: session persistence
If it materially improves DX, you MAY add an opt-in persistent context (stores browser state locally).
- Must be explicit and documented, because it can retain an authenticated session on disk. :contentReference[oaicite:6]{index=6}

---

## Suggested repo layout
- `polecat/`
  - `config.py` (constants)
  - `browser.py` (Playwright setup + login wait)
  - `scrapers.py` (BeautifulSoup extraction)
  - `parsers.py` (text cleanup + date parsing)
  - `calendar_gen.py` (ICS creation)
  - `main.py` (CLI orchestrator)
- `tests/` for unit tests of parsing + calendar generation

---

## Quality bar (what you should enforce)
When making changes in this repo:
- Keep changes small and reviewable; prefer incremental commits.
- Add type hints for public functions and key data structures.
- Write unit tests for parsers and ICS generation.
- Don’t introduce heavy frameworks unless clearly needed.

---

## What to do when unsure
- If an extraction is ambiguous, surface it in the summary table with a note rather than guessing silently.
- If the UI changes, favor robust selector strategies and fail with a helpful message (“Could not find Key dates link for course X”).

---

## Quick “definition of done” for Phase 1
- Running the CLI produces a verified summary table and a valid `.ics` file for a chosen term.
- No credentials stored.
- Reasonable handling of missing times and duplicate events.
