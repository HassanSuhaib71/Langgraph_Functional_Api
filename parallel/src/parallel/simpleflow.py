from langgraph.func import entrypoint, task


@task
def mul_by_two(num:int) -> int:

    return num*2

@task
def mul_by_three(num:int)-> int:

    return num*3


@entrypoint()
def parrallel_workflow(num:int):

    futures = [mul_by_two(num), mul_by_three(num)]

    results = [future.result() for future in futures]

    return {"OutPut" : results}

def call_parallel():
    result = parrallel_workflow.invoke(10)
    
    print("Output", result)