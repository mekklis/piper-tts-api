from flask import Flask, request, send_file
from piper import PiperVoice
import wave
import tempfile
import os

app = Flask(__name__)
voice = PiperVoice.load("/root/sv_SE-nst-medium.onnx")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        output_path = f.name
        with wave.open(f, "wb") as wav:
            voice.synthesize(text, wav)

    return send_file(output_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
