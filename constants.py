EXTENSION_TO_SKIP = [".png",".jpg",".jpeg",".gif",".bmp",".svg",".ico",".tif",".tiff"]
DEFAULT_DIR = "generated"
DEFAULT_MODEL = "gpt-3.5-turbo" # we recommend 'gpt-4' if you have it # gpt3.5 is going to be worse at generating code so we strongly recommend gpt4. i know most people dont have access, we are working on a hosted version 
DEFAULT_MAX_TOKENS = 2000 # i wonder how to tweak this properly. we dont want it to be max length as it encourages verbosity of code. but too short and code also truncates suddenly.