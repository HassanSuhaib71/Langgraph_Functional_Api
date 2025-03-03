import random
from langgraph.func import entrypoint, task
from typing import TypedDict, Literal


class RouterInput(TypedDict):
    """Input for the router function."""
    query: str

class RouterOutput(TypedDict):
    query: str
    cateogery: Literal["math", "writing", "general"]
    response: str

@task
def router_query(input:RouterInput) -> Literal["math", "writing", "general"]:
    """Randomly route query to a specific handler"""
    cateogery : Literal["math", "writing", "general"] = ["math", "writing", "general"]
    return random.choice(cateogery)

@task
def math_query(query:str) -> str:
    """Handle math queries"""
    return f"Math handle processing {query}"

@task
def writing_query(query:str) -> str:
    """Handle writing queries"""
    return f"Writing handle processing {query}"

@task
def general_query(query:str) -> str:
    """Handle general queries"""
    return f"General handle processing {query}"

@entrypoint()
def router_flow(input_data:RouterInput) -> RouterOutput:
    """Main worflow appropriate query to the right handler"""

    cateogery = router_query(input_data).result()

    if cateogery == "math":
        response = math_query(input_data["query"]).result()
    elif cateogery == "writing":
        response = writing_query(input_data["query"]).result()
    else:
        response = general_query(input_data["query"]).result()

    return RouterOutput(
        query=input_data["query"],
        cateogery=cateogery,
        response=response)

def router_call():

    input_data = {"query": "Select a random literal"}

    result = router_flow.invoke(input_data)
    print(result)
