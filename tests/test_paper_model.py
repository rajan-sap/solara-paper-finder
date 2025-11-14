import pytest
from search_engine import Paper
from datetime import datetime

# --- Paper Dataclass and Model Tests ---

# Test: Paper dataclass initializes with default affiliations if not provided.
# Expectation: affiliations is an empty list by default.
def test_paper_default_affiliations():
    paper = Paper(
        title="Test Paper",
        authors=["Author A"],
        abstract="Test abstract",
        url="http://example.com",
        published_date=datetime.now(),
        source="arXiv"
    )
    assert paper.affiliations == []

# Test: Paper dataclass stores and returns all provided fields correctly.
# Expectation: All fields match the input values.
def test_paper_fields_assignment():
    dt = datetime(2023, 1, 1)
    paper = Paper(
        title="Test Title",
        authors=["A", "B"],
        abstract="Test Abstract",
        url="http://test.com",
        published_date=dt,
        source="arXiv",
        pdf_url="http://test.com/pdf",
        citation_count=42,
        relevance_score=0.9,
        affiliations=["UiT"]
    )
    assert paper.title == "Test Title"
    assert paper.authors == ["A", "B"]
    assert paper.abstract == "Test Abstract"
    assert paper.url == "http://test.com"
    assert paper.published_date == dt
    assert paper.source == "arXiv"
    assert paper.pdf_url == "http://test.com/pdf"
    assert paper.citation_count == 42
    assert paper.relevance_score == 0.9
    assert paper.affiliations == ["UiT"]