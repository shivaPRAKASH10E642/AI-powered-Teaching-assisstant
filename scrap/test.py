import streamlit as st
import pandas as pd
import docx
import io

import get_content_summary
import get_transcripts

# Sample data
questions = []
content_title, summary, Notes = "", "", ""

# Initialize score
score = 0
answer = ["", "", "", "", "", "", "", "", "", ""]
i = 0

st.set_page_config(page_title="Dhrona.ai", page_icon="🏹")
st.title("🏹 Dhrona.ai 🏹 ")

# Rest of your code...

st.divider()

st.header("Assessment")
with st.expander("Lets take the test when ready!!"):
    with st.form(key="quiz_form"):
        for question in questions:
            st.subheader(f"Question {question['no']}: {question['question']}")
            options = [question["a"], question["b"], question["c"], question["d"]]
            user_answer = st.radio(
                "Select an answer", options, key=f"question_{question['no']}"
            )
            answer[i] = user_answer
            i += 1

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        i = 0
        for question in questions:
            if question["answer"] == answer[i]:
                score += 1
            i = i + 1

    st.header(f"Your score: {score}/{len(questions)}")
