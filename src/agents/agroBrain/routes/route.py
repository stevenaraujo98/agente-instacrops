from pydantic import BaseModel, Field
from typing import Literal
from langchain.chat_models import init_chat_model
from agents.agroBrain.state import State
from agents.agroBrain.routes.prompt import SYSTEM_PROMPT


# Define the structured output schema for routing intent
class RouteIntent(BaseModel):
    step: Literal["sensor_worker", "weather_worker"] = Field(
        'sensor_worker', description="The next step in the routing process"
    ) # by default returns conversation with the Field

llm = init_chat_model("openai:gpt-5-nano", temperature=0)
llm = llm.with_structured_output(schema=RouteIntent)

# Define the intent routing function
def intent_route(state: State) -> Literal["sensor_worker", "weather_worker"]:
    history = state["messages"]
    print('*'*100)
    print(history)
    print('*'*100)
    schema = llm.invoke([("system", SYSTEM_PROMPT)] + history)
    print('Ruteo a:', schema.step) 
    if schema.step is not None: 
        return schema.step
    return 'sensor_worker'
