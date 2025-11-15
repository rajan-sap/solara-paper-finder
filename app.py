def perform_search():
    """Execute paper search with transparent ranking criteria"""
    if not search_query.value.strip():
        search_error.set("Please enter a search query")
        return
    is_searching.set(True)
    search_error.set("")
    search_results.set([])
    ranking_criteria.set(None)
    visible_results_count.set(5)
    try:
        papers, criteria = search_papers(
            query=search_query.value,
            source=selected_database.value,
            max_results=10,
            sort_by="relevance"
        )
        search_results.set(papers)
        ranking_criteria.set(criteria)
    except Exception as e:
        search_error.set(str(e))
    finally:
        is_searching.set(False)
# Main Solara app

import solara
from search_engine import search_papers, Paper, RankingCriteria
from components.search_card import SearchCard
from components.search_bar import SearchBar
from components.footer import Footer
from components.header import NavBar, HeroHeader

# State management
search_query = solara.reactive("")
selected_database = solara.reactive("arXiv")
search_results = solara.reactive([])  # List of Paper objects
ranking_criteria = solara.reactive(None)  # RankingCriteria object
is_searching = solara.reactive(False)
search_error = solara.reactive("")
visible_results_count = solara.reactive(5)  # Number of results to display

@solara.component
def Page():
    """Main application"""
    
    # Add custom CSS for enhanced animations (optional, can be moved to a static file)
    solara.HTML(unsafe_innerHTML="""
    <style>
        .paper-card { position: relative; overflow: hidden; }
        .paper-card:hover { border-color: #2563eb !important; box-shadow: 0 12px 32px rgba(59, 130, 246, 0.15), 0 4px 12px rgba(0, 0, 0, 0.1) !important; }
        .search-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3) !important; }
        .load-more-btn:hover { transform: scale(1.05); box-shadow: 0 6px 16px rgba(59, 130, 246, 0.2) !important; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .fade-in { animation: fadeInUp 0.6s ease-out; }
    </style>
    """)
    
    # Outer container for centering with gradient background
    with solara.Column(style={
        "width": "100%",
        "min-height": "100vh",
        "height": "100vh",
        "background": "linear-gradient(to bottom, #f8fafc 0%, #e0e7ff 100%)",
        "padding": "40px 0",
        "box-sizing": "border-box",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "space-between"
    }):
        NavBar()
        # Main content area (flex: 1)
        with solara.Column(style={
            "width": "100%",
            "margin": "0 auto",
            "max-width": "1600px",
            "padding": "0 20px",
            "flex": 1
        }):
            HeroHeader()
            SearchBar(
                search_query=search_query,
                on_search=perform_search,
                is_searching=is_searching,
                selected_database=selected_database,
                ranking_criteria=ranking_criteria
            )
            if is_searching.value:
                solara.Markdown("🔍 **Searching for papers...**", style={"font-size": "1.3rem", "color": "#0369a1", "text-align": "center", "margin-bottom": "10px"})
            elif search_error.value:
                solara.Error(f"Error: {search_error.value}")
            elif search_results.value:
                solara.Markdown(f"### Found {len(search_results.value)} papers", style={"margin-top": "10px", "margin-bottom": "25px", "font-weight": "700", "color": "#0f172a", "font-size": "1.4rem"})
                visible_papers = search_results.value[:visible_results_count.value]
                for paper in visible_papers:
                    SearchCard(paper)

            if len(search_results.value) > visible_results_count.value:
                pass  # ...existing code for load more button...
                with solara.Row(style={"justify-content": "center", "margin-top": "20px"}):
                    solara.Button(
                        label="Load More Results",
                        on_click=lambda: visible_results_count.set(visible_results_count.value + 5),
                        classes=["load-more-btn"],
                        style={
                            "background": "linear-gradient(90deg, #2563eb 0%, #3b82f6 70%, #f1f5f9 100%)",
                            "color": "#f4f5f8",
                            "font-size": "1.1rem",
                            "font-weight": "600",
                            "padding": "12px 24px",
                            "border-radius": "10px",
                            "box-shadow": "0 6px 16px rgba(59, 130, 246, 0.2)",
                            "border": "none",
                            "transition": "transform 0.18s, box-shadow 0.18s"
                        }
                    )
            Footer()