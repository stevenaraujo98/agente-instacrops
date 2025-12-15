from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from agents.agroBrain.state import State
from agents.agroBrain.nodes.extractor.node import extractor
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from agents.agroBrain.nodes.sensorWorker.tools import tools as sensor_tools
from agents.agroBrain.nodes.weatherWorker.tools import tools as weather_tools
from agents.agroBrain.nodes.sensorWorker.prompt import prompt_template as sensor_prompt_template
from agents.agroBrain.nodes.weatherWorker.prompt import prompt_template as weather_prompt_template

class State(TypedDict):
    code: str
    weather_review: str
    sensor_review: str
    final_review: str

llm = init_chat_model("openai:gpt-5-mini", temperature=0)

model = ChatOpenAI(model_name="gpt-4o-mini")

def sensor_worker(state: State):
    """Nodo que obtiene datos de sensores y los guarda en el state"""
    # Crear el agente
    agent = create_agent(
        model=model,
        tools=sensor_tools,
        system_prompt=sensor_prompt_template.format()
    )
    
    # Ejecutar el agente
    result = agent.invoke(state["messages"])

    # Actualizar el state
    return {
        "sensor_review": result.text
    }


def weather_worker(state: State):
    """Nodo que obtiene datos del clima y los guarda en el state"""
    # Crear el agente
    agent = create_agent(
        model=model,
        tools=weather_tools,
        system_prompt=weather_prompt_template.format()
    )
    
    # Ejecutar el agente
    result = agent.invoke(state["messages"])

    # Actualizar el state
    return {
        "weather_review": result.text
    }


def aggregator(state: State):
    weather_review = state['weather_review']
    sensor_review = state['sensor_review']
    messages = [
        ("system", "You are a Senior Agronomist and Precision Agriculture Consultant. Your role is to synthesize data from atmospheric forecasts (Weather) and ground telemetry (Sensors) to provide actionable farming insights. Focus on irrigation needs, pest risks, and crop stress levels."),
        ("user", f"Based on the collected data, provide a consolidated situation report and specific recommendations for the farm manager. DATA INPUTS: \
        1. Weather & Forecast Analysis: {weather_review}\
        2. Soil Sensor Telemetry: {sensor_review}\
        Please structure your response with:\
        - **Current Status**: Correlation between soil conditions and weather.\
        - **Risks**: Potential threats (e.g., drought stress, waterlogging, fungal conditions).\
        - **Actionable Recommendations**: Specific advice (e.g., 'Increase irrigation', 'Hold irrigation due to incoming rain').")
    ]
    response = llm.invoke(messages)
    return {
        'final_review': response.text
    }

"""
Definition of the agroBrain agent using LangGraph
"""
builder = StateGraph(State)
builder.add_node("extractor", extractor)
builder.add_node("weather_worker", weather_worker)
builder.add_node("sensor_worker", sensor_worker)
builder.add_node('aggregator', aggregator)


builder.add_edge(START, "extractor")
builder.add_edge("extractor", "weather_worker")
builder.add_edge("extractor", "sensor_worker")

builder.add_edge("weather_worker", "aggregator")
builder.add_edge("sensor_worker", "aggregator")

builder.add_edge("aggregator", END)

agent = builder.compile()