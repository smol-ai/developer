import sys

from smol_dev.prompts import plan, specify_file_paths, generate_code_sync
from smol_dev.utils import generate_folder, write_file
from smol_dev.main import main
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True, type=str, help="Prompt for the app to be created.")
    parser.add_argument("--model", type=str, default="gpt-4-0613", help="model to use. can also use gpt-3.5-turbo-0613")
    parser.add_argument("--generate_folder_path", type=str, default="generated", help="Path of the folder for generated code.")
    parser.add_argument("--debug", type=bool, default=False, help="Enable or disable debug mode.")
    args = parser.parse_args()

    # read file from prompt if it ends in a .md filetype
    if len(args.prompt) < 100 and args.prompt.endswith(".md"):
        with open(args.prompt, "r") as promptfile:
            args.prompt = promptfile.read()

    print(args.prompt)
    main(prompt=args.prompt, generate_folder_path=args.generate_folder_path, debug=args.debug, model=args.model)
