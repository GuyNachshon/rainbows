import os
import json
import subprocess
from multiprocessing import Pool
from tqdm import tqdm
from transformers import pipeline
import torch
import soundfile as sf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
DOWNLOAD_DIR = os.path.join(DATA_DIR, 'downloads')
TRANSCRIPTIONS_DIR = os.path.join(DATA_DIR, 'transcriptions')

# Use GPU if available
device = 0 if torch.cuda.is_available() else -1

# Load the transcription pipeline
pipe = pipeline(
    "automatic-speech-recognition",
    model="ivrit-ai/whisper-large-v3-tuned",
    device=device
)

def transcribe_video(video_filename):
    os.makedirs(TRANSCRIPTIONS_DIR, exist_ok=True)
    video_path = os.path.join(DOWNLOAD_DIR, video_filename)
    video_id = os.path.splitext(video_filename)[0]
    transcription_path = os.path.join(TRANSCRIPTIONS_DIR, f"{video_id}.txt")

    if os.path.exists(transcription_path):
        print(f"Transcription for {video_id} already exists. Skipping.")
        return

    try:
        # Extract audio from video
        audio_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.wav")
        command = ['ffmpeg', '-i', video_path, '-ac', '1', '-ar', '16000', audio_path]
        subprocess.run(command, check=True, capture_output=True, text=True)

        # Transcribe the audio
        transcription = pipe(audio_path)["text"]

        # Save the transcription
        with open(transcription_path, 'w', encoding='utf-8') as f:
            f.write(transcription)

        print(f"Successfully transcribed {video_id}")

        # Clean up the audio file
        os.remove(audio_path)

    except Exception as e:
        print(f"Error transcribing {video_id}: {e}")

def main():
    video_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.endswith('.mp4')]

    with Pool() as pool:
        list(tqdm(pool.imap(transcribe_video, video_files), total=len(video_files), desc="Transcribing videos"))

if __name__ == "__main__":
    main()
