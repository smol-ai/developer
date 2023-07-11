import sys
import time

from smol_dev.prompts import plan, specify_file_paths, generate_code_sync
from smol_dev.utils import generate_folder, write_file
import argparse

# model = "gpt-3.5-turbo-0613"
defaultmodel = "gpt-4-0613"

def main(prompt, generate_folder_path="generated", debug=False, model: str = defaultmodel):
    # create generateFolder folder if doesnt exist
    generate_folder(generate_folder_path)

    # plan shared_deps
    if debug:
        print("--------shared_deps---------")
    with open(f"{generate_folder_path}/shared_deps.md", "wb") as f:

        start_time = time.time()
        def stream_handler(chunk):
            f.write(chunk)
            if debug:
                end_time = time.time()

                sys.stdout.write("\r \033[93mChars streamed\033[0m: {}. \033[93mChars per second\033[0m: {:.2f}".format(stream_handler.count, stream_handler.count / (end_time - start_time)))
                sys.stdout.flush()
                stream_handler.count += len(chunk)

        stream_handler.count = 0
        stream_handler.onComplete = lambda x: sys.stdout.write("\033[0m\n") # remove the stdout line when streaming is complete

        shared_deps = plan(prompt, stream_handler, model=model)
    if debug:
        print(shared_deps)
    write_file(f"{generate_folder_path}/shared_deps.md", shared_deps)
    if debug:
        print("--------shared_deps---------")

    # specify file_paths
    if debug:
        print("--------specify_filePaths---------")
    file_paths = specify_file_paths(prompt, shared_deps, model=model)
    if debug:
        print(file_paths)
    if debug:
        print("--------file_paths---------")

    # loop through file_paths array and generate code for each file
    for file_path in file_paths:
        file_path = f"{generate_folder_path}/{file_path}"  # just append prefix
        if debug:
            print(f"--------generate_code: {file_path} ---------")

        start_time = time.time()
        def stream_handler(chunk):
            if debug:
                end_time = time.time()
                sys.stdout.write("\r \033[93mChars streamed\033[0m: {}. \033[93mChars per second\033[0m: {:.2f}".format(stream_handler.count, stream_handler.count / (end_time - start_time)))
                sys.stdout.flush()
                stream_handler.count += len(chunk)
        stream_handler.count = 0
        stream_handler.onComplete = lambda x: sys.stdout.write("\033[0m\n") # remove the stdout line when streaming is complete
        code = generate_code_sync(prompt, shared_deps, file_path, stream_handler, model=model)
        if debug:
            print(code)
        if debug:
            print(f"--------generate_code: {file_path} ---------")
        # create file with code content
        write_file(file_path, code)
        
    print("--------smol dev done!---------")


# for local testing
# python main.py --prompt "a simple JavaScript/HTML/CSS/Canvas app that is a one player game of PONG..." --generate_folder_path "generated" --debug True

if __name__ == "__main__":
    prompt = """
  a simple JavaScript/HTML/CSS/Canvas app that is a one player game of PONG. 
  The left paddle is controlled by the player, following where the mouse goes.
  The right paddle is controlled by a simple AI algorithm, which slowly moves the paddle toward the ball at every frame, with some probability of error.
  Make the canvas a 400 x 400 black square and center it in the app.
  Make the paddles 100px long, yellow and the ball small and red.
  Make sure to render the paddles and name them so they can controlled in javascript.
  Implement the collision detection and scoring as well.
  Every time the ball bouncess off a paddle, the ball should move faster.
  It is meant to run in Chrome browser, so dont use anything that is not supported by Chrome, and don't use the import and export keywords.
  """
    if len(sys.argv) == 2:
        prompt = sys.argv[1]
    else:
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--prompt", type=str, required=True, help="Prompt for the app to be created.")
        parser.add_argument("--generate_folder_path", type=str, default="generated", help="Path of the folder for generated code.")
        parser.add_argument("--debug", type=bool, default=False, help="Enable or disable debug mode.")
        args = parser.parse_args()
        if args.prompt:
            prompt = args.prompt
        
    print(prompt)
        
    main(prompt=prompt, generate_folder_path=args.generate_folder_path, debug=args.debug)
