from langgraph.graph import MessagesState

""""
Customized status for the agroBrain agent
"""
class State(MessagesState):
    customer_name: str
    target_city: str
    target_date: str
    target_hour: str
    type_sensor: str
