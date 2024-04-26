import requests
import youtube_dl
import os
from openai import OpenAI


def audio_to_text_with_timestamps(file_path, openai_api_key):
  client = OpenAI(api_key= openai_api_key)
  audio_file= open(f"{file_path}", "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["segment"]

    )

  return transcription