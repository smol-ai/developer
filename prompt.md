a Chrome Manifest V3 extension that reads the current page, and offers a popup UI that sends the page content to the Anthropic Claude API along with a prompt to summarize it, and lets the user modify that prompt and re-send the prompt+content to get another summary view of the content.

When clicked:
- pops up a small window with a simple, modern, slick, minimalistic styled html popup
  - checks its own storage, and asks for an API key to Anthropic Claude if it isn't stored, and stores it
  - which accesses the title and main content of the currently open page (extracted via an injected content script, and sent over using a 'pageContent' action) and renders it in a <details>/<summary> tag on the popup page under a "Full article" <summary> tag (tastefully styled).
  - from the popup script, calls the Anthropic model endpoint https://api.anthropic.com/v1/complete with the `claude-instant-v1` model with the page content, prompting it to ask for a detailed, bullet pointed, easy to read HTML summary of the given content.
  - renders the Anthropic-generated HTML summary inside of the popup in a div with an id of content
  - at the bottom of the popup, show a textbox with a default value of the same prompt that we used and send button that lets the user re-ask Anthropic with the same content but different prompt. disable these inputs while it waits.

Remember:

- It has to run in a browser environment, so no Nodejs APIs allowed.

- Have background.js store the title and content when it receives the { action: "pageContent" } message.
Then, when it receives a { action: "pageContent" } message, it should respond with the stored title and content.

- have a "Read page content of {TITLE}. Loading..." message while waiting for the anthropic api to return, with the TITLE being the page title. do not show it until the api call begins, and clear it when it ends.

- the return signature of the anthropic api is curl https://api.anthropic.com/v1/complete\
  -H "x-api-key: $API_KEY"\
  -H 'content-type: application/json'\
  -d '{
    "prompt": "\n\nHuman: Tell me a haiku about trees\n\nAssistant: ",
    "model": "claude-v1", "max_tokens_to_sample": 300, "stop_sequences": ["\n\nHuman:"]
  }'
{"completion":" Here is a haiku about trees:\n\nSilent sentinels, \nStanding solemn in the woods,\nBranches reaching sky.","stop":"\n\nHuman:","stop_reason":"stop_sequence","truncated":false,"log_id":"f5d95cf326a4ac39ee36a35f434a59d5","model":"claude-v1","exception":null}

- in the string prompt sent to anthropic, first include the page title and page content, and finally append the prompt, clearly vertically separated by spacing.

- if the anthropic api call is a 401, handle that by clearing the stored anthropic api key and asking for it again.

- use <link rel="stylesheet" href="https://unpkg.com/mvp.css@1.12/mvp.css"> for styling the popup and add styles to make sure the default styling follows the basic rules of web design, for example having margins around the body, a system font stack, and nice vertical spacing.

- give the popup window a minimum width of 400 and height of 600