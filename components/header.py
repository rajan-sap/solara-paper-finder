import solara

# Navigation bar header at the very top
@solara.component
def NavBar():
    with solara.Row(style={
        "width": "100%",
        "position": "sticky",
        "top": 0,
        "z-index": 100,
        "background": "#e0e7ff",  # Lighter blue tone
        "padding": "0.7rem 2.5rem",
        "align-items": "center",
        "justify-content": "space-between",
        "box-shadow": "0 2px 12px rgba(59, 130, 246, 0.08)"
    }):
        # Logo
        solara.HTML(
            tag="div",
            unsafe_innerHTML="<span style='font-size:2.1rem;font-weight:800;color:#2563eb;vertical-align:middle;'>📚 TopRead</span>",
            style={"display": "flex", "align-items": "center"}
        )
        # Navigation text labels
        with solara.Row(style={
            "gap": "24px",
            "align-items": "center",
            "margin-left": "auto",
            "background": "#e0e7ff",
            "padding": "6px 18px",
            "border-radius": "8px"
        }):
            solara.Button(label="My Library", style={"background": "none", "color": "#2563eb", "font-size": "1.13rem", "box-shadow": "none", "border": "none", "font-weight": "700", "letter-spacing": "0.01em"}, outlined=False)
            solara.Button(label="About", style={"background": "none", "color": "#2563eb", "font-size": "1.13rem", "box-shadow": "none", "border": "none", "font-weight": "700", "letter-spacing": "0.01em"}, outlined=False)
            solara.Button(label="Login", style={"background": "#e0e7ff", "color": "#2563eb", "font-size": "1.13rem", "box-shadow": "none", "border": "none", "font-weight": "700", "letter-spacing": "0.01em", "border-radius": "7px", "padding": "7px 22px", "margin-left": "18px"}, outlined=False)

# Hero section (formerly Header)
@solara.component
def HeroHeader():
    with solara.Column(style={
        "text-align": "center", 
        "margin-bottom": "50px",
        "padding": "50px 40px",
        "background": "rgba(255, 255, 255, 0.8)",
        "border-radius": "24px",
        "backdrop-filter": "blur(10px)",
        "box-shadow": "0 8px 32px rgba(0, 0, 0, 0.08)"
    }):
        solara.HTML(
            tag="h1",
            unsafe_innerHTML="Reading list favored by top researchers worldwide!",
  
            style={
                "font-size": "3rem",
                "margin-bottom": "20px",
                "color": "#1e293b",
                "font-weight": "800",
                "letter-spacing": "-0.02em",
            }
        )
        solara.HTML(
            tag="p",
            unsafe_innerHTML="<em>Discover the most influential research papers—highly ranked and widely acclaimed by leading experts.</em>",
            style={
                "font-size": "1.4rem", 
                "color": "#475569", 
                "margin": "0",
                "font-weight": "400",
                "max-width": "900px",
                "margin-left": "auto",
                "margin-right": "auto"
            }
        )
