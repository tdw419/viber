
from flask import Flask, request, jsonify
import extension

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello, World!"

@app.route("/mcp.rag", methods=["POST"])
def handle_rag():
    data = request.get_json()
    subcommand = data.get("subcommand")
    if subcommand == "query":
        query = data.get("query")
        # Since rag_search now returns a list of dicts, it's jsonify-able
        results = extension.rag_search(query)
        return jsonify(results)
    elif subcommand == "add":
        file_path = data.get("file_path")
        # Ensure file exists before proceeding
        if file_path:
            extension.rag_add(file_path)
            return jsonify({"status": "success", "message": f"Added {file_path}"})
        else:
            return jsonify({"error": "file_path is required for add"}), 400
    else:
        return jsonify({"error": "Invalid subcommand"}), 400

if __name__ == "__main__":
    app.run(port=5000, debug=True)
