import os

generatedDir = "generated"


def read_file(filename):
    with open(filename, "r") as file:
        return file.read()


def walk_directory(directory):
    image_extensions = [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".svg",
        ".ico",
        ".tif",
        ".tiff",
    ]
    code_contents = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not any(file.endswith(ext) for ext in image_extensions):
                try:
                    relative_filepath = os.path.relpath(
                        os.path.join(root, file), directory
                    )
                    code_contents[relative_filepath] = read_file(
                        os.path.join(root, file)
                    )
                except Exception as e:
                    code_contents[
                        relative_filepath
                    ] = f"Error reading file {file}: {str(e)}"
    return code_contents


def main(prompt, directory=generatedDir, model="gpt-3.5-turbo"):
    code_contents = walk_directory(directory)

    # Now, `code_contents` is a dictionary that contains the content of all your non-image files
    # You can send this to OpenAI's text-davinci-003 for help

    context = "\n".join(
        f"{path}:\n{contents}" for path, contents in code_contents.items()
    )
    system = "You are an AI debugger who is trying to debug a program for a user based on their file system. The user has provided you with the following files and their contents, finally folllowed by the error message or issue they are facing."
    prompt = (
        "My files are as follows: "
        + context
        + "\n\n"
        + "My issue is as follows: "
        + prompt
    )
    prompt += (
        "\n\nGive me ideas for what could be wrong and what fixes to do in which files."
    )
    res = generate_response(system, prompt, model)
    # print res in teal
    print("\033[96m" + res + "\033[0m")


def generate_response(system_prompt, user_prompt, model="gpt-3.5-turbo", *args):
    import openai

    # Set up your OpenAI API credentials
    openai.api_key = os.environ["OPENAI_API_KEY"]

    messages = []
    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    # loop thru each arg and add it to messages alternating role between "assistant" and "user"
    role = "assistant"
    for value in args:
        messages.append({"role": role, "content": value})
        role = "user" if role == "assistant" else "assistant"

    params = {
        "model": model,
        # "model": "gpt-4",
        "messages": messages,
        "max_tokens": 1500,
        "temperature": 0,
    }

    # Send the API request
    response = openai.ChatCompletion.create(**params)

    # Get the reply from the API response
    reply = response.choices[0]["message"]["content"]
    return reply


if __name__ == "__main__":
    import sys

    prompt = sys.argv[1]
    main(prompt)
