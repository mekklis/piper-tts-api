FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L --retry 5 --retry-delay 3 \
    https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz \
    -o piper.tar.gz \
    && tar -xzf piper.tar.gz \
    && mv piper/piper /usr/local/bin/piper \
    && rm -rf piper.tar.gz piper

RUN wget --tries=5 \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx \
    -O /root/sv_SE-nst-medium.onnx \
    && wget --tries=5 \
    https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json \
    -O /root/sv_SE-nst-medium.onnx.json

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY main.py .

EXPOSE 10000
CMD ["python3", "main.py"]
