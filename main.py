from flask import Flask, request, send_file
from flask_cors import CORS
from piper import PiperVoice
import wave
import tempfile
import os

app = Flask(__name__)
CORS(app)

voice = PiperVoice.load("/root/sv_SE-nst-medium.onnx")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    output_path = tmp.name

    with wave.open(output_path, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(22050)
        voice.synthesize(text, wav)

    return send_file(output_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
