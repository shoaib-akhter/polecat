"""BeautifulSoup scrapers for extracting course and date information."""

from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup
from playwright.sync_api import Page

from polecat.config import BASE_URL


@dataclass
class Course:
    """Represents a course extracted from the dashboard."""

    name: str
    url: str


@dataclass
class ExtractedDate:
    """Represents a date extracted from a course page."""

    course_name: str
    title: str  # e.g., "Exam", "Coursework due"
    date_text: str  # Raw date text before parsing
    source: str  # "A" (Key dates) or "B" (Assessment guidance)
    url: Optional[str] = None  # Deep link if available
    notes: Optional[str] = None  # Any ambiguity notes


def extract_courses(page: Page) -> list[Course]:
    """
    Extract all visible course cards from the dashboard.

    Args:
        page: Playwright page object on the dashboard

    Returns:
        List of Course objects with name and URL
    """
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    courses: list[Course] = []

    # Moodle typically uses course cards or course list items
    # Try multiple selector strategies for resilience
    course_links = soup.select(
        ".coursebox a.aalink, "  # Classic Moodle
        ".course-card a, "  # Card-based theme
        "[data-region='course-content'] a, "  # Modern Moodle
        ".course-listitem a.aalink"  # List view
    )

    seen_urls: set[str] = set()

    for link in course_links:
        href = link.get("href", "")
        name = link.get_text(strip=True)

        # Skip empty or duplicate entries
        if not href or not name or href in seen_urls:
            continue

        # Only include actual course links
        if "/course/view.php" not in href:
            continue

        # Normalize URL
        if href.startswith("/"):
            href = BASE_URL + href

        seen_urls.add(href)
        courses.append(Course(name=name, url=href))

    if not courses:
        print("WARNING: No courses found on dashboard.")
        print("  - Make sure you've selected the correct term filter")
        print("  - The page structure may have changed")

    return courses


def extract_key_dates(page: Page, course: Course) -> list[ExtractedDate]:
    """
    Extract dates from Source A: Key resources -> Key dates table.

    Args:
        page: Playwright page object on the course page
        course: The course being scraped

    Returns:
        List of ExtractedDate objects from the Key dates table
    """
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    dates: list[ExtractedDate] = []

    # Look for "Key dates" section - typically a table or list
    # Try to find by heading text first
    key_dates_heading = soup.find(
        lambda tag: tag.name in ["h2", "h3", "h4", "h5"]
        and "key dates" in tag.get_text(strip=True).lower()
    )

    if not key_dates_heading:
        # Try finding a link to key dates
        key_dates_link = soup.find("a", string=lambda s: s and "key dates" in s.lower())
        if key_dates_link:
            # Note: we'd need to navigate to this link to get the dates
            # For now, just note that we found the link but can't extract inline
            return dates

    # If we found the heading, look for a table or list nearby
    if key_dates_heading:
        # Look for table rows in the next sibling elements
        container = key_dates_heading.find_parent(["div", "section"])
        if container:
            rows = container.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    # Assume format: Title | Date
                    title = cells[0].get_text(strip=True)
                    date_text = cells[1].get_text(strip=True)

                    if title and date_text:
                        dates.append(
                            ExtractedDate(
                                course_name=course.name,
                                title=title,
                                date_text=date_text,
                                source="A",
                                url=course.url,
                            )
                        )

    return dates


def extract_assessment_dates(page: Page, course: Course) -> list[ExtractedDate]:
    """
    Extract dates from Source B: Module overview -> Assessment guidance.

    This source often contains more precise exam times in free text.

    Args:
        page: Playwright page object on the course page
        course: The course being scraped

    Returns:
        List of ExtractedDate objects from the Assessment guidance section
    """
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    dates: list[ExtractedDate] = []

    # Look for "Assessment guidance" or "Assessment" section
    assessment_heading = soup.find(
        lambda tag: tag.name in ["h2", "h3", "h4", "h5"]
        and "assessment" in tag.get_text(strip=True).lower()
    )

    if not assessment_heading:
        return dates

    # Get the content after the heading
    container = assessment_heading.find_parent(["div", "section"])
    if not container:
        # Try getting next siblings
        container = assessment_heading

    # Get all text content - we'll parse dates from free text later
    text_content = container.get_text(separator=" ", strip=True)

    if text_content:
        # Store the raw text - parsers.py will extract actual dates
        dates.append(
            ExtractedDate(
                course_name=course.name,
                title="Assessment",
                date_text=text_content,
                source="B",
                url=course.url,
                notes="Raw text - needs date parsing",
            )
        )

    return dates


def scrape_course_dates(page: Page, course: Course) -> list[ExtractedDate]:
    """
    Navigate to a course page and extract dates from both sources.

    Args:
        page: Playwright page object
        course: The course to scrape

    Returns:
        Combined list of dates from Source A and Source B
    """
    print(f"  Scraping: {course.name}")

    # Navigate to the course page
    page.goto(course.url)
    page.wait_for_load_state("networkidle")

    # Extract from both sources
    source_a_dates = extract_key_dates(page, course)
    source_b_dates = extract_assessment_dates(page, course)

    if not source_a_dates and not source_b_dates:
        print(f"    WARNING: No dates found for {course.name}")

    return source_a_dates + source_b_dates
