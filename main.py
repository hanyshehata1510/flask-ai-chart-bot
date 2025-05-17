from flask import Flask, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

latest_analysis = ""

@app.route('/analyze', methods=['POST'])
def analyze():
    global latest_analysis
    data = request.get_json()

    message = data.get("message", "No message received.")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional market analyst. Provide a short, clear technical analysis based on this OHLCV data."},
            {"role": "user", "content": f"Analyze this chart data:\n{message}"}
        ]
    )

    latest_analysis = response["choices"][0]["message"]["content"]
    print("AI Analysis:", latest_analysis)

    return {"status": "ok", "analysis": latest_analysis}

@app.route('/latest-analysis')
def latest():
    return latest_analysis or "Waiting for data..."
