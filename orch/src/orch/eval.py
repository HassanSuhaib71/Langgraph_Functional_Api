from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

#Evaluator-optimizer Workflow 
#Poem Flow == Funny Poem Flow
#Input == poem topic
#Genrator: Genrate a funny poem
#Evaluator: Eavluate the poem if it is funny then end else not

@task
def poem_generator(input_data:str) -> str:
    return llm.invoke(f"Generate a funny poem about {input_data}").content

@task
def poem_evaluator(inputdata: str) -> str:
    return llm.invoke(f"Evaluate the poem if it is funny or not {inputdata}.In output return only one word 'funny' or 'retry'")

@entrypoint()
def evaluator_optimizer_workflow(topic: str):
    while True:
        poem = poem_generator(topic).result()
        print("\n\n Generated Poem",poem)
        evaluator = poem_evaluator(poem).result()
        print("\n\n Evaluator", evaluator)
        if evaluator == "funny":
            break
        else:
            continue
    return poem

def main():
    poem = evaluator_optimizer_workflow.invoke("Verical AI agents.")
    print("\n\n Poem", poem)