import gradio as gr
import os

def chat(input_text):
    return f"You said: {input_text}"

iface = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="Type your message"),
    outputs=gr.Textbox(label="Bot reply"),
    title="The Third Voice Chatbot"
)

port = int(os.environ.get("PORT", 10000))
iface.launch(server_name="0.0.0.0", server_port=port)
