from smol_dev.prompts import plan, specify_file_paths, generate_code

from agent_protocol import (
    Agent,
    StepResult,
    StepHandler,
)


async def smol_developer(prompt: str):
    shared_deps = plan(prompt)
    yield shared_deps

    file_paths = specify_file_paths(prompt, shared_deps)
    yield file_paths

    for file_path in file_paths:
        code = await generate_code(prompt, shared_deps, file_path)
        yield code


async def task_handler(task_input) -> StepHandler:
    if not task_input:
        raise Exception("No task prompt")

    smol_developer_loop = smol_developer(prompt=task_input)

    async def step_handler(step_input):
        result = await anext(smol_developer_loop, None)
        if result is None:
            return StepResult(is_last=True)
        return StepResult(output=result)

    return step_handler


Agent.handle_task(task_handler).start()
