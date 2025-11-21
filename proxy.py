from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TRANSCRIPT_API_KEY = os.getenv("TRANSCRIPT_API_KEY")
BASE_URL = "https://api.transcriptapi.com/api/v1/transcript"

@app.route("/")
def home():
    return "Leninware Transcript Proxy is running."

@app.route("/youtube/<video_id>", methods=["GET"])
def youtube(video_id):
    if not TRANSCRIPT_API_KEY:
        return jsonify({"error": "Missing TRANSCRIPT_API_KEY"}), 500

    headers = {"X-Api-Key": TRANSCRIPT_API_KEY}
    url = f"{BASE_URL}/{video_id}"

    try:
        response = requests.get(url, headers=headers, timeout=20)

        try:
            data = response.json()
        except ValueError:
            return jsonify({
                "error": "Transcript API returned non-JSON data",
                "raw": response.text
            }), 500

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": "Proxy request failed",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)