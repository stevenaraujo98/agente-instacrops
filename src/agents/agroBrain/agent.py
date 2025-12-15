from langgraph.graph import StateGraph, START, END

from agents.agroBrain.state import State
from agents.agroBrain.nodes.extractor.node import extractor
from agents.agroBrain.nodes.weatherWorker.node import weather_worker
from agents.agroBrain.nodes.sensorWorker.node import sensor_worker
# from agents.agroBrain.routes.intent.route import intent_route



builder = StateGraph(State)
builder.add_node("extractor", extractor)
builder.add_node("weather_worker", weather_worker)
builder.add_node("sensor_worker", sensor_worker)

builder.add_edge(START, "extractor")
# builder.add_conditional_edges('extractor', intent_route)
builder.add_edge("extractor", "weather_worker")
builder.add_edge("extractor", "sensor_worker")
builder.add_edge("weather_worker", END)
builder.add_edge("sensor_worker", END)

agent = builder.compile()