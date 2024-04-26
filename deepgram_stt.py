# !pip install deepgram
# !pip install deepgram-sdk==3.2.7
import requests
import os
import json
from deepgram import DeepgramClient, PrerecordedOptions

from dotenv import load_dotenv

load_dotenv()
deepgram_api_key = os.getenv('deepgram_api_key')
print(deepgram_api_key)

deepgram_api_key = ""

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

AUDIO_FILE = r"C:\Shiva\NP\Teaching Assisstant - AI\AI_ST\AI-powered-Teaching-assisstant\IP.mp3"




def main():
    try:
        deepgram = DeepgramClient(deepgram_api_key)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=False,
        )

        response = deepgram.listen.prerecorded.v("2").transcribe_file(payload, options)
        
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()