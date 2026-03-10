import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

from flask import Flask, request, jsonify
from flask_cors import CORS

from app.agent.graph import agent
from app.agent.state import SarthiState

app = Flask(__name__)
CORS(app)  # allows your frontend to call this from any origin


# -------------------------
# POST /api/message
# Body: { "question": "What is dharma?" }
# -------------------------
@app.route("/api/message", methods=["POST"])
def message():
    data = request.get_json()

    if not data or not data.get("question", "").strip():
        return jsonify({"error": "question is required"}), 400

    question = data["question"].strip()

    initial_state = SarthiState(question=question)
    final_state = agent.invoke(initial_state)
    answer = final_state["answer"]

    return jsonify({"answer": answer})


# -------------------------
# Health check
# -------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)