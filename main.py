import os
import modal
import ast

stub = modal.Stub("smol-developer-v1")
generatedDir = "generated"
openai_image = modal.Image.debian_slim().pip_install("openai", "tiktoken")
openai_model = "gpt-4" # or 'gpt-3.5-turbo',
openai_model_max_tokens = 2000 # i wonder how to tweak this properly


@stub.function(
    image=openai_image,
    secret=modal.Secret.from_dotenv(),
    retries=modal.Retries(
        max_retries=3,
        backoff_coefficient=2.0,
        initial_delay=1.0,
    ),
    # concurrency_limit=5,
    # timeout=120,
)
def generate_response(system_prompt, user_prompt, *args):
    # IMPORTANT: Keep the import statements here due to Modal container restrictions.
    # Shifting the imports to the start of the code may cause issues with package availability.
    import openai
    import tiktoken

    def reportTokens(prompt):
        encoding = tiktoken.encoding_for_model(openai_model)
        # print number of tokens in light gray, with first 10 characters of prompt in green
        print("\033[37m" + str(len(encoding.encode(prompt))) + " tokens\033[0m" + " in prompt: " + "\033[92m" + prompt[:50] + "\033[0m")
        

    # Set up your OpenAI API credentials
    openai.api_key = os.environ["OPENAI_API_KEY"]

    messages = []
    messages.append({"role": "system", "content": system_prompt})
    reportTokens(system_prompt)
    messages.append({"role": "user", "content": user_prompt})
    reportTokens(user_prompt)
    # Loop through each value in args and add it to messages alternating role between "assistant" and "user"
    role = "assistant"
    for value in args:
        messages.append({"role": role, "content": value})
        reportTokens(value)
        role = "user" if role == "assistant" else "assistant"

    params = {
        "model": openai_model,
        "messages": messages,
        "max_tokens": openai_model_max_tokens,
        "temperature": 0,
    }

    # Send the API request
    response = openai.ChatCompletion.create(**params)

    # Get the reply from the API response
    reply = response.choices[0]["message"]["content"]
    return reply


@stub.function()
def generate_file(filename, filepaths_string=None, shared_dependencies=None, prompt=None):
    # call openai api with this prompt
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
       - MOST IMPORTANT OF ALL - the purpose of our app is {prompt} - every line of code you generate must be valid code. Do not include code fences in your response, for example
    
    Bad response:
    ```javascript 
    console.log("hello world")
    ```
    
    Good response:
    console.log("hello world")
    
    Begin generating the code now.

    """,
    )

    return filename, filecode


@stub.local_entrypoint()
def main(prompt, directory=generatedDir, file=None):
    # read file from prompt if it ends in a .md filetype
    if prompt.endswith(".md"):
        with open(prompt, "r") as promptfile:
            prompt = promptfile.read()

    print("hi its me, 🐣the smol developer🐣! you said you wanted:")
    # print the prompt in green color
    print("\033[92m" + prompt + "\033[0m")

    # example prompt:
    # a Chrome extension that, when clicked, opens a small window with a page where you can enter
    # a prompt for reading the currently open page and generating some response from openai

    # call openai api with this prompt
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
            write_file(filename, filecode, directory)
        else:
            clean_dir(directory)

            # understand shared dependencies
            shared_dependencies = generate_response.call(
                """You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
                
            In response to the user's prompt:

            ---
            the app is: {prompt}
            ---
            
            the files we have decided to generate are: {filepaths_string}

            Now that we have a list of files, we need to understand what dependencies they share.
            Please name and briefly describe what is shared between the files we are generating, including exported variables, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.
            Exclusively focus on the names of the shared dependencies, and do not add any other explanation.
            """,
                prompt,
            )
            print(shared_dependencies)
            # write shared dependencies as a md file inside the generated directory
            write_file("shared_dependencies.md", shared_dependencies, directory)
            
            # Generate code files for each file path in `list_actual`.
            for filename, filecode in generate_file.map(
                list_actual, order_outputs=False, kwargs=dict(filepaths_string=filepaths_string, shared_dependencies=shared_dependencies, prompt=prompt)
            ):
                write_file(filename, filecode, directory)


    except ValueError:
        print("Failed to parse result.")


def write_file(filename, filecode, directory):
    # Output the filename in blue color
    print("\033[94m" + filename + "\033[0m")
    print(filecode)
    
    file_path = directory + "/" + filename
    dir = os.path.dirname(file_path)
    os.makedirs(dir, exist_ok=True)

    # Open the file in write mode
    with open(file_path, "w") as file:
        # Write content to the file
        file.write(filecode)


def clean_dir(directory):
    extensions_to_skip = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.ico', '.tif', '.tiff', '.eps', '.raw']  # Add more extensions if needed

    # Check if the directory exists
    if os.path.exists(directory):
        # If it does, iterate over all files and directories
        for root, files in os.walk(directory):
            for file in files:
                _, extension = os.path.splitext(file)
                if extension not in extensions_to_skip:
                    os.remove(os.path.join(root, file))
    else:
        os.makedirs(directory, exist_ok=True)