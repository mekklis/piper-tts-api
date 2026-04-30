from flask import Flask, request, send_file
from flask_cors import CORS
import tempfile
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return '''<!DOCTYPE html><html><body>
  <h2>Testa Piper TTS</h2>
  <textarea id="text" rows="4" cols="50">Hello this is a test</textarea>
  <br><br>
  <button onclick="speak()">Spela upp</button>
  <audio id="audio" controls></audio>
  <script>
    async function speak() {
      const text = document.getElementById("text").value;
      const response = await fetch("/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      document.getElementById("audio").src = url;
      document.getElementById("audio").play();
    }
  </script>
</body></html>'''

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    
    result = subprocess.run(
        ["python3", "-m", "piper", "--model", "/root/sv_SE-nst-medium.onnx", "--output_file", tmp.name],
        input=text.encode(),
        capture_output=True
    )
    
    return send_file(tmp.name, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
