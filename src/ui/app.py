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

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg.type):
        st.write(msg.content)

# Input de usuario
if prompt := st.chat_input("Consulta sobre cultivos..."):
    # Guardar y mostrar user message
    st.session_state.messages.append({"type": "human", "content": prompt})
    with st.chat_message("human"):
        st.write(prompt)

    # Invocar a tu agente (LangGraph)
    with st.chat_message("ai"):
        # Usamos stream para ver la respuesta en tiempo real
        response_placeholder = st.empty()
        full_response = ""
        
        # 'stream' devuelve eventos paso a paso
        inputs = {"messages": st.session_state.messages}
        for chunk in agent.stream(inputs, stream_mode="values"):
            # Filtramos para obtener solo el último mensaje del AI
            if "messages" in chunk:
                last_msg = chunk["messages"][-1]
                if last_msg.type == "ai":
                    full_response = last_msg.content
                    response_placeholder.write(full_response)
        
        # Guardar respuesta en historial
        st.session_state.messages.append({"type": "ai", "content": full_response})