import gradio as gr
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def chat(input_text):
    result = generator(input_text, max_length=50)
    return result[0]['generated_text']

iface = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="Type your message"),
    outputs=gr.Textbox(label="Bot reply"),
    title="The Third Voice Chatbot"
)

iface.launch(server_name="0.0.0.0", server_port=10000)
