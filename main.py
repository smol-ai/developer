import sys
import os
import ast
from time import sleep
from utils import clean_dir, reportTokens, write_file
from constants import DEFAULT_DIR, DEFAULT_MODEL, DEFAULT_MAX_TOKENS
from systemPrompts.developer import planPrompt1, planPrompt2, filePrompt


def generate_response(model, system_prompt, user_prompt, *args):
    import openai

    # Set up your OpenAI API credentials
    openai.api_key = os.environ["OPENAI_API_KEY"]

    messages = []
    messages.append({"role": "system", "content": system_prompt})
    reportTokens(system_prompt)
    messages.append({"role": "user", "content": user_prompt})
    reportTokens(user_prompt)
    # loop thru each arg and add it to messages alternating role between "assistant" and "user"
    role = "assistant"
    for value in args:
        messages.append({"role": role, "content": value})
        reportTokens(value)
        role = "user" if role == "assistant" else "assistant"

    params = {
        "model": model,
        "messages": messages,
        "max_tokens": DEFAULT_MAX_TOKENS,
        "temperature": 0,
    }

    # Send the API request
    keep_trying = True
    numTries = 0
    while keep_trying and numTries < 5:
        try:
            numTries += 1
            response = openai.ChatCompletion.create(**params)
            keep_trying = False
        except Exception as e:
            # e.g. when the API is too busy, we don't want to fail everything
            print("Failed to generate response. Error: ", e)
            sleep(numTries)  # linear backoff
            print("Retrying...")

    # Get the reply from the API response
    reply = response.choices[0]["message"]["content"]
    return reply


def generate_file(
    filename,
    model=DEFAULT_MODEL,
    filepaths_string=None,
    shared_dependencies=None,
    prompt=None,
):
    systemPrompt, userPrompt = filePrompt(prompt, filepaths_string, shared_dependencies, filename)

    # call openai api with this prompt
    filecode = generate_response(model, systemPrompt, userPrompt)

    return filename, filecode


def main(prompt, directory=DEFAULT_DIR, model=DEFAULT_MODEL, file=None):
    # read prompt from file if it ends in a .md filetype
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
    filepaths_string = generate_response(
        model,
        planPrompt1(),
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
            filename, filecode = generate_file(
                file,
                model=model,
                filepaths_string=filepaths_string,
                shared_dependencies=shared_dependencies,
                prompt=prompt,
            )
            write_file(filename, filecode, directory)
        else:
            clean_dir(directory)

            # understand shared dependencies
            shared_dependencies = generate_response(
                model, planPrompt2(prompt, filepaths_string), prompt
            )
            print(shared_dependencies)
            # write shared dependencies as a md file inside the generated directory
            write_file("shared_dependencies.md", shared_dependencies, directory)

            for name in list_actual:
                filename, filecode = generate_file(
                    name,
                    model=model,
                    filepaths_string=filepaths_string,
                    shared_dependencies=shared_dependencies,
                    prompt=prompt,
                )
                write_file(filename, filecode, directory)

    except ValueError:
        print("Failed to parse result: " + result)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default=DEFAULT_DIR, help='Directory to write generated files to.')
    parser.add_argument('-f', '--file', help='If you only want to regenerate a single file, specify it here.')
    parser.add_argument('-m', '--model', default=DEFAULT_MODEL, help='Specify your desired model here (we recommend using `gpt-4`)')
    parser.add_argument('-p', '--prompt', help='Write your full prompt as a string, or give a path to a .md file with your prompt')
    args = parser.parse_args()

    
    # Check for arguments
    if len(sys.argv) < 2:
        # Looks like we don't have a prompt. Check if prompt.md exists
        if not os.path.exists("prompt.md"):
            # Still no? Then we can't continue
            print("Please provide a prompt")
            sys.exit(1)

        # Still here? Assign the prompt file name to prompt
        args.prompt = "prompt.md"

    else:
        # Set prompt to the first argument
        prompt = sys.argv[1]

    # Run the main function
    main(args.prompt, directory = args.directory, model = args.model, file=args.file)
