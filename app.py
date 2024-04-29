import streamlit as st
import docx
import io
import get_content_summary
from get_content_summary import generate_summary_studyplan_QandA_Gemini
from get_transcripts import get_transcripts_from_file, get_transcripts_from_url

# Sample data
questions = []
content_title, summary, Notes = "", "", ""

# Initialize score
score = 0
answer = ["", "", "", "", "", "", "", "", "", ""]
i = 0


st.set_page_config(page_title="Dhrona.ai", page_icon="🏹")
st.title("🏹 Dhrona.ai 🏹 ")
# st.subheader('Your personalized teaching assistant by AI Anamolies')

default_title = "This is where title of your for the uploaded lecture gets published"
default_lessonplan = "This is where the default lesson plan gets uploaded"
default_notes = "This is where the notes get published"

ss = st.session_state


with st.sidebar:
    with st.form("config"):
        st.header("Upload here")
        yturl = st.text_input("Enter YouTube URL ")
        st.subheader("or")
        audiofile = st.file_uploader("Please choose a file")
        # st.subheader("or")
        # driveurl = st.text_input("Enter location of the file")
        submit1 = st.form_submit_button("submit")
    if submit1:
        if yturl:
            # transcript = extract_youtube_transcript(url)
            transcripts, sentences = get_transcripts_from_url(audio_file_url=yturl)
            content_title, summary, Notes, questions = (
                get_content_summary.generate_summary_studyplan_QandA_Gemini(transcripts)
            )
            ##st.write("Text Summary:")
            # st.write(transcript)
        elif audiofile:
            # transcript = extract_pdf_text(url)
            ##st.write("Text Summary:")
            # st.write(transcript)
            audio_bytes = audiofile.read()
            transcripts, sentences = get_transcripts_from_file(audio_bytes)
            content_title, summary, Notes, questions = (
                generate_summary_studyplan_QandA_Gemini
            )

        else:
            st.write("Please enter a valid YouTube URL or file URL.")

st.info(
    """
[Dhrona.ai](https://github.com/xleven/ai-hackathon-judge) is a personalized teaching assistant
built by AI anomalies : [Siddartha](https://github.com/xleven) & [Shiva](https://github.com/langchain-ai/langchain) with [Streamlit](https://streamlit.io).
""",
    icon="ℹ️",
)

st.info(
    """
All you need to do is upload an Youtube url or audio file of your lecture. "Dhron" will give you a detailed, yet crisp notes along with a lesson plan. Once you are done going through the notes, you can test your skills by answering 10 MCQ's
""",
    icon="ℹ️",
)

st.header("Lesson Info")
title = st.header.write(f"{content_title}")


with st.expander("Lesson Plan"):
    st.write(f"{summary}")

with st.expander("Notes"):
    st.write(f"{Notes}")

# lessonplan = st.text_area("Lesson Plan", default_lessonplan, height=200)
# notes = st.text_area("Notes", default_notes, height=600)

st.divider()

# update your file here
file1 = "Notes.docx"


# Function to create a Word document from a string
def create_word_document(text):
    doc = docx.Document()
    doc.add_paragraph(text)
    # Add more formatting as needed
    return doc


# Function to save the document to a BytesIO object
def save_document_to_bytesio(doc):
    bio = io.BytesIO()
    doc.save(bio)
    return bio


# Create a Word document from a string
# text = "This is a sample text for the Word document."
doc = create_word_document(Notes)

# Save the document to a BytesIO object
bio = save_document_to_bytesio(doc)


st.subheader("Download your notes here")
st.download_button(
    label="Download Notes",
    # data=text.encode('utf-8'),
    # file_name=file1,
    data=bio.getvalue(),
    file_name=file1,
    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    # mime="text/plain",
    # file_name="example.md",
    # mime="text/markdown",
)

st.divider()

st.header("Assessment")
with st.expander("Lets take the test when ready!!"):
    # st.write(f"{default_lessonplan}")

    # Create a form for the quiz
    with st.form(key="quiz_form"):
        for question in questions:
            st.subheader(f"Question {question['no']}: {question['question']}")
            options = [question["a"], question["b"], question["c"], question["d"]]
            user_answer = st.radio(
                "Select an answer", options, key=f"question_{question['no']}"
            )
            # st.write(user_answer)
            answer.append(user_answer)  # Append user's answer to the answer list
        st.write(answer)  # Display all user answers
        submit2 = st.form_submit_button("Submit")
        # Submit button to calculate the score

    if submit2:
        i = 0
        # "entering submit function"
        # st.write(answer)
        # st.write(questions)
        for question in questions:
            # st.write("Entering for loop")
            # user_answer = st.radio(key=f"question_{question['no']}")
            if question["answer"] == answer[i]:
                # st.write("correct")
                score += 1
            else:
                pass
                # return score
            i = i + 1
        # Display the final score outside the form
        st.header(f"Your score: {score}/{len(questions)}")
