FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install piper-tts

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .

RUN python3 -c "from piper import PiperVoice; import urllib.request; \
    urllib.request.urlretrieve('https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx', '/root/sv_SE-nst-medium.onnx'); \
    urllib.request.urlretrieve('https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json', '/root/sv_SE-nst-medium.onnx.json')"

EXPOSE 10000
CMD ["python3", "main.py"]
