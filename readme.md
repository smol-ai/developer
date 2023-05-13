# smol developer

this is a prototype of a bot that scaffolds code out for you once you give it a goal. it uses Modal and GPT4, both of which require invites, sorry.

it works, but it doesnt produce working code yet.

## dev

```bash
modal run main.py --prompt "a Chrome extension that, when clicked, opens a small window with a page where you can enter a prompt for reading the currently open page and generating some response from openai"   
```

```bash
modal run main.py --prompt "a Chrome extension that, when clicked, opens a small window with a nicely styled page where you can enter a prompt for reading the currently open page and generating some response from openai. if there is no openai key stored, it should prompt for one and store the openai key for future usage. It has to run in a browser environment, so no Nodejs APIs allowed."
```

## future directions

we have paused on this for now, but we could:

- specify .md files with further prompts that could finetune the output in each of them
- make agents that autonomously check for change in the spec and regenerates the file
- use errors as information - however its a bit hard to get errors from the chrome extension environment