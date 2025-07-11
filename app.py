from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# Load a local model for rewriting (DistilGPT2 is lightweight)
rewrite_pipeline = pipeline("text-generation", model="distilgpt2")

# --- Routes ---

@app.route("/")
def root():
    return send_from_directory(".", "index4.html")

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.get_json()
    message = data.get("message", "")
    tone = data.get("tone", "neutral")
    # Simple prompt engineering for tone (customize as needed)
    prompt = f"Rewrite this message in a {tone} tone:\n{message}\n"
    result = rewrite_pipeline(prompt, max_length=80, num_return_sequences=1)
    rewritten = result[0]["generated_text"].replace(prompt, "").strip()
    return jsonify({"rewrittenText": rewritten})

@app.route("/analyze-tone", methods=["POST"])
def analyze_tone():
    data = request.get_json()
    message = data.get("message", "")
    # Simple rule-based tone analysis (replace with ML if desired)
    if any(word in message.lower() for word in ["angry", "upset", "frustrated"]):
        analysis = "They might be feeling upset or frustrated."
    elif any(word in message.lower() for word in ["thanks", "thank", "grateful"]):
        analysis = "They might be feeling appreciative or thankful."
    elif any(word in message.lower() for word in ["sorry", "apologize"]):
        analysis = "They might be feeling regretful or apologetic."
    else:
        analysis = "Their feelings are not clear. Consider context or ask for clarification."
    return jsonify({"analysis": analysis})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
           
