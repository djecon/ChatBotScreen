import streamlit as st
import requests
import datetime
import pytz
import sqlite3
# import pinecone

pc_api = st.secrets["PINECONE_API"]
# pinecone.init(api_key=pc_key, environment='gcp-starter')
# index = pinecone.Index('natural')
# index_stats_response = index.describe_index_stats()
# vector_count = index_stats_response['total_vector_count']

conn = sqlite3.connect('querytable.db')
c = conn.cursor()
iconimage = 'an-2050-dark-circle-logo-favicon.png'
st.set_page_config(page_title="A&N Chatbot", page_icon=iconimage, initial_sidebar_state="collapsed")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# padding = 0
#  st.markdown(f""" <style>
#    .reportview-container .main .block-container{{
#        padding-top: {padding}rem;
#        padding-right: {padding}rem;
#        padding-left: {padding}rem;
#        padding-bottom: {padding}rem;
#    }} </style> """, unsafe_allow_html=True)

def create_querytable():
    c.execute('CREATE TABLE IF NOT EXISTS querytable(query TEXT,response TEXT, timestamp TEXT)')

def get_querycount():
    c.execute()

def add_query(query, response):
    timestamp = datetime.datetime.utcnow().isoformat()
    c.execute('INSERT INTO querytable(query,response,timestamp) VALUES (?,?,?)', (query, response, timestamp))
    conn.commit()

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

def is_valid_time():
    pacific = pytz.timezone('US/Pacific')
    current_time = datetime.datetime.now(pacific).time()
    print(current_time)
    return current_time < datetime.time(5, 0) or current_time >= datetime.time(17, 0)
    
API_URL = "http://34.207.163.184:3000/api/v1/prediction/6ce36d53-ed90-4759-877b-83aedadb617b"
logo_image = 'an-2050-light-horizontal-logo.png'

create_querytable()

c.execute('SELECT COUNT(*) FROM querytable')
querycount = c.fetchone()[0]

with st.sidebar:
    st.sidebar.write("Question Count", querycount)
    st.sidebar.write("Vector Count:", 34671)

st.image(logo_image)
st.title("Chatbot")
st.text("Based on 68 PDF guides. This app is only available between 8am - 5pm Pacific")
st.text(
    "The following information is provided by an AI-powered system and should be used for informational purposes only. While the system strives to provide accurate and relevant responses, it may not always reflect human expertise or account for specific contexts. Users are advised to verify the information independently and consult with domain experts if needed.")

if not is_valid_time():
    # Initialize chat history
    create_querytable()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about Natural & Adabas"):
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
        # Store audit trail
        add_query(prompt, response)
        querycount += 1

else:
    st.error("Sorry, this feature is only available between 8am and 5pm Pacific")

