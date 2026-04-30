@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    
    audio_bytes = b""
    for audio_bytes_chunk in voice.synthesize_stream_raw(text):
        audio_bytes += audio_bytes_chunk
    
    with wave.open(tmp.name, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(22050)
        wav.writeframes(audio_bytes)
    
    return send_file(tmp.name, mimetype="audio/wav")
