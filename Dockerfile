FROM ghcr.io/rhasspy/piper:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx \
    -O /root/sv_SE-nst-medium.onnx \
    && wget https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json \
    -O /root/sv_SE-nst-medium.onnx.json

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY main.py .

EXPOSE 10000
CMD ["python3", "main.py"]
