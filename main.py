from flask import Flask, request, send_file, Response
from flask_cors import CORS
from piper import PiperVoice
import wave
import tempfile

app = Flask(__name__)
CORS(app)

voice = PiperVoice.load("/root/sv_SE-nst-medium.onnx")

@app.route("/")
def index():
    return '''
<!DOCTYPE html>
<html>
<body>
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
</body>
</html>
'''

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    with wave.open(tmp.name, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(voice.config.sample_rate)
        voice.synthesize(text, wav)
    return send_file(tmp.name, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
