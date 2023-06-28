# smol developer

<a href="https://app.e2b.dev/agent/smol-developer" target="_blank" rel="noopener noreferrer">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://app.e2b.dev/api/badge_light">
  <img alt="Deploy agent on e2b button" src="https://app.e2b.dev/api/badge"/>
</picture>
</a>

***Human-centric & Coherent Whole Program Synthesis*** aka your own personal junior developer

> [Build the thing that builds the thing!](https://twitter.com/swyx/status/1657578738345979905) a `smol dev` for every dev in every situation

this is a prototype of a "junior developer" agent (aka `smol dev`) that scaffolds an entire codebase out for you once you give it a product spec, but does not end the world or overpromise AGI. instead of making and maintaining specific, rigid, one-shot starters, like `create-react-app`, or `create-nextjs-app`, this is basically [`create-anything-app`](https://news.ycombinator.com/item?id=35942352) where you develop your scaffolding prompt in a tight loop with your smol dev.

AI that is helpful, harmless, and honest is complemented by a codebase that is simple, safe, and smol - <200 lines of Python and Prompts, so this is easy to understand and customize.

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

*Not no code, not low code, but some third thing.* 

Perhaps a higher order evolution of programming where you still need to be technical, but no longer have to implement every detail at least to scaffold things out.

## examples/prompt gallery

- [6 minute video demo](https://youtu.be/UCo7YeTy-aE) - (sorry for sped up audio, we were optimizing for twitter, bad call)
  - this was the original smol developer demo - going from prompt to full chrome extension that requests and stores and apikey, generates a popup window, reads and transmits page content, and usefully summarizes any website with Anthropic Claude, switching models up to the 100k one based on length of input
  - the prompt is located in [prompt.md](https://github.com/smol-ai/developer/blob/main/prompt.md) and it outputs [/exampleChromeExtension](https://github.com/smol-ai/developer/tree/main/examples/exampleChromeExtension)
- `smol-plugin` - prompt to ChatGPT plugin ([tweet](https://twitter.com/ultrasoundchad/status/1659366507409985536?s=20), [fork](https://github.com/gmchad/smol-plugin))

  <img src="https://github.com/smol-ai/developer/assets/6764957/6ffaac3b-5d90-460a-a590-c8a8c004bd36" height=200 />

- [Prompt to Pokemon App](https://twitter.com/RobertCaracaus/status/1659312419485761536?s=20)
  
  <img src="https://github.com/smol-ai/developer/assets/6764957/15fa189a-3f52-4618-ac8e-2a77b6500264" height=200 />
  
- [Political Campaign CRM Program example](https://github.com/smol-ai/developer/pull/22/files)
- [Lessons from Creating a VSCode Extension with GPT-4](https://bit.kevinslin.com/p/leveraging-gpt-4-to-automate-the) (also on [HN](https://news.ycombinator.com/item?id=36071342))
- [7 min Video: Smol AI Developer - Build ENTIRE Codebases With A Single Prompt](https://www.youtube.com/watch?v=DzRoYc2UGKI) produces a full working OpenAI CLI python app from a prompt

  <img src="https://github.com/smol-ai/developer/assets/6764957/e80058f1-ea9c-42dd-87ff-004b61f08f2e" height=200 />
  
- [12 min Video: SMOL AI - Develop Large Scale Apps with AGI in one click](https://www.youtube.com/watch?v=zsxyqz6SYp8) scaffolds a surprisingly complex React/Node/MongoDB full stack app in 40 minutes and $9

  <img src="https://github.com/smol-ai/developer/assets/6764957/c51f9f8c-021d-446a-b44d-7a6f48e64550" height=200 />

I'm actively seeking more examples, please PR yours! 

sorry for the lack of examples, I know that is frustrating but I wasnt ready for so many of you lol

## major forks/alternatives

please send in alternative implementations, and deploy strategies on alternative stacks!

- **JS/TS**: https://github.com/PicoCreator/smol-dev-js A pure JS variant of smol-dev, allowing even smoler incremental changes via prompting (if you dun want to do the whole spec2code thing), allowing you to plug it into any project live (for better or worse)
- **C#/Dotnet**: https://github.com/colhountech/smol-ai-dotnet in C#!
- **Golang**: https://github.com/tmc/smol-dev-go in Go
- https://github.com/gmchad/smol-plugin automatically generate @openai plugins by specifying your API in markdown in smol-developer style
- your fork here!

## arch diagram

naturally generated with gpt4, like [we did for babyagi](https://twitter.com/swyx/status/1648724820316786688)
![image](https://github.com/smol-ai/developer/assets/6764957/f8fc68f4-77f6-43ee-852f-a35fb195430a)


### innovations and insights

> Please subscribe to https://latent.space/ for a fuller writeup and insights and reflections

- **Markdown is all you need** - Markdown is the perfect way to prompt for whole program synthesis because it is easy to mix english and code (whether `variable_names` or entire \`\`\` code fenced code samples)
  - turns out you can specify prompts in code in prompts and gpt4 obeys that to the letter
- **Copy and paste programming**
  - teaching the program to understand how to code around a new API (Anthropic's API is after GPT3's knowledge cutoff) by just pasting in the `curl` input and output
  - pasting error messages into the prompt and vaguely telling the program how you'd like it handled. it kind of feels like "logbook driven programming".
- **Debugging by `cat`ing** the whole codebase with your error message and getting specific fix suggestions - particularly delightful!
- **Tricks for whole program coherence** - our chosen example usecase, Chrome extensions, have a lot of indirect dependencies across files. Any hallucination of cross dependencies causes the whole program to error. 
  - We solved this by adding an intermediate step asking GPT to think through `shared_dependencies.md`, and then insisting on using that in generating each file. This basically means GPT is able to talk to itself...
  - ... but it's not perfect, yet. `shared_dependencies.md` is sometimes not comperehensive in understanding what are hard dependencies between files. So we just solved it by specifying a specific `name` in the prompt. felt dirty at first but it works, and really it's just clear unambiguous communication at the end of the day. 
  - see `prompt.md` for SOTA smol-dev prompting
- **Low activation energy for unfamiliar APIs**
  - we have never really learned css animations, but now can just say we want a "juicy css animated red and white candy stripe loading indicator" and it does the thing. 
  - ditto for Chrome Extension Manifest v3 - the docs are an abject mess, but fortunately we don't have to read them now to just get a basic thing done
  - the Anthropic docs (bad bad) were missing guidance on what return signature they have. so just curl it and dump it in the prompt lol.
- **Modal is all you need** - we chose Modal to solve 4 things:
  - solve python dependency hell in dev and prod
  - parallelizable code generation
  - simple upgrade path from local dev to cloud hosted endpoints (in future)
  - fault tolerant openai api calls with retries/backoff, and attached storage (for future use)

> Please subscribe to https://latent.space/ for a fuller writeup and insights and reflections

### caveats

We were working on a Chrome Extension, which requires images to be generated, so we added some usecase specific code in there to skip destroying/regenerating them, that we haven't decided how to generalize.

We dont have access to GPT4-32k, but if we did, we'd explore dumping entire API/SDK documentation into context.

The feedback loop is very slow right now (`time` says about 2-4 mins to generate a program with GPT4, even with parallelization due to Modal (occasionally spiking higher)), but it's a safe bet that it will go down over time (see also "future directions" below).

## install

it's basically: 

- `git clone https://github.com/smol-ai/developer`.
- copy over `.example.env` to `.env` filling in your API keys.

There are no python dependencies to wrangle thanks to using Modal as a [self-provisioning runtime](https://www.google.com/search?q=self+provisioning+runtime).

Unfortunately this project also uses 3 other things:

- Modal.com - [sign up](https://modal.com/signup), then `pip install modal-client && modal token new`
  - You can run this project w/o Modal following these instructions:
  - `pip install -r requirements.txt`
  - `export OPENAI_API_KEY=sk-xxxxxx` (your openai api key here)
  - `python main_no_modal.py YOUR_PROMPT_HERE`
- GPT-4 api (private beta) - this project now defaults to using `gpt-3.5-turbo` but it obviously wont be as good. we are working on a hosted version so you can try this out on our keys.
- (for the demo project only) anthropic claude 100k context api (private beta) - not important unless you're exactly trying to repro my demo

you'll have to adapt this code on a fork if you want to use it on other infra. please open issues/PRs and i'll happily highlight your fork here.

### trying the example chrome extension from the demo video

the `/examples/exampleChromeExtension` folder contains `a Chrome Manifest V3 extension that reads the current page, and offers a popup UI that has the page title+content and a textarea for a prompt (with a default value we specify). When the user hits submit, it sends the page title+content to the Anthropic Claude API along with the up to date prompt to summarize it. The user can modify that prompt and re-send the prompt+content to get another summary view of the content.`

- go to Manage Extensions in Chrome
- load unpacked
- find the relevant folder in your file system and load it
- go to any content heavy site
- click the cute bird
- see it work and rejoice

this entire extension was generated by the prompt in `prompt.md` (except for the images), and was built up over time by adding more words to the prompt in an iterative process.

## usage: smol dev

basic usage (by default it runs with `gpt-3.5-turbo`, but we strongly encourage running with `gpt-4` if you have access)

```bash
# inline prompt
modal run main.py --prompt "a Chrome extension that, when clicked, opens a small window with a page where you can enter a prompt for reading the currently open page and generating some response from openai" --model=gpt-4
```

after a while of adding to your prompt, you can extract your prompt to a file, as long as your "prompt" ends in a .md extension we'll go look for that file

```bash
# prompt in markdown file
modal run main.py --prompt prompt.md --model=gpt-4
```

each time you run this, the generated directory is deleted (except for images) and all files are rewritten from scratch. 

In the `shared_dependencies.md` file is a helper file that ensures coherence between files. This is in the process of being expanded into an official `--plan` functionality (see https://github.com/smol-ai/developer/issues/12)

### smol dev in single file mode

if you make a tweak to the prompt and only want it to affect one file, and keep the rest of the files, specify the file param:

```bash
modal run main.py --prompt prompt.md  --file popup.js
```

### smol dev without modal.com

By default, `main.py` uses Modal, beacuse it provides a nice upgrade path to a hosted experience (coming soon, so you can try it out without needing GPT4 key access).

However if you want to just run it on your own machine, you can run smol dev w/o Modal following these instructions:

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-xxxxxx # your openai api key here)

python main_no_modal.py YOUR_PROMPT_HERE
```

If no command line argument is given, **and** the file `prompt.md` exists, the main function will automatically use the `prompt.md` file. All other command line arguments are left as default. *this is handy for those using the "run" function on a `venv` setup in PyCharm for Windows, where no opportunity is given to enter command line arguments. Thanks [@danmenzies](https://github.com/smol-ai/developer/pull/55)* 

## usage: smol debugger

*this is a beta feature, very very MVP, just a proof of concept really*

take the entire contents of the generated directory in context, feed in an error, get a response. this basically takes advantage of longer (32k-100k) context so we basically dont have to do any embedding of the source.

```bash
modal run debugger.py --prompt "Uncaught (in promise) TypeError: Cannot destructure property 'pageTitle' of '(intermediate value)' as it is undefined.    at init (popup.js:59:11)"

# gpt4
modal run debugger.py --prompt "your_error msg_here" --model=gpt-4
```

## usage: smol pm

*this is even worse than beta, its kind of a "let's see what happens" experiment*

take the entire contents of the generated directory in context, and get a prompt back that could synthesize the whole program. basically `smol dev`, in reverse.

```bash
modal run code2prompt.py # ~0.5 second with gpt 3.5

# use gpt4
modal run code2prompt.py --model=gpt-4 # 2 mins, MUCH better results
```

We have done indicative runs of both, stored in `examples/code2prompt/code2prompt-gpt3.md` vs `examples/code2prompt/code2prompt-gpt4.md`. Note how incredibly better gpt4 is at prompt engineering its future self.

Naturally, we had to try `code2prompt2code`...

```bash
# add prompt... this needed a few iterations to get right
modal run code2prompt.py --prompt "make sure all the id's of the DOM elements, and the data structure of the page content (stored with {pageTitle, pageContent }) , referenced/shared by the js files match up exactly. take note to only use Chrome Manifest V3 apis. rename the extension to code2prompt2code" --model=gpt-4 # takes 4 mins. produces semi working chrome extension copy based purely on the model-generated description of a different codebase

# must go deeper
modal run main.py --prompt code2prompt-gpt4.md --directory code2prompt2code
```

We leave the social and technical impacts of multilayer generative deep-frying of codebases as an exercise to the reader.

## Development using a Dev Container

> this is a [new addition](https://github.com/smol-ai/developer/pull/30)! Please try it out and send in fixes if there are any issues.

We have configured a development container for this project, which provides an isolated and consistent development environment. This approach is ideal for developers using Visual Studio Code's Remote - Containers extension or GitHub's Codespaces.

If you have [VS Code](https://code.visualstudio.com/download) and [Docker](https://www.swyx.io/running-docker-without-docker-desktop) installed on your machine, you can make use of the devcontainer to create an isolated environment with all dependencies automatically installed and configured. This is a great way to ensure a consistent development experience across different machines.

Here are the steps to use the devcontainer:

1. Open this project in VS Code.
2. When prompted to "Reopen in Container", choose "Reopen in Container". This will start the process of building the devcontainer defined by the `Dockerfile` and `.devcontainer.json` in the `.devcontainer` directory.
3. Wait for the build to finish. The first time will be a bit longer as it downloads and builds everything. Future loads will be much faster.
4. Once the build is finished, the VS Code window will reload and you are now working inside the devcontainer.


<details>
<summary> Benefits of a Dev Container </summary>

1. **Consistent Environment**: Every developer works within the same development setup, eliminating "it works on my machine" issues and easing the onboarding of new contributors.

2. **Sandboxing**: Your development environment is isolated from your local machine, allowing you to work on multiple projects with differing dependencies without conflict.

3. **Version Control for Environments**: Just as you version control your source code, you can do the same with your development environment. If a dependency update introduces issues, it's easy to revert to a previous state.

4. **Easier CI/CD Integration**: If your CI/CD pipeline utilizes Docker, your testing environment will be identical to your local development environment, ensuring consistency across development, testing, and production setups.

5. **Portability**: This setup can be utilized on any computer with Docker and the appropriate IDE installed. Simply clone the repository and start the container.
</details>


## future directions

things to try/would accept open issue discussions and PRs:

- **specify .md files for each generated file**, with further prompts that could finetune the output in each of them
  - so basically like `popup.html.md` and `content_script.js.md` and so on
- **bootstrap the `prompt.md`** for existing codebases - write a script to read in a codebase and write a descriptive, bullet pointed prompt that generates it
  - done by `smol pm`, but its not very good yet - would love for some focused polish/effort until we have quine smol developer that can generate itself lmao
- **ability to install its own dependencies**
  - this leaks into depending on the execution environment, which we all know is the path to dependency madness. how to avoid? dockerize? nix? [web container](https://twitter.com/litbid/status/1658154530385670150)?
  - Modal has an interesting possibility: generate functions that speak modal which also solves the dependency thing https://twitter.com/akshat_b/status/1658146096902811657
- **self-heal** by running the code itself and use errors as information for reprompting 
  - however its a bit hard to get errors from the chrome extension environment so we did not try this
- **using anthropic as the coding layer**
  - you can run `modal run anthropic.py --prompt prompt.md --outputdir=anthropic` to try it
  - but it doesnt work because anthropic doesnt follow instructions to generate file code very well.
- **make agents that autonomously run this code in a loop/watch the prompt file** and regenerate code each time, on a new git branch
  - the code could be generated on 5 simultaneous git branches and checking their output would just involve switching git branches
