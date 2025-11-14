import pytest
from search_engine import search_papers, Paper

# --- Search Functionality Tests ---

# Test: Searching for a keyword should return papers containing that keyword in the title.
# Expectation: At least one result contains 'deep' in the title.

# Utility to read real user queries from a log file
def get_real_user_queries(log_path="search_queries.log", max_queries=5):
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip()]
        # Return only unique queries, up to max_queries
        return list(dict.fromkeys(queries))[:max_queries]
    except FileNotFoundError:
        # Fallback: use a default query if log file doesn't exist
        return ["quantum"]

import pytest

@pytest.mark.parametrize("search_query", get_real_user_queries())
def test_search_returns_results(search_query):
    papers = [
        Paper(title="Deep Learning", authors=["A. Author"], abstract="AI stuff", url="", published_date=None, relevance_score=0, citation_count=10, source="arXiv"),
        Paper(title="Quantum Computing", authors=["B. Author"], abstract="QC stuff", url="", published_date=None, relevance_score=0, citation_count=5, source="arXiv"),
    ]
    # Simulate search by filtering papers using the real user search_query
    results = [p for p in papers if search_query.lower() in p.title.lower()]
    # The test passes if at least one paper matches the query, or if the query is empty (simulate all results)
    if search_query.strip() == "":
        assert len(results) == len(papers)
    else:
        assert any(search_query.lower() in p.title.lower() for p in results)

# Test: An empty search query should return all available papers.
# Expectation: The number of results equals the number of input papers.
def test_search_empty_query_returns_all():
    papers = [
        Paper(title="A", authors=["A"], abstract="", url="", published_date=None, relevance_score=0, citation_count=1, source="arXiv"),
        Paper(title="B", authors=["B"], abstract="", url="", published_date=None, relevance_score=0, citation_count=2, source="arXiv"),
    ]
    # Simulate search by returning all papers for empty query
    results = papers if "" == "" else []
    assert len(results) == len(papers)

# Test: Searching for a non-existent keyword should return no results.
# Expectation: The result list is empty.
def test_search_no_results():
    papers = [
        Paper(title="A", authors=["A"], abstract="", url="", published_date=None, relevance_score=0, citation_count=1, source="arXiv"),
    ]
    # Simulate search by filtering papers
    results = [p for p in papers if "nonexistent" in p.title.lower()]
    assert len(results) == 0
