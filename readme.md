# 🐣 smol developer

<a href="https://app.e2b.dev/agent/smol-developer" target="_blank" rel="noopener noreferrer">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://app.e2b.dev/api/badge_light">
  <img alt="Deploy agent on e2b button" src="https://app.e2b.dev/api/badge"/>
</picture>
</a>

***Human-centric & Coherent Whole Program Synthesis*** aka your own personal junior developer

> [Build the thing that builds the thing!](https://twitter.com/swyx/status/1657578738345979905) a `smol dev` for every dev in every situation

This is a prototype of a "junior developer" agent (aka `smol dev`) that scaffolds an entire codebase out for you once you give it a product spec, but does not end the world or overpromise AGI. instead of making and maintaining specific, rigid, one-shot starters, like `create-react-app`, or `create-nextjs-app`, this is basically [`create-anything-app`](https://news.ycombinator.com/item?id=35942352) where you develop your scaffolding prompt in a tight loop with your smol dev.

After the [successful initial v0 launch](https://twitter.com/swyx/status/1657578738345979905), smol developer was rewritten to be **even smol-ler**, and importable from a library!

## Basic Usage

### In Git Repo mode

```bash
# install 
git clone https://github.com/smol-ai/developer.git
cd developer
poetry install # install dependencies

# run
python main.py "a HTML/JS/CSS Tic Tac Toe Game" # defaults to gpt-4-0613
# python main.py "a HTML/JS/CSS Tic Tac Toe Game" --model=gpt-3.5-turbo-0613

# other cli flags 
python main.py --prompt prompt.md # for longer prompts, move them into a markdown file
python main.py --prompt prompt.md --debug True # for debugging
```

<details>
  <summary>
This lets you develop apps as a human in the loop, as per the original version of smol developer.
  </summary>


<p align="center">
  <img height=200 src="https://pbs.twimg.com/media/FwEzVCcaMAE7t4h?format=jpg&name=large" />
</p>

*engineering with prompts, rather than prompt engineering* 

The demo example in `prompt.md` shows the potential of AI-enabled, but still firmly human developer centric, workflow:

- Human writes a basic prompt for the app they want to build
- `main.py` generates code
- Human runs/reads the code
- Human can:
  - simply add to the prompt as they discover underspecified parts of the prompt
  - manually runs the code and identifies errors
  - *paste the error into the prompt* just like they would file a GitHub issue
  - for extra help, they can use `debugger.py` which reads the whole codebase to make specific code change suggestions

Loop until happiness is attained. Notice that AI is only used as long as it is adding value - once it gets in your way, just take over the codebase from your smol junior developer with no fuss and no hurt feelings. (*we could also have smol-dev take over an existing codebase and bootstrap its own prompt... but that's a Future Direction*)

</details>

In this way you can use your clone of this repo itself to prototype/develop your app.

### In Library mode 

This is the new thing in smol developer v1! Add `smol developer` to your own projects!

```bash
pip install smol-dev
``` 

Here you can basically look at the contents of `main.py` as our "documentation" of how you can use these functions and prompts in your own app:

```python
from smol_dev.prompts import plan, specify_file_paths, generate_code_sync

prompt = "a HTML/JS/CSS Tic Tac Toe Game"

shared_deps = plan(prompt) # returns a long string representing the coding plan

# do something with the shared_deps plan if you wish, for example ask for user confirmation/edits and iterate in a loop

file_paths = specify_file_paths(prompt, shared_deps) # returns an array of strings representing the filenames it needs to write based on your prompt and shared_deps. Relies on OpenAI's new Function Calling API to guarantee JSON.

# do something with the filepaths if you wish, for example display a plan

# loop through file_paths array and generate code for each file
for file_path in file_paths:
    code = generate_code_sync(prompt, shared_deps, file_path) # generates the source code of each file
    
    # do something with the source code of the file, eg. write to disk or display in UI
    # there is also an async `generate_code()` version of this
```


