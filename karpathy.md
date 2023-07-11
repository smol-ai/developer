# Anki Flash Card Generator

https://twitter.com/karpathy/status/1663262981302681603

a Chrome extension that, when clicked, opens a small window with a page where you can enter a prompt for reading the currently open page and generating anki flash cards from the page content using the openai gpt-4 chatcompletion api

## details of the chrome extension

- follows Chrome Manifest v3
- it is a chrome extension so only clientside js using chrome extension api's allowed
- has a default icon named `icon.png` in the root folder
- min height 600, width 400, center all content

- when the user opens the popup:
  - injects a content script that reads all content and sends it over to the popup
  - ask me for my OpenAI api key, and when the user presses submit, use the user's API key to read the page content and create some anki cards in this format (from https://chat.openai.com/share/a54de047-8796-47b4-937d-5b7dc70bc16e):

{QUESTION}
A: {CANDIDATE ANSWER 1}
B: {CANDIDATE ANSWER 2}
C: {CANDIDATE ANSWER 3}
D: {CANDIDATE ANSWER 4}
Answer: {LETTER}

For example:

What is the most populous state of the United States?
A: Florida
B: Texas
C: California
D: New York
Answer: C

You'll notice that the Multiple Choice options are designed to be somewhat hard, with distractor answers that are plausible (e.g. Texas, Florida and New York are quite populous but not the most populous). 

## chatcompletion api example

<!-- https://platform.openai.com/docs/api-reference/chat -->

example request

curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

example params

{
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "Hello!"}]
}


example response

{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
