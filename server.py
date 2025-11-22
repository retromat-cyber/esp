from flask import Flask, request, jsonify
import openai
import os
import base64

app = Flask(__name__)

# Новый клиент OpenAI (новый SDK)
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# -----------------------------  
# 📌 1) Эндпоинт чата (обновлённый)
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Лучше, быстрее, дешевле 
        messages=messages
    )

    # Всегда возвращаем unified формат
    return jsonify({
        "content": completion.choices[0].message["content"]
    })

# -----------------------------  
# 📌 2) Эндпоинт активации по слову "chatgpt"
# -----------------------------
@app.route("/wake", methods=["POST"])
def wake_word_detect():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400

    file = request.files["file"]
    audio_bytes = file.read()

    # Отправляем wav/mp3 прямо как байты
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-tts",  # Whisper V3 встроенный
        file=("wake.wav", audio_bytes)  # важно передать (имя, байты)
    )

    text = transcript.text.lower()
    wake_word = "chatgpt"
    activated = wake_word in text

    return jsonify({
        "text": text,
        "wake": activated
    })

# -----------------------------  
# 📌 3) Эндпоинт проверки сервера
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return "✅ ChatGPT Voice Server is running!"

# -----------------------------  
# 📌 Запуск
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
