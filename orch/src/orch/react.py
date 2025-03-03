from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from datetime import datetime

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


@tool
def get_current_time():
    """return the current time """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


agent = create_react_agent(
    model=llm,
    tool=[get_current_time],
    prompt ="""
    You are the helpful assisstant that can help with tasks and questions.
    You can use the following tools to help with tasks and questions: 
    - get_current_time
    """
)

def main():
    response = agent.invoke({"messages" : "What is current time?"})
    for message in response['messages']:
        message.pretty_print()