import os
from constants import EXTENSION_TO_SKIP, DEFAULT_MODEL

def clean_dir(directory):
    # Check if the directory exists
    if os.path.exists(directory):
        # If it does, iterate over all files and directories
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                _, extension = os.path.splitext(filename)
                if extension not in EXTENSION_TO_SKIP:
                    os.remove(os.path.join(dirpath, filename))
    else:
        os.makedirs(directory, exist_ok=True)
        

def reportTokens(prompt, model=DEFAULT_MODEL):
    import tiktoken # keep import statements here to fit Modal container restrictions https://modal.com/docs/guide/custom-container#additional-python-packages
    encoding = tiktoken.encoding_for_model(model)
    # print number of tokens in light gray, with first 10 characters of prompt in green
    
    print('----------------')
    print(prompt)
    print('----------------')
    print(
        "\033[37m"
        + str(len(encoding.encode(prompt)))
        + " tokens\033[0m"
        + " in prompt: "
        + "\033[92m"
        + prompt[:100]
        + "\033[0m" 
        + ("..." if len(prompt) > 100 else "")
    )
    
    
def write_file(filename, filecode, directory):
    # Output the filename in blue color
    print("\033[94m" + filename + "\033[0m")
    print(filecode)
    
    file_path = os.path.join(directory, filename)
    dir = os.path.dirname(file_path)

    # Check if the filename is actually a directory
    if os.path.isdir(file_path):
        print(f"Error: {filename} is a directory, not a file.")
        return

    os.makedirs(dir, exist_ok=True)

    # Open the file in write mode
    with open(file_path, "w") as file:
        # Write content to the file
        file.write(filecode)