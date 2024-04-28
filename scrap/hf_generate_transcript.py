## from hugging face inference API we will generate transcripts for the audio files


from transformers import pipeline
import soundfile as sf


def generate_transcript(audio_file_path):
    # Load the audio file
    data, samplerate = sf.read(audio_file_path)
    duration = len(data) / samplerate

    # Initialize the transcription pipeline
    transcriber = pipeline(
        model="openai/whisper-large-v2", return_timestamps=True, chunk_length_s=30
    )

    # Check if the audio needs to be chunked
    if duration > 30:
        # Calculate the number of chunks needed
        num_chunks = int(duration // 30) + (duration % 30 > 0)
        transcripts = []

        # Process each chunk
        for i in range(num_chunks):
            start = i * 30 * samplerate
            end = min((i + 1) * 30 * samplerate, len(data))
            chunk_data = data[start:end]

            # Save the chunk temporarily to pass to the transcriber
            temp_chunk_path = f"temp_chunk_{i}.wav"
            sf.write(temp_chunk_path, chunk_data, samplerate)

            # Generate transcript for the chunk
            chunk_transcript = transcriber(temp_chunk_path)
            transcripts.append(chunk_transcript)

            # Clean up the temporary file
            os.remove(temp_chunk_path)

        return transcripts
    else:
        # Process the whole file if it's shorter than 30 seconds
        return transcriber(audio_file_path)


# Example usage
audio_path = "path_to_audio_file.wav"
transcripts = generate_transcript(audio_path)
print(transcripts)
