from langchain.agents import create_agent

from agents.agroBrain.nodes.weatherWorker.tools import tools
from agents.agroBrain.nodes.weatherWorker.prompt import prompt_template
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from agents.agroBrain.state import State

model = ChatOpenAI(
    model_name="gpt-4.1-nano",
    # model_name="gpt-4o-mini",
    # temperature=None,
    # max_tokens=None,
)

weather_worker = create_agent(
    model=model,
    tools=tools,
    system_prompt=prompt_template.format(),
)
