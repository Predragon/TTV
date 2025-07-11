import gradio as gr
from transformers import pipeline
import os

# Load a lightweight local model
generator = pipeline("text-generation", model="distilgpt2")

def chat(input_text):
    # Generate a response using the local model
    response = generator(input_text, max_length=60, num_return_sequences=1)
    return response[0]['generated_text']

iface = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="Type your message"),
    outputs=gr.Textbox(label="Bot reply"),
    title="The Third Voice Chatbot",
    description="A simple chatbot powered by DistilGPT2. No API key needed."
)

port = int(os.environ.get("PORT", 10000))
iface.launch(server_name="0.0.0.0", server_port=port)
