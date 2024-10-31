import streamlit as st
import backend as chatbot

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;  
    }
    .header {
        font-size: 2.5em;  
        font-weight: bold;
        color: #2C3E50; 
        text-align: center;
        margin-bottom: 20px;
        padding: 10px;
        border-radius: 10px;
        background-color: #ECF0F1; 
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);  
    }
    .subheader {
        font-size: 1.2em;
        color: #34495E;  
        text-align: center;
        margin-bottom: 30px;
    }
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px 0;
        max-width: 70%;
        display: inline-block;
        text-align: center; 
    }
    .user-bubble {
        background-color: #3498DB;  
        color: white;
        align-self: flex-end;  
        margin-left: auto; 
    }
    .assistant-bubble {
        background-color: #E74C3C;  
        color: white;
        align-self: flex-start;  
        margin-right: auto;  
    }
    .chat-message {
        display: flex;
        justify-content: center;  
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Subheader
st.markdown("<div class='header'>Character-based Chatbot</div>", unsafe_allow_html=True)

# Initialize the memory buffers and chat history if not already done
if 'memory_buffers' not in st.session_state:
    st.session_state.memory_buffers = {}

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}

# Function to handle chat history
def add_to_chat_history(session_id, role, text):
    if session_id not in st.session_state.chat_history:
        st.session_state.chat_history[session_id] = []
    st.session_state.chat_history[session_id].append({"role": role, "text": text})

# Sidebar for session management
st.sidebar.title("Chat Sessions")
session_names = list(st.session_state.chat_history.keys())
current_session = st.sidebar.selectbox("Select Session", options=session_names + ["New Session"])
if current_session == "New Session":
    new_session_name = st.sidebar.text_input("Enter new session name")
    if st.sidebar.button("Create Session"):
        current_session = new_session_name
        st.session_state.chat_history[current_session] = []

# Delete session functionality
if current_session in session_names:
    if st.sidebar.button("Delete Session"):
        del st.session_state.chat_history[current_session]
        current_session = session_names[0] if session_names else "New Session"

# Display chat history for the current session
if current_session in st.session_state.chat_history:
    for message in st.session_state.chat_history[current_session]:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f"<div class='chat-bubble user-bubble'>{message['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble assistant-bubble'>{message['text']}</div>", unsafe_allow_html=True)

# Dropdown for selecting character profile
character_profile = st.selectbox("Select Character Profile", ["mom", "dad", "sibling", "significant other", "friend", "teacher", "coach", "neutral"])

# User input options
st.markdown("### Enter your message")
input_text = st.chat_input("Type your message here...")

if input_text:
    # Display user message
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-bubble user-bubble'>{input_text}</div>", unsafe_allow_html=True)
    add_to_chat_history(current_session, "user", input_text)

    # Initialize the memory buffer for the current session
    if current_session not in st.session_state.memory_buffers:
        st.session_state.memory_buffers[current_session] = chatbot.chatbot_memory()
    memory = st.session_state.memory_buffers[current_session]

    # Get chatbot response with fixed values for temperature and top_p
    chat_response = chatbot.chatbot_chain(
        input_text=input_text, 
        character_profile=character_profile,  # Pass the character profile here
        memory=memory,
        temperature=0.5,  # Fixed value for temperature
        top_p=1,          # Fixed value for top_p
    )
    
    # Display chatbot response
    with st.chat_message("assistant"):
        st.markdown(f"<div class='chat-bubble assistant-bubble'>{chat_response}</div>", unsafe_allow_html=True)
    add_to_chat_history(current_session, "assistant", chat_response)
