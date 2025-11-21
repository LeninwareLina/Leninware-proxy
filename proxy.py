from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TRANSCRIPT_API_KEY = os.getenv("TRANSCRIPT_API_KEY")

TRANSCRIPT_ENDPOINT = "https://api.transcriptapi.com/api/v1/transcript"

@app.route("/transcript", methods=["GET"])
def transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id parameter"}), 400

    if not TRANSCRIPT_API_KEY:
        return jsonify({"error": "Missing TRANSCRIPT_API_KEY"}), 500

    # Call TranscriptAPI
    url = f"{TRANSCRIPT_ENDPOINT}/{video_id}"
    headers = {"Authorization": f"Bearer {TRANSCRIPT_API_KEY}"}

    try:
        r = requests.get(url, headers=headers)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": f"Proxy request failed: {str(e)}"}), 500


@app.route("/")
def root():
    return "Transcript Proxy Online"