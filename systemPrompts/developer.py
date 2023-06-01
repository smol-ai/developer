import re
import inspect

def intercept(fstring):
    frame = inspect.currentframe().f_back
    code = frame.f_code
    filename = code.co_filename
    line_number = code.co_firstlineno
    locals_dict = frame.f_locals

    # Extract expressions within the f-string
    regex = r'\{([^{}]+)\}'
    expressions = re.findall(regex, fstring)

    # Process the expressions
    components = []
    for expr in expressions:
        # Unescape braces
        expr = expr.replace('{{', '{').replace('}}', '}')

        # Evaluate the expression
        result = eval(expr, globals(), locals_dict)
        components.append(result)

    # Log or perform any desired actions with the components
    print("Intercepted components:", components)
    print("File:", filename)
    print("Line number:", line_number)

    # Pass through the f-string as-is
    return fstring


def call(fstring):
    print("Original f-string:", fstring)




def planPrompt1():
  return """You are an AI developer who is trying to write a program that will generate code for the user based on their intent.

  When given their intent, create a complete, exhaustive list of filepaths that the user would write to make the program.

  only list the filepaths you would write, and return them as a python list of strings.
  do not add any other explanation, only return a python list of strings.
  """
  
def planPrompt2(sourcePrompt, filepaths_string):
  
  return """You are an AI developer who is trying to write a program that will generate code for the user based on their intent.

  In response to the user's prompt:

  ---
  the app is: {prompt}
  ---

  the files we have decided to generate are: {filepaths_string}

  Now that we have a list of files, we need to understand what dependencies they share.
  Please name and briefly describe what is shared between the files we are generating, including exported variables, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.
  Exclusively focus on the names of the shared dependencies, and do not add any other explanation.
  """
  

def filePrompt(sourcePrompt, filepaths_string, filename):
  systemPrompt = f"""You are an AI developer who is trying to write a program that will generate code for the user based on their intent.

    the app is: {sourcePrompt}

    the files we have decided to generate are: {filepaths_string}

    the shared dependencies (like filenames and variable names) we have decided on are: {shared_dependencies}

    only write valid code for the given filepath and file type, and return only the code.
    do not add any other explanation, only return valid code for that file type.
    """
  userPrompt =  f"""
    We have broken up the program into per-file generation.
    Now your job is to generate only the code for the file {filename}.
    Make sure to have consistent filenames if you reference other files we are also generating.

    Remember that you must obey 3 things:
       - you are generating code for the file {filename}
       - do not stray from the names of the files and the shared dependencies we have decided on
       - MOST IMPORTANT OF ALL - every line of code you generate must be valid code. Do not include code fences in your response, for example

    Bad response:
    ```javascript
    console.log("hello world")
    ```

    Good response:
    console.log("hello world")

    Begin generating the code now.

    """,
  return systemPrompt, userPrompt