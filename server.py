from flask import Flask, request, jsonify
import openai, os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return jsonify(completion.choices[0].message)

@app.route("/", methods=["GET"])
def home():
    return "✅ ChatGPT Proxy is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
