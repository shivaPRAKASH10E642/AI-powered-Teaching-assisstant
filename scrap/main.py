"""from deepgram_stt import *
from chat import *
from op_process import *
from dotenv import load_dotenv

#add your keys here
load_dotenv()
openai_api_key = os.getenv(openai_api_key)
deepgram_api_key = os.getenv(deepgram_api_key)

#Function calling and processing
path_to_file = "ip_krishnaik_langchain.mp3"
op = deepgram(path_to_file,deepgram_api_key)
op_processed = process_json_op(op)
doc(op_processed,"processed_from_deepgram")
system_prompt = "You are a good in creating detailed notes from audio transcripts along with timestamps. Please capture details of every concept that is being discussed in the transcript. Please dont summarize. Write it out as you were listening to the lecture"
user_prompt = f"{op_processed}"
summary = chat(user_prompt, system_prompt, openai_api_key)
doc(summary,"OPFILE")
mcq_system_prompt = "You are good at analysing a given text and come up with 10 multiple choice questions that covers the entire topic. Take time to go through the topic"
mcq_summ = chat(user_prompt, mcq_system_prompt, openai_api_key)
doc(mcq_summ,"MCQ")"""

from get_content_summary import generate_summary_studyplan_QandA_Gemini
from get_transcripts import get_transcripts_from_file, get_transcripts_from_url
import os
import dotenv

dotenv.load_dotenv()

### on main function start
if __name__ == "__main__":
    sentences = [], transcripts = "",summary="",lesson_plan=[],MAQ=[]  # noqa: E999
    try:
        if "https:" in input:
            transcripts, sentences = get_transcripts_from_url(
                input, os.getenv("DEEPGRAM_API_KEY")
            )
        else:
            transcripts, sentences = get_transcripts_from_file(
                input, os.getenv("DEEPGRAM_API_KEY")
            )
    except Exception as e:
        print(f"Error getting transacripts, sentences. error is: {str(e)}")

    try:
        summary,lesson_plan,MAQ=generate_summary_studyplan_QandA_Gemini(transcripts)

    except Exception as e:
        print(f"error at retrvie info from gemini. {str(e)}")
