# !pip install deepgram
# !pip install deepgram-sdk==3.2.7
import requests
import os
import json
from deepgram import DeepgramClient, PrerecordedOptions
from dotenv import load_dotenv

# The API key we created in step 3
deepgram_api_key = ''
# Replace with your file path
path_to_file = 'input_audio.mp3'

def deepgram(path_to_file,deepgram_api_key):
    deepgram = DeepgramClient(deepgram_api_key)

    with open(path_to_file, 'rb') as buffer_data:
        payload = { 'buffer': buffer_data }

        options = PrerecordedOptions(
            smart_format=True, model="nova-2", language="en-US", paragraphs = True
        )

        print('Requesting transcript...')
        print('Your file may take up to a couple minutes to process.')
        response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)
        print(response.to_json(indent=4))
        return response.to_json(indent=4)
