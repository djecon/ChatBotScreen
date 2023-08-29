import streamlit as st
import requests
import datetime
import pytz

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

def is_valid_time():
    pacific = pytz.timezone('US/Pacific')
    current_time = datetime.datetime.now(pacific).time()
    print(current_time)
    return current_time < datetime.time(8, 0) or current_time >= datetime.time(17, 0)

API_URL = "http://44.206.234.21:3000/api/v1/prediction/6ce36d53-ed90-4759-877b-83aedadb617b"
# API_URL = "http://localhost:3000/api/v1/prediction/575f6659-23eb-4ccb-885c-d2d3632fb976"

logo_image = 'an-2050-light-horizontal-logo.png'
st.image(logo_image)
st.title("Chatbot")
st.text("Based on 29 PDF guides. This app is only available between 8am to 5pm Pacific")

if not is_valid_time():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is your question about Natural & Adabas?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = query({
            "question": prompt,
        })

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.error("Sorry, this feature is only available between 8am and 5pm Pacific")

