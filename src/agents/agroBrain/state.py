from langgraph.graph import MessagesState

class State(MessagesState):
    customer_name: str
    target_city: str
    target_date: str
    target_hour: str