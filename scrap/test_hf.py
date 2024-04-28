import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def generate_transcripts(audio_file_path):
    # Load the model and processor
    model_id = "openai/whisper-large-v3"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id).to(device)
    processor = AutoProcessor.from_pretrained(model_id)

    # Create a pipeline for automatic speech recognition
    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        device=device,
    )

    # Process the audio file
    transcription_result = asr_pipeline(audio_file_path, return_timestamps="sentence")

    # Extract complete transcript
    complete_transcript = transcription_result["text"]

    # Extract topic-wise paragraphs with timestamps
    topic_paragraphs = []
    for chunk in transcription_result["chunks"]:
        topic_paragraphs.append(
            {
                "text": chunk["text"],
                "start_time": chunk["start"],
                "end_time": chunk["end"],
            }
        )

    return complete_transcript, topic_paragraphs


# Example usage:
audio_path = "How To Learn Data Science Smartly [TubeRipper.com].mp3"
transcripts, topics = generate_transcripts(audio_path)
print("Complete Transcript:", transcripts)
print("Topic-wise Paragraphs with Timestamps:", topics)
