import json
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import os
import dotenv
from pytube import YouTube

dotenv.load_dotenv()


def get_transcripts_from_url(audio_file_url):
    """Read the input audio file from a provided URL and generate the transcripts along with the segments."""
    audio_file_path = get_youtube_audio(audio_file_url)
    print(audio_file_path)
    with open(audio_file_path, "rb") as file:
        buffered_data = file.read()

    return get_transcripts_from_file(buffered_data)


def get_transcripts_from_file(buffer_data):
    """Read the input audio file uploaded to local and generate the transcripts along with the segments."""
    try:
        deepgram_client = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2", smart_format=False, paragraphs=True, summarize="v2"
        )

        response = deepgram_client.listen.prerecorded.v("1").transcribe_file(
            payload, options
        )

        transcript = ""
        sentences = []

        trans_data = json.loads(response.to_json(indent=4))
        # Extracting the required information
        for channel in trans_data["results"]["channels"]:
            for alternative in channel["alternatives"]:
                transcript = alternative["transcript"]
                for paragraph in alternative["paragraphs"]["paragraphs"]:
                    sentences = paragraph["sentences"]

        return transcript, sentences

    except Exception as e:
        print(f"Exception getting transcripts from file: {e}")
        return e


def get_youtube_audio(url):
    """Download the audio file from the URL using PyTube."""
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Filter streams to get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Set the output file name and path
        output_file_name = os.path.join("./Data/test_videos/", f"{yt.title}.mp3")

        # Download the audio stream
        audio_stream.download(
            # output_path="./Data/test_videos/",
            filename=output_file_name,
        )

        return output_file_name
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
        return None


if __name__ == "__main__":
    audio_file_url = "https://www.youtube.com/watch?v=CHW5SExulzI&t=1799s"
    transcript, sentences = get_transcripts_from_url(
        audio_file_url, os.getenv("DEEPGRAM_API_KEY")
    )
    print(transcript)

    ## print(f"Transcripts: {trans_data['results']['channels'](0)['alternatives']['transcript']}")

    # Extracting the required information
    """_summary_
    for channel in trans_data["results"]["channels"]:
    for alternative in channel["alternatives"]:
        print("Transcript:", alternative["transcript"])
        print("Paragraphs:")
        for paragraph in alternative["paragraphs"]["paragraphs"]:
            for sentence in paragraph["sentences"]:
                print(f"  Text: {sentence['text']}")
                print(f"  Start Time: {sentence['start']}s")
                print(f"  End Time: {sentence['end']}s")"""
