import solara

@solara.component
def SearchBar(search_query, on_search, is_searching, selected_database, ranking_criteria):
    with solara.Card(style={
        "padding": "32px 40px 24px 40px",
        "border-radius": "22px",
        "box-shadow": "0 6px 32px rgba(59, 130, 246, 0.13)",
        "background": "linear-gradient(90deg, #f1f5f9 0%, #e0e7ff 100%)",
        "margin-bottom": "36px",
        "border": "1.5px solid #c7d2fe",
        "position": "relative"
    }):
        # Database selection as button array at top right
        database_options = ["arXiv", "PubMed", "IEEE"]
        with solara.Row(style={
            "position": "absolute",
            "top": "16px",
            "right": "36px",
            "gap": "6px",
            "z-index": 2,
            "background": "transparent",
            "padding": "2px 10px",
            "border-radius": "8px",
            "box-shadow": "0 1px 4px rgba(59,130,246,0.07)",
            "align-items": "center"
        }):
            solara.HTML(tag="span", unsafe_innerHTML="<strong style='font-size:1.28rem;color:#2563eb;'>Databases:</strong>")
            button_width = "100px"  # Wide enough for 'IEEE Xplore'
            for db in database_options:
                custom_class = f"db-btn-{db.replace(' ', '-').lower()}"
                is_selected = selected_database.value == db
                solara.Button(
                    label=db,
                    outlined=False,
                    color="#2563eb" if is_selected else "#cbd5e1",
                    classes=[custom_class, "db-btn-shared"],
                    style={
                        "font-size": "0.98rem",
                        "font-weight": "600",
                        "border-radius": "7px",
                        "padding": "3px 12px",
                        "background": "linear-gradient(90deg, #2563eb 0%, #3b82f6 70%, #f1f5f9 100%)" if is_selected else "#f1f5f9",
                        "border": "none",
                        "color": "#f4f5f8" if is_selected else "#64748b",
                        "width": button_width,
                        "min-width": button_width,
                        "max-width": button_width,
                        "text-transform": "none",
                        "transition": "background 0.18s, color 0.18s"
                    },
                    on_click=lambda db=db: selected_database.set(db)
                )
            # Add custom CSS for hover and selected effect (no border)
            solara.HTML(unsafe_innerHTML="""
            <style>
            .db-btn-shared.selected, .db-btn-arxiv.selected, .db-btn-pubmed.selected, .db-btn-ieee-xplore.selected {
                background: linear-gradient(90deg, #2563eb 0%, #3b82f6 70%, #f1f5f9 100%) !important;
                color: #f4f5f8 !important;
                border: none !important;
            }
            .db-btn-shared:hover:not(.selected), .db-btn-arxiv:hover:not(.selected), .db-btn-pubmed:hover:not(.selected), .db-btn-ieee-xplore:hover:not(.selected) {
                background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 70%, #f1f5f9 100%) !important;
                color: #f4f5f8 !important;
                border: none !important;
            }
            </style>
            """)
    
        solara.HTML(tag="div", style={"height": "38px"})
        with solara.Row(style={
            "gap": "10",
            "align-items": "center",
            "margin-bottom": "8px",
            "flex-wrap": "wrap",
            "background": "#f8fafc",
            "border-radius": "10px",
            "padding": "0",
            "box-shadow": "0 1px 4px rgba(0,0,0,0.04)",
            "border": "1.5px solid #cbd5e1",
            "overflow": "hidden",
            "width": "70%",

        }):
            solara.InputText(
                label="Interested topics or keywords...",
                value=search_query.value,
                on_value=search_query.set,
                style={
                    "border": "none",
                    "box-shadow": "none",
                    "background": "#f8fafc",
                    "font-size": "1.18rem",
                    "padding": "18px 18px 18px 18px",
                    "border-radius": "10px 0 0 10px",
                    "min-width": "0",
                    "flex": 1
                }
            )
            solara.Button(
                label="Search",
                icon_name="mdi-magnify",
                on_click=on_search,
                disabled=is_searching.value,
                classes=["search-btn"],
                style={
                    "padding": "18px 28px",
                    "font-size": "1.1rem",
                    "border-radius": "0 10px 10px 0",
                    "background": "linear-gradient(90deg, #2563eb 0%, #60a5fa 100%)",
                    "color": "#fff",
                    "box-shadow": "none",
                    "font-weight": "700",
                    "letter-spacing": "0.01em",
                    "border": "none",
                    "height": "48px"
                }
            )
        #    # Ranking dropdown
        #     ranking_options = [
        #         ("AI ranking", "AI Ranking"),
        #         ("relevance", "Relevance"),
        #         ("citations", "Citations"),
        #         ("submittedDate", "Date (Submitted)")
        #     ]
        #     display_values = [label for value, label in ranking_options]
        #     value_map = {label: value for value, label in ranking_options}
        #     current_label = next((label for value, label in ranking_options if value == (ranking_criteria.value or "relevance")), "Relevance")
        #     def on_ranking_change(label):
        #         ranking_criteria.set(value_map[label])
        #     solara.Select(
        #         label="Ranking",
        #         value=current_label,
        #         values=display_values,
        #         on_value=on_ranking_change,
        #         style={
        #             "border-radius": "10px",
        #             "background": "#f1f5f9",
        #             "font-size": "1.08rem",
        #             "border": "1.5px solid #cbd5e1",
        #             "transition": "background 0.18s, color 0.18s"
                    
        #         }
        #     )
        #     solara.HTML(unsafe_innerHTML="""
        #     <style>
        #     .solara-select__option:hover, .solara-select__option[aria-selected="true"] {
        #         background: #f1f5f9 !important;
        #         color: #f1f5f9  !important;
        #         border-radius: 8px !important;
        #     }
        #     </style>
        #     """)

        # Third row: Example search tokens
        with solara.Row(style={
            "gap": "10px",
            "align-items": "center",
            "margin-bottom": "0",
            "flex-wrap": "wrap",
            "background": "transparent",
            "border-radius": "12px",
            "padding": "18px 28px",
            "box-shadow": "none",
            "width": "100%",
            "max-width": "600px"
        }):
            solara.HTML(
                tag="span",
                unsafe_innerHTML="<strong>Examples:</strong> <span style='color:#64748b'>large language model</span>, <span style='color:#64748b'>agentic AI</span>, <span style='color:#64748b'>RAG</span>",
                style={
                    "font-size": "1.13rem",
                    "font-style": "italic",
                    "color": "#334155"
                }
            )
