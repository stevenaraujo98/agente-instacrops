from langchain_core.prompts import PromptTemplate

template = """\
You are a helpful assistant who can extract contact information and the city of interest from a given conversation.
"""

prompt_template = PromptTemplate.from_template(template)