FROM huggingface/transformers-pytorch-gpu

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r pyproject.toml

CMD ["python3", "transcribe_videos.py"]
