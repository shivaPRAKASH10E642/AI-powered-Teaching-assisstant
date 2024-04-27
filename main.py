from deepgram_stt import *
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
doc(mcq_summ,"MCQ")