# !pip install deepgram
# !pip install deepgram-sdk==3.2.7
import requests
import json
from deepgram import DeepgramClient, PrerecordedOptions
deepgram_api_key = '3935a1a64b88c5ad5fced77f93bd796c93399553'


from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

AUDIO_FILE = r"C:\Shiva\NP\Teaching Assisstant - AI\IP.mp3"


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

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()