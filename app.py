# Main Solara app
import solara
from typing import Optional, List
from search_engine import search_papers, Paper, RankingCriteria

# State management
search_query = solara.reactive("")
selected_database = solara.reactive("arXiv")
search_results = solara.reactive([])  # List of Paper objects
ranking_criteria = solara.reactive(None)  # RankingCriteria object
is_searching = solara.reactive(False)
search_error = solara.reactive("")

@solara.component
def Page():
    """Main paper finder application"""
    
    # Hero Section
    with solara.Column(style={
        "padding": "40px 20px",
        "width": "70%",
        "margin": "0 auto",
        "box-sizing": "border-box"
    }):
        # Header
        with solara.Column(style={"text-align": "center", "margin-bottom": "60px"}):
            solara.HTML(
                tag="h1",
                unsafe_innerHTML="📚 Academic Paper Finder",
                style={
                    "font-size": "3rem",
                    "margin-bottom": "20px",
                    "color": "#1e293b",
                    "font-weight": "700"
                }
            )
            solara.Markdown(
                """
                *Discover, explore, and organize academic papers from leading research databases*
                """,
                style={"font-size": "1.2rem", "color": "#64748b", "margin-bottom": "40px"}
            )
        
        # Search Section
        with solara.Card(
            style={
                "padding": "40px",
                "box-shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                "border-radius": "12px",
                "margin-bottom": "40px"
            }
        ):
            # Header row with title and database selector
            with solara.Row(style={
                "margin-bottom": "20px",
                "align-items": "center",
                "justify-content": "space-between"
            }):
                solara.HTML(
                    tag="h2",
                    unsafe_innerHTML="🔍 Search for Papers",
                    style={"color": "#334155", "margin": "0"}
                )
                with solara.Row(style={"align-items": "center", "gap": "10px"}):
                    solara.Markdown("**Database:**", style={"margin": "0"})
                    solara.ToggleButtonsSingle(
                        value=selected_database.value,
                        on_value=selected_database.set,
                        values=["arXiv", "PubMed", "IEEE", "Google Scholar"]
                    )
            
            # Search input
            solara.InputText(
                label="Enter keywords, topic, or author",
                value=search_query.value,
                on_value=search_query.set,
                style={"width": "100%", "margin-bottom": "20px"}
            )
            
            # Search button
            with solara.Row(style={"justify-content": "center"}):
                solara.Button(
                    "Search Papers",
                    on_click=lambda: perform_search(),
                    color="primary",
                    style={
                        "padding": "12px 32px",
                        "font-size": "1.1rem",
                        "border-radius": "8px"
                    }
                )
        
        # Features Section
        with solara.Row(style={"gap": "30px", "margin-bottom": "40px"}):
            # Feature 1
            with solara.Card(style={"flex": "1", "padding": "30px", "text-align": "center"}):
                solara.HTML(
                    tag="div",
                    unsafe_innerHTML="🎯",
                    style={"font-size": "3rem", "margin-bottom": "15px"}
                )
                solara.Markdown("**Smart Search**")
                solara.Markdown(
                    "Advanced algorithms to find the most relevant papers for your research",
                    style={"color": "#64748b", "font-size": "0.9rem"}
                )
            
            # Feature 2
            with solara.Card(style={"flex": "1", "padding": "30px", "text-align": "center"}):
                solara.HTML(
                    tag="div",
                    unsafe_innerHTML="📊",
                    style={"font-size": "3rem", "margin-bottom": "15px"}
                )
                solara.Markdown("**Filter & Sort**")
                solara.Markdown(
                    "Organize results by date, citations, relevance, and more",
                    style={"color": "#64748b", "font-size": "0.9rem"}
                )
            
            # Feature 3
            with solara.Card(style={"flex": "1", "padding": "30px", "text-align": "center"}):
                solara.HTML(
                    tag="div",
                    unsafe_innerHTML="💾",
                    style={"font-size": "3rem", "margin-bottom": "15px"}
                )
                solara.Markdown("**Save & Export**")
                solara.Markdown(
                    "Export citations in multiple formats (BibTeX, APA, MLA)",
                    style={"color": "#64748b", "font-size": "0.9rem"}
                )
        
        # Results placeholder
        if search_query.value:
            with solara.Card(style={"padding": "30px", "margin-top": "20px"}):
                solara.Markdown(f"### Search Results for: *{search_query.value}*")
                solara.Markdown(f"**Database:** {selected_database.value}")
                solara.Info("Search functionality will be implemented soon. Stay tuned!")
        
        # Results Section with Ranking Criteria Documentation
        if search_results.value and ranking_criteria.value:
            with solara.Card(style={
                "padding": "30px",
                "margin-top": "20px",
                "background": "#f8fafc"
            }):
                solara.Markdown(f"### 📊 Ranking Criteria Used")
                solara.Markdown(f"**Source:** {ranking_criteria.value.source}")
                solara.Markdown(f"**Sort Method:** {ranking_criteria.value.sort_method}")
                solara.Markdown(f"**Max Results:** {ranking_criteria.value.max_results}")
                solara.Markdown(f"**Description:** {ranking_criteria.value.description}")
                
                with solara.Details("View Detailed Methodology"):
                    solara.Markdown("**Filters Applied:**")
                    for filter_item in ranking_criteria.value.filters_applied:
                        solara.Markdown(f"- {filter_item}")
        
        # Search Results
        if search_results.value:
            solara.Markdown(f"### Found {len(search_results.value)} papers")
            
            for idx, paper in enumerate(search_results.value, 1):
                with solara.Card(style={
                    "padding": "20px",
                    "margin-bottom": "20px",
                    "border-left": "4px solid #3b82f6"
                }):
                    with solara.Row(style={"justify-content": "space-between", "align-items": "start"}):
                        solara.Markdown(f"**{idx}. {paper.title}**", style={"flex": "1"})
                        solara.Markdown(f"*Relevance: {paper.relevance_score:.2f}*", 
                                      style={"color": "#64748b", "font-size": "0.9rem"})
                    
                    solara.Markdown(f"👤 **Authors:** {', '.join(paper.authors[:3])}" + 
                                  (f" *et al.*" if len(paper.authors) > 3 else ""))
                    solara.Markdown(f"📅 **Published:** {paper.published_date.strftime('%Y-%m-%d')}")
                    
                    # Abstract
                    abstract = paper.abstract[:250] + "..." if len(paper.abstract) > 250 else paper.abstract
                    solara.Markdown(f"**Abstract:** {abstract}")
                    
                    # Links
                    with solara.Row(style={"gap": "10px", "margin-top": "10px"}):
                        solara.Button(
                            "View Paper",
                            href=paper.url,
                            target="_blank",
                            color="primary",
                            text=True
                        )
                        if paper.pdf_url:
                            solara.Button(
                                "Download PDF",
                                href=paper.pdf_url,
                                target="_blank",
                                color="secondary",
                                text=True
                            )
        
        elif is_searching.value:
            with solara.Card(style={"padding": "30px", "margin-top": "20px", "text-align": "center"}):
                solara.Markdown("🔍 **Searching for papers...**")
                solara.ProgressLinear()
        
        elif search_error.value:
            with solara.Card(style={"padding": "30px", "margin-top": "20px"}):
                solara.Error(f"Error: {search_error.value}")
        
        # Footer
        with solara.Column(style={"text-align": "center", "margin-top": "60px", "padding-top": "30px", "border-top": "1px solid #e2e8f0"}):
            solara.Markdown(
                "Built with ❤️ using [Solara](https://solara.dev) | Open Source",
                style={"color": "#94a3b8"}
            )

def perform_search():
    """Execute paper search with transparent ranking criteria"""
    if not search_query.value.strip():
        search_error.set("Please enter a search query")
        return
    
    is_searching.set(True)
    search_error.set("")
    search_results.set([])
    ranking_criteria.set(None)
    
    try:
        # Import here to avoid circular imports
        from search_engine import search_papers as search_fn
        
        # Perform search and get results with criteria
        papers, criteria = search_fn(
            query=search_query.value,
            source=selected_database.value,
            max_results=20,
            sort_by="relevance"
        )
        
        search_results.set(papers)
        ranking_criteria.set(criteria)
        
    except Exception as e:
        search_error.set(str(e))
    finally:
        is_searching.set(False)

