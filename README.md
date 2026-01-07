# Polecat

A CLI tool that extracts exam dates, assignment deadlines, and quiz schedules from the Cambridge Judge Business School (JBS) learning platform and generates an `.ics` calendar file.

## Features

- Extracts dates from two sources:
  - **Key Dates table** (unit releases, live sessions, quiz opens/closes)
  - **Assignment pages** (submission deadlines)
- Filters to show only important deadlines by default
- Generates standard `.ics` files compatible with Google Calendar, Outlook, Apple Calendar
- Human-in-the-loop: you complete SSO login manually (no credentials stored)

## Requirements

- Python 3.10+
- A JBS learning platform account

## Installation

### macOS

```bash
# Clone the repository
git clone https://github.com/shoaib-akhter/polecat.git
cd polecat

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Windows

```powershell
# Clone the repository
git clone https://github.com/shoaib-akhter/polecat.git
cd polecat

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Usage

```bash
python -m polecat.main
```

### Steps

1. **Browser opens** - A Chromium browser window will open
2. **Login** - Complete SSO login manually in the browser
3. **Select term** - Use the dropdown to filter courses by term (e.g., "Lent")
4. **Press Enter** - Confirm in terminal once courses are visible
5. **Review dates** - Check the summary table in terminal
6. **Confirm** - Type `y` to proceed
7. **Filter options** - Choose what to include in calendar:
   - Assignment "Opens" dates (default: no)
   - Unit releases and live sessions (default: no)
8. **Done** - Calendar file saved as `JBS_Calendar_[Term]_[Year].ics`

### Example Output

```
Found 9 course(s):
  - MBA10 Strategy (2025/26)
  - MBA11 Marketing (2025/26)
  ...

Filtered: 30 event(s) will be saved to calendar

SUCCESS! Calendar file created:
  /path/to/JBS_Calendar_Lent_2026.ics
```

## What Gets Extracted

| Event Type | Included by Default |
|------------|---------------------|
| Assignment Due dates | Yes |
| Exam dates | Yes |
| Quiz Opens/Closes | Yes |
| Assignment Opens dates | No (opt-in) |
| Unit release dates | No (opt-in) |
| Live session dates | No (opt-in) |

## License

MIT
