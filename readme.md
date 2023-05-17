# smol developer

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
  - *paste the error into the prompt* just like they would file a github issue
  - for extra help, they can use `debugger.py` which reads the whole codebase to make specific code change suggestions

Loop until happiness is attained. Notice that AI is only used as long as it is adding value - once it gets in your way, just take over the codebase from your smol junior developer with no fuss and no hurt feelings. (*we could also have smol-dev take over an existing codebase and bootstrap its own prompt... but that's a Future Direction*)

*Not no code, not low code, but some third thing.* 

Perhaps a higher order evolution of programming where you still need to be technical, but no longer have to implement every detail at least to scaffold things out.

## video demo

[![https://i3.ytimg.com/vi/UCo7YeTy-aE/hqdefault.jpg](https://i3.ytimg.com/vi/UCo7YeTy-aE/hqdefault.jpg)](https://youtu.be/UCo7YeTy-aE)

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

Unfortunately this project also uses 3 waitlisted things:

- Modal.com - `pip install modal-client` (private beta - hit up the modal team to get an invite, and login)
  - You can run this project w/o Modal following these instructions:
  - `pip install -r requirements.txt`
  - `python main_no_modal.py YOUR_PROMPT_HERE`
- GPT-4 api (private beta) - can use 3.5 but obviously wont be as good
- (for the demo project) anthropic claude 100k context api (private beta)

> yes, the most important skill in being an ai engineer is social engineering to get off waitlists. Modal will let you in if you say the keyword "swyx"

you'll have to adapt this code on a fork if you want to use it on other infra. please open issues/PRs and i'll happily highlight your fork here.

### trying the example chrome extension

the `/generated` and `/exampleChromeExtension` folder contains `a Chrome Manifest V3 extension that reads the current page, and offers a popup UI that has the page title+content and a textarea for a prompt (with a default value we specify). When the user hits submit, it sends the page title+content to the Anthropic Claude API along with the up to date prompt to summarize it. The user can modify that prompt and re-send the prompt+content to get another summary view of the content.`

- go to Manage Extensions in Chrome
- load unpacked
- find the relevant folder in your file system and load it
- go to any content heavy site
- click the cute bird
- see it work

this entire extension was generated by the prompt in `prompt.md` (except for the images), and was built up over time by adding more words to the prompt in an iterative process.

## smol dev

basic usage

```bash
modal run main.py --prompt "a Chrome extension that, when clicked, opens a small window with a page where you can enter a prompt for reading the currently open page and generating some response from openai"   
```

after a while of adding to your prompt, you can extract your prompt to a file, as long as your "prompt" ends in a .md extension we'll go look for that file

```bash
modal run main.py --prompt prompt.md   
```

each time you run this, the generated directory is deleted (except for images) and all files are rewritten from scratch. 

In the `shared_dependencies.md` file is a helper file that ensures coherence between files.

if you make a tweak to the prompt and only want it to affect one file, and keep the rest of the files, specify the file param:

```bash
modal run main.py --prompt prompt.md  --file popup.js
```

## smol debugger

take the entire contents of the generated directory in context, feed in an error, get a response. this basically takes advantage of longer (32k-100k) context so we basically dont have to do any embedding of the source.

```bash
modal run debugger.py --prompt "Uncaught (in promise) TypeError: Cannot destructure property 'pageTitle' of '(intermediate value)' as it is undefined.    at init (popup.js:59:11)"

# gpt4
modal run debugger.py --prompt "your_error msg_here" --model=gpt-4
```

## smol pm

take the entire contents of the generated directory in context, and get a prompt back that could synthesize the whole program. basically `smol dev`, in reverse.

```bash
modal run code2prompt.py # ~0.5 second

# use gpt4
modal run code2prompt.py --model=gpt-4 # 2 mins, MUCH better results
```

We have done indicative runs of both, stored in `code2prompt-gpt3.md` vs `code2prompt-gpt4.md`. Note how incredibly better gpt4 is at prompt engineering its future self.

Naturally, we had to try `code2prompt2code`...

```bash
# add prompt... this needed a few iterations to get right
modal run code2prompt.py --prompt "make sure all the id's of the DOM elements, and the data structure of the page content (stored with {pageTitle, pageContent }) , referenced/shared by the js files match up exactly. take note to only use Chrome Manifest V3 apis. rename the extension to code2prompt2code" --model=gpt-4 # takes 4 mins. produces semi working chrome extension copy based purely on the model-generated description of a different codebase

# must go deeper
modal run main.py --prompt code2prompt-gpt4.md --directory code2prompt2code
```

We leave the social and technical impacts of multilayer generative deep-frying of codebases as an exercise to the reader.

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
