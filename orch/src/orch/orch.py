from typing import cast
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")

class InstructionsGenerator(BaseModel):
    worker_instructions: list[str] = Field(description ="List of instructions for each worker")

@task
def call_orchastrator(idea: str):
    instrctions = cast(InstructionsGenerator, llm.with_structured_output(InstructionsGenerator).invoke(
        f"Generate instructions for the workers to generate a Idea valdation report for the following {idea}. Keep workers count under 3"
    ))
    return instrctions
@task
def call_worker(instructions:str):
    return llm.invoke(instructions).content

@task
def combine_result(results:list[str]) -> str:
    return "\n\n".join(results)

@entrypoint()
def orchastrator_worker(idea:str):
    #1. Call Orchastrator
    instructions = call_orchastrator(idea).result()
    #2. Create a list of feauters
    workers = [call_worker(instruction) for instruction in instructions.worker_instructions]
    #3. Resolve all futures in parallel
    results = [worker.result() for worker in workers]
    #4. Combine result
    final_report = combine_result(results).result()

    return final_report


def main():
    final_report = orchastrator_worker.invoke("Creating a Lead Generating Agent.")
    print("\n\n", final_report)