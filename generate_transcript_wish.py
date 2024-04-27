import openai
import dotenv
import os
from pydub import AudioSegment

## load the env variables
dotenv.load_dotenv()

## initialize the openai client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


## get the transcript using the whisper model
def get_transcript_with_segments(audio_file_path, client):
    # generate the transcript
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file_path,
        response_format="verbose_json",
        timestamp_granularities=["segment"],
    )
    return transcript.text, transcript.segments


## slice the input audio file if the file is larger than 25MB using python library pydub
def slice_audio_file(audio_file_path):
    # Define the maximum file size in bytes (25MB)
    max_file_size = 25 * 1024 * 1024  # 25MB in bytes
    audio = AudioSegment.from_file(audio_file_path)

    # Calculate the duration in milliseconds that corresponds to the maximum file size
    # Assuming the bit rate is 256 kbps, which is a common bit rate for MP3 files
    # Bit rate (kbps) / 8 = kBps; Duration (seconds) = File size (kB) / kBps
    bytes_per_second = (audio.frame_rate * audio.frame_width * audio.channels) / 8
    max_duration = int(
        (max_file_size / bytes_per_second) * 1000
    )  # Convert to milliseconds

    chunks = []
    for i in range(0, len(audio), max_duration):
        # Avoid cutting the audio in the middle of a sentence by finding the nearest silence
        # before the max_duration limit
        silence_threshold = -40  # dBFS, may need adjustment based on the audio file
        silence_chunk = audio[i : i + max_duration].split_to_mono()[0]
        silence_pos = silence_chunk.detect_silence(
            min_silence_len=1000, silence_thresh=silence_threshold
        )

        if silence_pos:
            nearest_silence_end = silence_pos[-1][
                1
            ]  # Get the end position of the last silence
        else:
            nearest_silence_end = max_duration

        end = min(i + nearest_silence_end, len(audio))
        chunk = audio[i:end]
        chunks.append(chunk)

        # Update the start position for the next chunk
        i = end

    # Export chunks to files
    chunk_files = []
    for index, chunk in enumerate(chunks):
        chunk_file_path = f"{audio_file_path[:-4]}_chunk{index}.mp3"
        chunk.export(chunk_file_path, format="mp3")
        chunk_files.append(chunk_file_path)

    return chunk_files


def post_transcript_correction(transcript, client):
    # Send the corrected transcript to GPT-3.5-turbo for correction and enhancement
    correction_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for correcting grammar and spelling errors in the transcript.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return correction_response.choices[0].message.content


## generate the transcript and process the audio file
def generate_transcript_and_process(audio_file_path, client):
    ## check if the audio file is larger than 25MB, if it is, slice the audio file and generate the
    # transcript for each chunk. else generate the transcript for the whole audio file
    transcript = ""
    segments = []

    ## open file in bytes
    with open(audio_file_path, "rb") as audio_file:
        ## check if the audio file is larger than 25MB
        if os.path.getsize(audio_file_path) > 25 * 1024 * 1024:
            # slice the audio file
            chunk_files = slice_audio_file(audio_file_path)
            # generate the transcript for each chunk

            for chunk_file in chunk_files:
                chunk_transcript, chunk_segments = get_transcript_with_segments(
                    chunk_file, client
                )
                transcript += chunk_transcript
                segments += chunk_segments
        else:
            transcript, segments = get_transcript_with_segments(audio_file, client)

    return transcript, segments


# Example usage


audio_path = "How To Learn Data Science Smartly [TubeRipper.com].mp3"

transcript, segments = generate_transcript_and_process(audio_path, client)

## send the transcripts to the post_transcript_correction function
corrected_transcript = post_transcript_correction(transcript, client)

## correct each segment of the transcripts passing to the post_transcript_correction function
for segment in segments:
    segment["text"] = post_transcript_correction(segment["text"], client)


## write transcripts to a text file as transcripts.txt
with open("transcripts.txt", "w") as file:
    file.write(corrected_transcript)

## write segments to a text file as segments.txt along with the start and end time of each segment
with open("segments.txt", "w") as file:
    for segment in segments:
        file.write(f"{segment['start']} - {segment['end']}: {segment['text']}\n")
