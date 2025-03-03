from langgraph.func import entrypoint, task


@task
def task1():
    print("Task_1")
    return "Task 1 Executed"

@task
def task2():
    print("Task_2")
    return "Task 2 Executed"

@entrypoint()
def run_flow(input:str):
    print("Running simple flow", input)

    task1_output = task1().result()
    task2_output = task2().result()

    return f"Workflow executed successfully with outputs : {task1_output} and {task2_output}"

def run_chain():
    # run_flow.invoke(input="Simple input")
    for event in run_flow.stream(input="Simple Input"):
        print(event)