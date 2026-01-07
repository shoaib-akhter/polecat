"""CLI orchestrator for Polecat."""

from datetime import datetime, date
from playwright.sync_api import sync_playwright

from polecat.browser import launch_browser, create_page, wait_for_login, wait_for_term_selection
from polecat.scrapers import extract_courses, scrape_course_dates, ExtractedDate
from polecat.parsers import parse_extracted_date, merge_events, ParsedEvent
from polecat.calendar_gen import generate_ics
from polecat.config import CURRENT_TERM


def print_banner() -> None:
    """Print the Polecat banner."""
    print()
    print("=" * 60)
    print("  POLECAT - JBS Learning Platform Calendar Generator")
    print(f"  Term: {CURRENT_TERM}")
    print("=" * 60)
    print()


def print_summary_table(events: list[ParsedEvent]) -> None:
    """
    Print a compact summary table of events for user verification.

    Args:
        events: List of ParsedEvent objects sorted by date
    """
    if not events:
        print("No events found.")
        return

    print()
    print("-" * 80)
    print(f"{'Date':<20} {'Course':<25} {'Event':<20} {'Source':<10}")
    print("-" * 80)

    for event in events:
        # Format date
        if isinstance(event.start_dt, datetime):
            date_str = event.start_dt.strftime("%Y-%m-%d %H:%M")
        else:
            date_str = event.start_dt.strftime("%Y-%m-%d") + " (all day)"

        # Truncate long names
        course = event.course_name[:23] + ".." if len(event.course_name) > 25 else event.course_name
        title = event.title[:18] + ".." if len(event.title) > 20 else event.title

        # Source indicator
        source = f"[{event.source}]"
        if event.conflict:
            source += " ⚠️"

        print(f"{date_str:<20} {course:<25} {title:<20} {source:<10}")

    print("-" * 80)
    print(f"Total: {len(events)} event(s)")

    # Show conflict warning if any
    conflicts = [e for e in events if e.conflict]
    if conflicts:
        print()
        print(f"⚠️  {len(conflicts)} event(s) had conflicts between sources (Source B prioritized)")

    print()


def get_user_confirmation() -> bool:
    """
    Ask user to confirm the extracted dates.

    Returns:
        True if user confirms, False otherwise
    """
    while True:
        response = input("Do these dates look correct? (y/n): ").strip().lower()
        if response in ("y", "yes"):
            return True
        elif response in ("n", "no"):
            return False
        else:
            print("Please enter 'y' or 'n'")


def run() -> None:
    """Main entry point for Polecat."""
    print_banner()

    with sync_playwright() as playwright:
        # Launch browser
        print("Launching browser...")
        browser = launch_browser(playwright)
        page = create_page(browser)

        try:
            # Step 1: Wait for SSO login
            wait_for_login(page)

            # Step 2: Wait for term selection
            wait_for_term_selection(page)

            # Step 3: Discover courses
            print()
            print("Discovering courses...")
            courses = extract_courses(page)

            if not courses:
                print("ERROR: No courses found. Exiting.")
                return

            print(f"Found {len(courses)} course(s):")
            for course in courses:
                print(f"  - {course.name}")

            # Step 4: Extract dates from each course
            print()
            print("Extracting dates from courses...")
            all_extracted: list[ExtractedDate] = []

            for course in courses:
                extracted = scrape_course_dates(page, course)
                all_extracted.extend(extracted)

            if not all_extracted:
                print()
                print("WARNING: No dates found in any course.")
                print("The page structure may have changed, or there are no key dates for this term.")
                return

            # Step 5: Parse and merge events
            print()
            print("Parsing dates...")
            all_events: list[ParsedEvent] = []

            for extracted in all_extracted:
                parsed = parse_extracted_date(extracted)
                all_events.extend(parsed)

            if not all_events:
                print("WARNING: Could not parse any dates from the extracted content.")
                return

            # Merge and deduplicate
            merged_events = merge_events(all_events)

            # Step 6: Show summary and ask for confirmation
            print_summary_table(merged_events)

            if not get_user_confirmation():
                print("Cancelled. No calendar file generated.")
                return

            # Step 7: Generate ICS file
            print()
            print("Generating calendar...")
            filepath = generate_ics(merged_events)

            print()
            print("=" * 60)
            print("SUCCESS! Calendar file created:")
            print()
            print(f"  {filepath.absolute()}")
            print()
            print("You can import this file into Google Calendar, Outlook,")
            print("Apple Calendar, or any other calendar application.")
            print("=" * 60)
            print()

        finally:
            # Clean up
            browser.close()


def main() -> None:
    """Entry point with error handling."""
    try:
        run()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
    except Exception as e:
        print(f"\nERROR: {e}")
        print("If this persists, please check the page structure or report the issue.")
        raise


if __name__ == "__main__":
    main()
