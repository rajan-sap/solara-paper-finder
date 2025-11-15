import solara

@solara.component
def PaperChatModal(open, on_close, paper_title, chat_history, on_send):
    with solara.Dialog(open=open, on_close=on_close, style={"min-width": "420px", "max-width": "600px"}):
        solara.HTML(tag="h3", unsafe_innerHTML=f"Chat about: <span style='color:#2563eb'>{paper_title}</span>", style={"margin-bottom": "12px", "font-size": "1.25rem"})
        with solara.Column(style={"max-height": "320px", "overflow-y": "auto", "background": "#f8fafc", "border-radius": "8px", "padding": "12px", "margin-bottom": "10px", "border": "1px solid #e0e7ff"}):
            for msg in chat_history:
                solara.HTML(tag="div", unsafe_innerHTML=f"<b>{msg['role'].capitalize()}:</b> {msg['content']}", style={"margin-bottom": "8px", "color": "#334155" if msg['role']=="user" else "#2563eb"})
        with solara.Row():
            user_input, set_user_input = solara.use_state("")
            solara.InputText(label="Type your message...", value=user_input, on_value=set_user_input, style={"flex":1})
            solara.Button(label="Send", on_click=lambda: on_send(user_input) if user_input.strip() else None, disabled=not user_input.strip(), style={"margin-left": "8px"})
