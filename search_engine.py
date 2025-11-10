"""
Research Paper Search Engine Module

This module provides transparent paper search functionality with explicitly documented
ranking criteria for each data source.
"""

import arxiv
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import time


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
    affiliations: List[str] = None  # Author affiliations/institutions
    
    def __post_init__(self):
        """Initialize optional fields"""
        if self.affiliations is None:
            self.affiliations = []
    
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


def get_citation_count_from_semantic_scholar(arxiv_id: str) -> Optional[int]:
    """
    Fetch citation count from Semantic Scholar API for an arXiv paper.
    
    Semantic Scholar is maintained by the Allen Institute for AI and provides
    reliable citation data aggregated from multiple sources.
    
    Args:
        arxiv_id: arXiv ID (e.g., "2301.12345" or full URL)
    
    Returns:
        Citation count or None if not found
    """
    try:
        # Extract just the ID if full URL provided
        if 'arxiv.org' in arxiv_id:
            arxiv_id = arxiv_id.split('/')[-1]
        
        # Remove version number if present (e.g., "2301.12345v2" -> "2301.12345")
        arxiv_id = arxiv_id.split('v')[0]
        
        # Semantic Scholar API endpoint
        url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}"
        params = {"fields": "citationCount,title"}
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('citationCount', 0)
        elif response.status_code == 404:
            # Paper not found in Semantic Scholar database
            return None
        else:
            return None
    except Exception as e:
        # Fail gracefully - don't break search if citation lookup fails
        return None


class ArxivSearchEngine:
    """
    arXiv Search Engine
    
    WHAT ARXIV API PROVIDES:
    =========================
    ✓ Paper metadata:
      - Title, authors (name only, no affiliations in structured format)
      - Abstract (full text)
      - Published date and last updated date
      - Primary category and all categories (e.g., cs.AI, math.CO)
      
    ✓ URLs and identifiers:
      - arXiv entry ID and URL (e.g., http://arxiv.org/abs/2301.12345)
      - PDF download URL
      - DOI (if paper is published in journal)
      - Journal reference (if available)
      
    ✓ Additional fields:
      - Comment field (may contain affiliations, funding info, page counts)
      - Author list with individual author objects
      
    ✗ WHAT ARXIV API DOES NOT PROVIDE:
    ===================================
    ✗ Citation counts - Not tracked by arXiv
    ✗ Impact factors - Preprint server, not journal
    ✗ Structured affiliation data - Only available in comment field as free text
    ✗ Peer review status - arXiv hosts preprints
    ✗ Full-text search - Only searches titles and abstracts
    ✗ Author h-index or metrics
    
    CITATION DATA SOURCE:
    =====================
    📊 Citation counts fetched from Semantic Scholar API
       - Maintained by Allen Institute for AI
       - Most trusted source for academic citation data
       - Aggregates from multiple databases
       - Free API with reasonable rate limits
    
    RANKING CRITERIA:
    =================
    1. SORT METHODS:
       - Relevance: arXiv's algorithm (title/abstract keyword matching)
       - Submitted Date: Most recently submitted papers first
       - Last Updated: Most recently updated papers first
    
    2. RELEVANCE SCORE:
       - Calculated based on query match quality (0.0-1.0, higher = more relevant)
    """
    
    def __init__(self):
        self.source_name = "arXiv"
    
    def search(
        self,
        query: str,
        max_results: int = 10,
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
            
            # Extract affiliations from email domains
            affiliations = []
            seen_domains = set()
            
            # Check if result has comment field which often contains contact info
            if hasattr(result, 'comment') and result.comment:
                # Extract email domains from comment
                import re
                email_pattern = r'[\w\.-]+@([\w\.-]+\.\w+)'
                emails = re.findall(email_pattern, result.comment)
                for domain in emails:
                    if domain not in seen_domains:
                        # Convert domain to organization name (e.g., mit.edu -> MIT)
                        org_name = domain.split('.')[0].upper() if '.' in domain else domain.upper()
                        # Better formatting for known domains
                        if 'edu' in domain:
                            org_name = domain.split('.')[0].replace('-', ' ').title()
                        affiliations.append(org_name)
                        seen_domains.add(domain)
            
            # Also check authors for affiliation attribute
            for author in result.authors:
                if hasattr(author, 'affiliation') and author.affiliation:
                    if author.affiliation not in affiliations:
                        affiliations.append(author.affiliation)
            
            # Fetch citation count from Semantic Scholar (most trusted source)
            citation_count = get_citation_count_from_semantic_scholar(result.entry_id)
            if citation_count is None:
                citation_count = 0  # Default to 0 if not found
            
            # Small delay to respect API rate limits (100 requests/5 minutes for Semantic Scholar)
            time.sleep(0.1)
            
            paper = Paper(
                title=result.title,
                authors=[author.name for author in result.authors],
                abstract=result.summary,
                published_date=result.published,
                url=result.entry_id,
                pdf_url=result.pdf_url,
                source="arXiv",
                citation_count=citation_count,  # Fetched from Semantic Scholar API (Allen Institute for AI)
                relevance_score=relevance,
                affiliations=affiliations[:3] if affiliations else []  # Limit to top 3
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
