import sys
import os
import modal
import ast

stub = modal.Stub("smol-developer-v1")

openai_image = modal.Image.debian_slim().pip_install("openai")


@stub.function(
    image=openai_image,
    secret=modal.Secret.from_dotenv(),
    retries=modal.Retries(
        max_retries=3,
        backoff_coefficient=2.0,
        initial_delay=1.0,
    ),
    timeout=120
)
def generate_response(system_prompt, user_prompt, *args):
    import openai
    # Set up your OpenAI API credentials
    openai.api_key = os.environ["OPENAI_API_KEY"]

    messages = []
    messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': user_prompt})
    # loop thru each arg and add it to messages alternating role between "assistant" and "user"
    role = 'assistant'
    for value in args:
        messages.append({'role': role, 'content': value})
        role = 'user' if role == 'assistant' else 'assistant'


    params = {
        # 'model': 'gpt-3.5-turbo',
        'model': 'gpt-4',
        'messages': messages,
        'max_tokens': 300,
        'temperature': 0
    }

    # Send the API request
    response = openai.ChatCompletion.create(**params)

    # Get the reply from the API response
    reply = response.choices[0]['message']['content']
    return reply

@stub.function()
def generate_file(filename, filepaths_string, prompt):
    # call openai api with this prompt
    filecode = generate_response.call(f"""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
    the app is: {prompt}

    the files we have decided to generate are: {filepaths_string}
    
    only write valid code for the given filepath and file type, and return only the code.
    do not add any other explanation, only return valid code for that file type.
    """, f"""
    We have broken up the program into per-file generation. 
    Now your job is to generate only the code for the file {filename}. 
    Make sure to have consistent filenames if you reference other files we are also generating.
    Remember that you must obey 3 things: 
       - you are generating code for the file {filename}
       - the other files we have listed are {filepaths_string}
       - MOST IMPORTANT OF ALL - the purpose of our app is {prompt} - every line of code you generate must be in service of this purpose.
    Begin generating the code now.
    """
    )
    # # print first filecode in gray
    # print("\033[90m" + filecode + "\033[0m")
    
    # reprompt as needed
    filecode = generate_response.call(f"""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
    the app is: {prompt}

    the files we have decided to generate are: {filepaths_string}
    
    only write valid code for the given filepath and file type, and return only the code.
    do not add any other explanation, only return valid code for that file type.
    """, f"""
    We have broken up the program into per-file generation. 
    Now your job is to generate only the code for the file {filename}. 
    Make sure to have consistent filenames if you reference other files we are also generating.
    Do not generate any code that references files we have not explicitly listed since they will not exist.
    """, filecode,
    f"""
    Your original code may have issues. Remember that you must obey 3 things: 
       - you are generating code for the file {filename}
       - the other files we have listed are {filepaths_string}
       - MOST IMPORTANT OF ALL - the purpose of our app is {prompt} - every line of code you generate must be in service of this purpose.
    Make sure to have consistent filenames if you reference other files we are also generating. 
    If you reference a file that we are not generating, the code will not work, so make sure the name matches the files we have listed.
    Remember what environment the code has to operate in, and you must generate code that will work in that environment.
    """
    )

    return filename, filecode


@stub.local_entrypoint()
def main(prompt):
    print("hi its me, the smol developer! you have asked me to")
    # print the prompt in green color
    print("\033[92m" + prompt + "\033[0m")


    # example prompt:
    # a Chrome extension that, when clicked, opens a small window with a page where you can enter
    # a prompt for reading the currently open page and generating some response from openai
    
    # call openai api with this prompt
    filepaths_string = generate_response.call("""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
        
    When given their intent, create a complete, exhaustive list of filepaths that the user would write to make the program.
    
    only list the filepaths you would write, and return them as a python list of strings. 
    do not add any other explanation, only return a python list of strings.
    """, prompt
    )
    print(filepaths_string)
    # parse the result into a python list
    list_actual = []
    try:
        list_actual = ast.literal_eval(filepaths_string)
        # write the file
        generatedDir = "generated"

        import shutil
        # Check if the directory exists
        if os.path.exists(generatedDir):
            # If it does, delete it and all its contents
            shutil.rmtree(generatedDir)
        os.makedirs(generatedDir, exist_ok=True)
        for filename, filecode in generate_file.map(list_actual, filepaths_string, prompt):
            # print the filename in blue color
            print("\033[94m" + filename + "\033[0m")
            print(filecode)

            with open(generatedDir + '/' + filename, 'w') as file:
                # Write a line to the file
                file.write(filecode)

    except ValueError:
        print('Failed to parse result: ' + result)


    # # Call the function locally.
    # print(f(1000))

    # # Call the function remotely.
    # print(f.call(1000))

    # # Parallel map.
    # total = 0
    # for ret in f.map(range(20)):
    #     total += ret

    # print(total)
