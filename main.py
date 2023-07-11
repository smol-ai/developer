import sys

from smol_dev.prompts import plan, specify_file_paths, generate_code_sync
from smol_dev.utils import generate_folder, write_file
from smol_dev.main import main
import argparse




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
        parser.add_argument("--prompt", type=str, help="Prompt for the app to be created.")
        parser.add_argument("--model", type=str, default="gpt-4-0613", help="model to use. can also use gpt-3.5-turbo-0613")
        parser.add_argument("--generate_folder_path", type=str, default="generated", help="Path of the folder for generated code.")
        parser.add_argument("--debug", type=bool, default=False, help="Enable or disable debug mode.")
        args = parser.parse_args()
        if args.prompt:
            prompt = args.prompt

    # read file from prompt if it ends in a .md filetype
    if len(prompt) < 100 and prompt.endswith(".md"):
        with open(prompt, "r") as promptfile:
            prompt = promptfile.read()

    print(prompt)
        
    main(prompt=prompt, generate_folder_path=args.generate_folder_path, debug=args.debug, model=args.model)
