
import solara
from search_engine import Paper



@solara.component
def SearchCard(paper: Paper):
    with solara.Card(classes=["paper-card", "fade-in"], style={
        "margin": "18px 0",
        "padding": "30px 32px 26px 32px",
        "border-radius": "20px",
        "box-shadow": "0 6px 32px rgba(59, 130, 246, 0.13)",
        "background": "#f8fafc",
        "border": "1.5px solid #c7d2fe",
        "transition": "border-color 0.18s"
    }):
        solara.HTML(unsafe_innerHTML="""
        <style>
        .paper-card:hover {
            border-color: #2563eb !important;
            /* No transform/scale on hover */
        }
        </style>
        """)
        with solara.Row(style={
            "gap": "18px",
            "align-items": "center",
            "margin-bottom": "8px",
            "flex-wrap": "wrap",
            "padding": "0 0 6px 0",
            "border-bottom": "1.2px solid #e5e7eb",
            "background": "#f8fafc"
        }):
            solara.HTML(tag="h2", unsafe_innerHTML=paper.title, style={
                "font-size": "1.07rem",
                "color": "#1e293b",
                "margin": "0 0 2px 0",
                "font-weight": "700",
                "flex": "2 1 320px",
                "line-height": "1.25",
                "white-space": "nowrap",
                "overflow": "hidden",
                "text-overflow": "ellipsis"
            })
            solara.HTML(
                tag="span",
                unsafe_innerHTML=f"<span style='background:#f1f5f9;border-radius:7px;padding:4px 12px;font-size:0.98rem;color:#64748b;font-weight:700;'>{paper.published_date.strftime('%Y-%m-%d')}</span>",
                style={"flex": "0 1 110px", "margin-right": "22px"}
            )
            solara.HTML(
                tag="span",
                unsafe_innerHTML=f"<span style='background:#e0e7ff;border-radius:7px;padding:4px 12px;font-size:0.98rem;color:#2563eb;font-weight:600;'>{paper.relevance_score:.2f}</span>",
                style={"flex": "0 1 80px", "margin-left": "auto"}
            )
        with solara.Row(style={"gap": "18px", "align-items": "center", "margin-bottom": "18px", "flex-wrap": "wrap"}):
            solara.HTML(
                tag="span",
                unsafe_innerHTML=f"<span style='background:#f1f5f9;border-radius:50%;padding:7px 13px 7px 13px;margin-right:8px;display:inline-block;vertical-align:middle;'><svg width='18' height='18' fill='#2563eb' viewBox='0 0 24 24'><circle cx='12' cy='12' r='10' fill='#2563eb' opacity='0.12'/><text x='12' y='16' text-anchor='middle' font-size='12' fill='#2563eb' font-weight='bold'>A</text></svg></span> <strong>Authors:</strong> <span style='font-style:italic'>{', '.join(paper.authors)}</span>",
                style={"color": "#334155", "font-size": "1.01rem", "flex": "1 1 180px"}
            )
        solara.HTML(tag="p", unsafe_innerHTML=f"<strong>Abstract:</strong> <span style='color:#475569;font-weight:400;'>{paper.abstract}</span>", style={"color": "#475569", "margin-bottom": "14px", "font-size": "1.07rem", "line-height": "1.6"})
        solara.Button(
            label="View Paper",
            icon_name="mdi-open-in-new",
            href=paper.url,
            target="_blank",
            style={
                "margin-top": "10px",
                "padding": "12px 28px",
                "font-size": "1.09rem",
                "border-radius": "9px",
                "background": "linear-gradient(90deg, #2563eb 0%, #60a5fa 100%)",
                "color": "#fff",
                "box-shadow": "0 2px 8px rgba(59, 130, 246, 0.16)",
                "font-weight": "700",
                "letter-spacing": "0.01em",
                "border": "none"
            }
        )
