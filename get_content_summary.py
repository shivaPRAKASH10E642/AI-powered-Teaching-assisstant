## with provided summary from the transcript, generate summary for the content, study plan and question and answers
import google.generativeai as genai
import os
import dotenv
import json

dotenv.load_dotenv()
# generate summary from provided text
"""def generate_summary_studyplan_QandA(text, api_key):
    user_prompt = (
        "provide summary, lesson plan and multiple choice questions to below context\n"
        + text
    )
    client = OpenAI(api_key=api_key)
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "you are a helpful teaching assistant, you will help teachers and students in generating summary, lesson plan and question and answers in multiple choice for the provided context.",
                "role": "user",
                "content": user_prompt,
            }
        ],
    )"""


def generate_summary_studyplan_QandA_Gemini(text):
    genai.configure(api_key=os.getenv("GEMINI_PRO_PREVIEW"))
    genai.GenerationConfig(temperature=0.2)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        system_instruction=[
            "you are a helpful teaching assistant, you will be helping students in generating below details from the context provided",
            "1.Title:,2.Summary:,3. Detail notes: and 4.10 multiple choice question and answers",
            "question and answers should contain answer at bottom as 'answer: B' ",
            "the response shoud be in json format with keys as ",
            "Title:",
            "Summary:",
            "Notes:",
            "qanda:",
            "example format for qanda, example: '{'no': 1, 'question': 'What is the capital of France?', 'a': 'Paris', 'b': 'London', 'c': 'Berlin', 'd': 'Madrid', 'answer': 'Paris'}'",
        ],
    )

    prompt = f"provide summary, lesson plan and multiple choice questions to below context. context :{text}"

    response = model.generate_content([prompt])

    if response.text:
        try:
            json_data = response.text.replace("json", "").replace("```", "")
            json_response = json.loads(json_data)
            return (
                json_response.get("Title", "No title"),
                json_response.get("Summary"),
                json_response.get("Notes"),
                json_response.get("qanda"),
            )
        except json.JSONDecodeError:
            print("Failed to decode JSON from response")
        else:
            print("No response text received")


if __name__ == "__main__":
    with open(
        "./test.txt",
        "r",
    ) as file:
        text = file.read()

    lesson_plan = []
    questionAndAnsw = []

    summary, lesson_plan, questionAndAnsw = generate_summary_studyplan_QandA_Gemini(
        text=text
    )
    ##print(summary)
    for plan in lesson_plan:
        print(plan)
