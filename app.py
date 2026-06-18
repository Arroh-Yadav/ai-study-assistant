import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Please set GEMINI_API_KEY environment variable")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("🤖 AI Study Assistant")

# Sidebar for features
option = st.sidebar.selectbox("Choose a feature", ["Chat", "Generate Quiz", "Study Plan", "Summarize Notes"])

if option == "Chat":
    st.header("Ask anything about your studies")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[{"role": "user", "parts": [{"text": prompt}]}]
            )
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

elif option == "Generate Quiz":
    st.header("Generate a Quiz")
    subject = st.text_input("Subject")
    topic = st.text_input("Specific Topic")
    num_questions = st.number_input("Number of questions", min_value=5, max_value=20, value=10)
    
    if st.button("Generate Quiz"):
        prompt = f"Create a {num_questions}-question multiple choice quiz on {topic} in {subject}. Include answers."
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        st.write(response.text)

elif option == "Study Plan":
    st.header("Create a Study Plan")
    subject = st.text_input("Subject")
    duration = st.text_input("Study duration (e.g., 1 week)")
    goals = st.text_area("Your goals")
    
    if st.button("Generate Plan"):
        prompt = f"Create a detailed study plan for {subject} over {duration}. Goals: {goals}"
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        st.write(response.text)

elif option == "Summarize Notes":
    st.header("Summarize Your Notes")
    notes = st.text_area("Paste your notes here")
    
    if st.button("Summarize"):
        prompt = f"Summarize these study notes concisely and highlight key points: {notes}"
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        st.write(response.text)