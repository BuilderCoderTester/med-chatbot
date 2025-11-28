from flask import Flask, request, jsonify
from flask_cors import CORS
# from pipeline import rag_chain  # RAG chain already created at import time
from rag.rag_module import query_rag_chain 
from pipeline import ask_question

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Question is required"}), 400

        response = ask_question(question)
        print(response)
        # Expected format from your Gemini RAG setup
        answer = response.get("answer") or response.get("output") or ""

        return jsonify({"answer": answer})

    except Exception as e:
        print("💥 Backend error:", e)
        return jsonify({"error": "Internal server error"}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "RAG Medical Chatbot API is running"})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
