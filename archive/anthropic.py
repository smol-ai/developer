import sys
import os
import modal
import ast
from utils import clean_dir

stub = modal.Stub("smol-developer-v1-anthropic")
generatedDir = "generated"
new_image = modal.Image.debian_slim().pip_install("requests")


@stub.function(
    image=new_image,
    secret=modal.Secret.from_dotenv(),
    retries=modal.Retries(
        max_retries=3,
        backoff_coefficient=2.0,
        initial_delay=1.0,
    ),
    concurrency_limit=5,
    timeout=120,
)
def generate_response(system_prompt, user_prompt, *args):
    import requests
    import json
    # Set up your API credentials
    ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

    messages = []
    messages.append("Human: " + user_prompt)
    messages.append("Human: " + system_prompt)
    
    for value in args:
      messages.append("Human: " + value)

    messages.append("Assistant: ")
    print("messages", messages)
    params = {
        # 'model': 'gpt-3.5-turbo',
        "model": "claude-instant-v1",
        # flatten messages into a single string
        "prompt": "\n\n".join(messages),
        "max_tokens_to_sample": 1500,
        "stop_sequences": ["\n\nHuman:"],
        "temperature": 0,
    }

# # Synchronous request: only replies with the full response
# export API_KEY=my_api_key
# curl https://api.anthropic.com/v1/complete\
#   -H "x-api-key: $API_KEY"\
#   -H 'content-type: application/json'\
#   -d '{
#     "prompt": "\n\nHuman: Tell me a haiku about trees\n\nAssistant: ",
#     "model": "claude-v1", "max_tokens_to_sample": 300, "stop_sequences": ["\n\nHuman:"]
#   }'
# {"completion":" Here is a haiku about trees:\n\nSilent sentinels, \nStanding solemn in the woods,\nBranches reaching sky.","stop":"\n\nHuman:","stop_reason":"stop_sequence","truncated":false,"log_id":"f5d95cf326a4ac39ee36a35f434a59d5","model":"claude-v1","exception":null}

    # Send the API request to anthropic and get the reply
    response = requests.post(
        "https://api.anthropic.com/v1/complete",
        headers={"x-api-key": ANTHROPIC_API_KEY, "content-type": "application/json"},
        data=json.dumps(params),
    )
    response = response.json()
    reply = response["completion"]
    # trim leading/trailing spaces of reply
    return reply.strip()


@stub.function()
def generate_file(filename, filepaths_string=None, shared_dependencies=None, prompt=None):
    # call api with this prompt
    filecode = generate_response.call(
        f"""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
    the app is: {prompt}

    the files we have decided to generate are: {filepaths_string}

    the shared dependencies (like filenames and variable names) we have decided on are: {shared_dependencies}
    
    only write valid code for the given filepath and file type, and return only the code.
    do not add any other explanation, only return valid code for that file type.
    """,
        f"""
    We have broken up the program into per-file generation. 
    Now your job is to generate only the code for the file {filename}. 
    Make sure to have consistent filenames if you reference other files we are also generating.
    Remember that you must obey 3 things: 
       - you are generating code for the file {filename}
       - do not stray from the names of the files and the shared dependencies we have decided on
       - MOST IMPORTANT OF ALL - the purpose of our app is {prompt} - every line of code you generate must be valid code.
    Begin generating the code now.
    """,
    )

    return filename, filecode


@stub.local_entrypoint()
def main(prompt, outputdir=generatedDir, file=None):
    # read file from prompt if it ends in a .md filetype
    if prompt.endswith(".md"):
        with open(prompt, "r") as promptfile:
            prompt = promptfile.read()

    print("hi its me, the smol developer! you have asked me to")
    # print the prompt in green color
    print("\033[92m" + prompt + "\033[0m")

    # example prompt:
    # a Chrome extension that, when clicked, opens a small window with a page where you can enter
    # a prompt for reading the currently open page and generating some response

    # call api with this prompt
    filepaths_string = generate_response.call(
        """You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
    When given their intent, create a complete, exhaustive list of filepaths that the user would write to make the program.
    
    only list the filepaths you would write, and return them as a python list of strings. 
    do not add any other explanation, only return a python list of strings.
    """,
        prompt,
    )
    print(filepaths_string)
    # parse the result into a python list
    list_actual = []
    try:
        list_actual = ast.literal_eval(filepaths_string)

        # if shared_dependencies.md is there, read it in, else set it to None
        shared_dependencies = None
        if os.path.exists("shared_dependencies.md"):
            with open("shared_dependencies.md", "r") as shared_dependencies_file:
                shared_dependencies = shared_dependencies_file.read()

        if file is not None:
            # check file
            print("file", file)
            filename, filecode = generate_file(file, filepaths_string=filepaths_string, shared_dependencies=shared_dependencies, prompt=prompt)
            write_file(filename, filecode)
        else:
            clean_dir()

            # understand shared dependencies
            shared_dependencies = generate_response.call(
                """You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
                
            In response to the user's prompt:

            ---
            the app is: {prompt}
            ---
            
            the files we have decided to generate are: {filepaths_string}

            Now that we have a list of files, we need to understand what dependencies they share.
            Please name and briefly describe what is shared between the files we are generating, including filenames, variables, data schemas, DOM elements and id's, message names, and function names.
            """,
                prompt,
            )
            print(shared_dependencies)
            # write shared dependencies as a md file inside the generated directory
            write_file("shared_dependencies.md", shared_dependencies)
            
            # Existing for loop
            for filename, filecode in generate_file.map(
                list_actual, kwargs=dict(filepaths_string=filepaths_string, shared_dependencies=shared_dependencies, prompt=prompt)
            ):
                write_file(filename, filecode)


    except ValueError:
        print("Failed to parse result: " + result)


def write_file(filename, filecode):
    # Output the filename in blue color
    print("\033[94m" + filename + "\033[0m")
    print(filecode)

    # Open the file in write mode
    with open(generatedDir + "/" + filename, "w") as file:
        # Write content to the file
        file.write(filecode)
