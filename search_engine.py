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

def get_citation_count_from_semantic_scholar(arxiv_id: str) -> tuple[Optional[int], List[str]]:
    """
    Fetch citation count and author affiliations from Semantic Scholar API for an arXiv paper.
    """
    try:
        # Extract just the ID if full URL provided
        if 'arxiv.org' in arxiv_id:
            arxiv_id = arxiv_id.split('/')[-1]
        arxiv_id = arxiv_id.split('v')[0]
        url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}"
        params = {"fields": "citationCount,title,authors,authors.affiliations"}
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            citation_count = data.get('citationCount', 0)
            affiliations = []
            seen_affiliations = set()
            for author in data.get('authors', []):
                author_affiliations = author.get('affiliations', [])
                for affiliation in author_affiliations:
                    affiliation_name = affiliation if isinstance(affiliation, str) else affiliation.get('name', '')
                    if affiliation_name and affiliation_name not in seen_affiliations:
                        affiliations.append(affiliation_name)
                        seen_affiliations.add(affiliation_name)
            return citation_count, affiliations
        elif response.status_code == 404:
            return None, []
        else:
            return None, []
    except Exception as e:
        return None, []

class ArxivSearchEngine:
    """
    arXiv Search Engine
    """
    def __init__(self):
        self.source_name = "arXiv"
    def search(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "relevance"
    ) -> tuple[List[Paper], RankingCriteria]:
        sort_criteria_map = {
            "relevance": arxiv.SortCriterion.Relevance,
            "submittedDate": arxiv.SortCriterion.SubmittedDate,
            "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate
        }
        sort_criterion = sort_criteria_map.get(sort_by, arxiv.SortCriterion.Relevance)
        if sort_by == "citations":
            criteria = RankingCriteria(
                source="arXiv",
                sort_method="citations",
                max_results=max_results,
                filters_applied=["Sorted by number of citations (Semantic Scholar)"],
                description=f"Papers sorted by number of citations (descending). Citation data from Semantic Scholar. Results limited to top {max_results} papers."
            )
        else:
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
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criterion
        )
        papers = []
        for idx, result in enumerate(search.results()):
            relevance = 1.0 - (idx / max_results) if max_results > 0 else 0.0
            affiliations = []
            seen_domains = set()
            if hasattr(result, 'comment') and result.comment:
                import re
                email_pattern = r'[\w\.-]+@([\w\.-]+\.\w+)'
                emails = re.findall(email_pattern, result.comment)
                for domain in emails:
                    if domain not in seen_domains:
                        org_name = domain.split('.')[0].upper() if '.' in domain else domain.upper()
                        if 'edu' in domain:
                            org_name = domain.split('.')[0].replace('-', ' ').title()
                        affiliations.append(org_name)
                        seen_domains.add(domain)
            for author in result.authors:
                if hasattr(author, 'affiliation') and author.affiliation:
                    if author.affiliation not in affiliations:
                        affiliations.append(author.affiliation)
            citation_count, semantic_affiliations = get_citation_count_from_semantic_scholar(result.entry_id)
            if citation_count is None:
                citation_count = 0
            for affiliation in semantic_affiliations:
                if affiliation not in affiliations:
                    affiliations.append(affiliation)
            time.sleep(0.1)
            paper = Paper(
                title=result.title,
                authors=[author.name for author in result.authors],
                abstract=result.summary,
                published_date=result.published,
                url=result.entry_id,
                pdf_url=result.pdf_url,
                source="arXiv",
                citation_count=citation_count,
                relevance_score=relevance,
                affiliations=affiliations[:3] if affiliations else []
            )
            papers.append(paper)
        if sort_by == "citations":
            papers = sorted(papers, key=lambda p: p.citation_count, reverse=True)
            papers = papers[:max_results]
        return papers, criteria

class SearchEngineFactory:
    """Factory to create appropriate search engine based on source"""
    @staticmethod
    def get_engine(source: str):
        engines = {
            "arXiv": ArxivSearchEngine(),
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
    """
    engine = SearchEngineFactory.get_engine(source)
    return engine.search(query, max_results, sort_by)
