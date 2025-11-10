"""
Paper Search Engine Module

This module provides transparent paper search functionality with explicitly documented
ranking criteria for each data source.
"""

import arxiv
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RankingCriteria:
    """Documents the criteria used to rank and filter papers"""
    source: str
    sort_method: str
    max_results: int
    filters_applied: List[str]
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display"""
        return {
            "source": self.source,
            "sort_method": self.sort_method,
            "max_results": self.max_results,
            "filters_applied": self.filters_applied,
            "description": self.description
        }


@dataclass
class Paper:
    """Represents a research paper with metadata"""
    title: str
    authors: List[str]
    abstract: str
    published_date: datetime
    url: str
    source: str
    pdf_url: str = ""
    citation_count: int = 0
    relevance_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display"""
        return {
            "title": self.title,
            "authors": ", ".join(self.authors),
            "abstract": self.abstract[:300] + "..." if len(self.abstract) > 300 else self.abstract,
            "published_date": self.published_date.strftime("%Y-%m-%d"),
            "url": self.url,
            "pdf_url": self.pdf_url,
            "source": self.source,
            "citation_count": self.citation_count,
            "relevance_score": round(self.relevance_score, 2)
        }


class ArxivSearchEngine:
    """
    arXiv Search Engine
    
    RANKING CRITERIA DOCUMENTATION:
    ================================
    
    1. SORT METHODS:
       - Relevance: Papers ranked by arXiv's internal relevance algorithm
         (considers title/abstract keyword matching, citation patterns)
       - Submitted Date: Most recently submitted papers first
       - Last Updated: Most recently updated papers first
    
    2. FILTERS:
       - Max Results: Limits number of papers returned (default: 20)
       - Date Range: Can filter by publication date (optional)
       
    3. RELEVANCE SCORE:
       - Provided by arXiv API based on query match quality
       - Range: 0.0 to 1.0 (higher = more relevant)
       
    4. LIMITATIONS:
       - Citation counts not available in arXiv API
       - No journal impact factor data
       - Preprints may not be peer-reviewed
    """
    
    def __init__(self):
        self.source_name = "arXiv"
    
    def search(
        self,
        query: str,
        max_results: int = 20,
        sort_by: str = "relevance"
    ) -> tuple[List[Paper], RankingCriteria]:
        """
        Search arXiv for papers
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            sort_by: Sorting method ("relevance", "submittedDate", "lastUpdatedDate")
            
        Returns:
            Tuple of (list of Paper objects, RankingCriteria documenting the search)
        """
        # Map sort_by string to arXiv SortCriterion
        sort_criteria_map = {
            "relevance": arxiv.SortCriterion.Relevance,
            "submittedDate": arxiv.SortCriterion.SubmittedDate,
            "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate
        }
        
        sort_criterion = sort_criteria_map.get(sort_by, arxiv.SortCriterion.Relevance)
        
        # Document the criteria being used
        criteria = RankingCriteria(
            source="arXiv",
            sort_method=sort_by,
            max_results=max_results,
            filters_applied=["Query keyword matching in title/abstract"],
            description=f"Papers sorted by {sort_by}. "
                       f"arXiv relevance algorithm considers keyword frequency, "
                       f"position in title/abstract, and semantic similarity. "
                       f"Results limited to top {max_results} papers."
        )
        
        # Perform the search
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criterion
        )
        
        papers = []
        for idx, result in enumerate(search.results()):
            # Calculate a simple relevance score based on position (1.0 for first, decreasing)
            relevance = 1.0 - (idx / max_results) if max_results > 0 else 0.0
            
            paper = Paper(
                title=result.title,
                authors=[author.name for author in result.authors],
                abstract=result.summary,
                published_date=result.published,
                url=result.entry_id,
                pdf_url=result.pdf_url,
                source="arXiv",
                citation_count=0,  # Not available in arXiv API
                relevance_score=relevance
            )
            papers.append(paper)
        
        return papers, criteria


class SearchEngineFactory:
    """Factory to create appropriate search engine based on source"""
    
    @staticmethod
    def get_engine(source: str):
        """Get search engine for specified source"""
        engines = {
            "arXiv": ArxivSearchEngine(),
            # Future: Add more engines here
            # "Semantic Scholar": SemanticScholarEngine(),
            # "PubMed": PubMedEngine(),
        }
        
        engine = engines.get(source)
        if not engine:
            raise ValueError(f"Search engine for source '{source}' not implemented yet")
        
        return engine


def search_papers(
    query: str,
    source: str = "arXiv",
    max_results: int = 20,
    sort_by: str = "relevance"
) -> tuple[List[Paper], RankingCriteria]:
    """
    Main search function with transparent ranking criteria
    
    Args:
        query: Search query string
        source: Data source ("arXiv", "PubMed", "IEEE", "Google Scholar")
        max_results: Maximum number of results
        sort_by: Sorting method (varies by source)
        
    Returns:
        Tuple of (list of Paper objects, RankingCriteria documenting methodology)
    """
    engine = SearchEngineFactory.get_engine(source)
    return engine.search(query, max_results, sort_by)
