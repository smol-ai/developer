# smol developer

this is a prototype of a bot that scaffolds code out for you once you give it a goal. it uses Modal and GPT4, both of which require invites, sorry.

## dev

```bash
modal run main.py --prompt "a Chrome extension that, when clicked, opens a small window with a page where you can enter a prompt for reading the currently open page and generating some response from openai"   
```

```bash
modal run main.py --prompt "a Chrome extension that, when clicked, opens a small window with a nicely styled page where you can enter a prompt for reading the currently open page and generating some response from openai. if there is no openai key stored, it should prompt for one and store the openai key for future usage. It has to run in a browser environment, so no Nodejs APIs allowed."
```