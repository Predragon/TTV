import gradio as gr
from transformers import pipeline
import os

# Load a lightweight local model for rewriting
rewrite_pipeline = pipeline("text-generation", model="distilgpt2")

def rewrite_message(message, tone):
    prompt = f"Rewrite this message in a {tone} tone:\n{message}\n"
    result = rewrite_pipeline(prompt, max_length=80, num_return_sequences=1)
    rewritten = result[0]["generated_text"].replace(prompt, "").strip()
    return rewritten

def analyze_tone(message):
    # Simple rule-based analysis
    msg = message.lower()
    if any(word in msg for word in ["angry", "upset", "frustrated"]):
        analysis = "They might be feeling upset or frustrated."
    elif any(word in msg for word in ["thanks", "thank", "grateful"]):
        analysis = "They might be feeling appreciative or thankful."
    elif any(word in msg for word in ["sorry", "apologize"]):
        analysis = "They might be feeling regretful or apologetic."
    else:
        analysis = "Their feelings are not clear. Consider context or ask for clarification."
    return analysis

with gr.Blocks(theme=gr.themes.Monochrome(), css="""
body { background-color: #1a1a2e !important; }
.gradio-container { background-color: #2a2a4a !important; color: #e0e0e0 !important; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.4);}
h1, .gradio-container h1 { color: #e94560 !important; font-family: 'Playfair Display', serif; }
label, .gradio-label { color: #a0a0a0 !important; font-weight: 700; }
textarea, select, .gr-input, .gr-textbox { background-color: #16213e !important; color: #e0e0e0 !important; border-radius: 8px !important; }
button, .gr-button { background-color: #e94560 !important; color: white !important; border-radius: 8px !important; font-weight: 700 !important; }
button:hover, .gr-button:hover { background-color: #ff6a80 !important; }
.suggestion-box { background-color: #3e3e5e !important; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 5px solid #e94560; color: #c0c0d0 !important; font-size: 0.95em; }
""") as demo:
    gr.Markdown("""
    # The Third Voice AI
    Rewrite your messages for clarity, tone, and impact. Analyze what the other person might be feeling.
    """)
    with gr.Row():
        with gr.Column():
            gr.Markdown("**Your Message:**")
            message_input = gr.Textbox(lines=4, placeholder="Enter your message here...")
            gr.Markdown("**Desired Tone:**")
            tone_select = gr.Dropdown(
                ["Professional", "Friendly", "Assertive", "Empathetic", "Concise", "Neutral"],
                value="Professional",
                label=None
            )
            rewrite_btn = gr.Button("Rewrite Message")
            rewritten_output = gr.Textbox(label="Rewritten Message", elem_classes="suggestion-box")
        with gr.Column():
            gr.Markdown("**Message You Received:**")
            incoming_input = gr.Textbox(lines=4, placeholder="Paste their message here...")
            analyze_btn = gr.Button("Analyze Tone and Feelings")
            analysis_output = gr.Textbox(label="Analysis", elem_classes="suggestion-box")
    # Actions
    rewrite_btn.click(
        rewrite_message,
        inputs=[message_input, tone_select],
        outputs=rewritten_output
    )
    analyze_btn.click(
        analyze_tone,
        inputs=incoming_input,
        outputs=analysis_output
    )

port = int(os.environ.get("PORT", 10000))
demo.launch(server_name="0.0.0.0", server_port=port)
            
