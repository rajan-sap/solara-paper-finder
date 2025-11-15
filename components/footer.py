import solara

@solara.component
def Footer():
    with solara.Column(style={
        "text-align": "center",
        "width": "100%",
        "position": "absolute",
        "left": 0,
        "bottom": 0,
        "padding": "18px 0 18px 0",
        "color": "#64748b",
        "font-size": "1.1rem",
        "background": "rgba(255,255,255,0.95)",
        "z-index": 100
    }):
        solara.HTML(
            tag="footer",
            unsafe_innerHTML="&copy; 2025 TopRead. Made to deliver the top read. <span style='color:#60a5fa'>&#10084;</span> ",
        )
