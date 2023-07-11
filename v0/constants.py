EXTENSION_TO_SKIP = [".png",".jpg",".jpeg",".gif",".bmp",".svg",".ico",".tif",".tiff"]
DEFAULT_DIR = "generated"

# we use the 0613 version of the models because we rely on the function calling API
DEFAULT_MODEL = "gpt-4-0613" # we recommend 'gpt-4-0613' if you have it, it will be slower but better at coding. use gpt-4-32k if you have it
#  DEFAULT_MODEL = "gpt-3.5-turbo-0613" # gpt3.5 is going to be worse at generating code but faster. 
DEFAULT_MAX_TOKENS = 2000 # i wonder how to tweak this properly. we dont want it to be max length as it encourages verbosity of code. but too short and code also truncates suddenly.