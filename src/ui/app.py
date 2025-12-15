from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.agents.agroBrain.agent import agent 

st.title("Agente AgroBrain 🌿")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg.type):
        st.write(msg.content)

# User input
if prompt := st.chat_input("Consulta sobre cultivos..."):
    # Save and display user message with corresponding role
    st.session_state.messages.append({"type": "human", "content": prompt})
    with st.chat_message("human"): # Sets the message as the user's
        st.write(prompt) # Displays the message in the interface

    # Invoke the agent (LangGraph)
    with st.chat_message("ai"):
        # Use stream to see the response in real-time
        response_placeholder = st.empty()
        full_response = ""
        
        # 'stream' returns events step by step
        inputs = {"messages": st.session_state.messages}
        for chunk in agent.stream(inputs, stream_mode="values"):
            # Filter to get only the last AI message
            if "messages" in chunk:
                last_msg = chunk["messages"][-1]
                if last_msg.type == "ai":
                    full_response = last_msg.content
                    response_placeholder.write(full_response)
        
        # Save response in history with corresponding role
        st.session_state.messages.append({"type": "ai", "content": full_response})