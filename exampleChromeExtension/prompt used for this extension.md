a Chrome Manifest V3 extension that reads the current page, and offers a popup UI that sends the page content to the Anthropic Claude API along with a prompt to summarize it, and lets the user modify that prompt and re-send the prompt+content to get another summary view of the content.


- When clicked:
  - it injects a content script `content_script.js` on the currently open tab, 
  and accesses the title `pageTitle` and main content `pageContent` of the currently open page 
  (extracted via an injected content script, and sent over using a `storePageContent` action) 
  - in the background, receives the `storePageContent` data and stores it
  - pops up a small window with a simple, modern, slick, minimalistic styled html popup
  - in the popup script
    - retrieves the page content data using a `getPageContent` action (and the background listens for the `getPageContent` action and retrieves that data) 
    - check extension storage for an `apiKey`, and if it isn't stored, asks for an API key to Anthropic Claude and stores it.
    - calls the Anthropic model endpoint https://api.anthropic.com/v1/complete with the `claude-instant-v1-100k` model with: 
      - append the page title
      - append the page content
      - append a prompt to ask for a detailed, easy to read HTML summary of the given content with 3-4 highlights per section with important keywords bolded and important links preserved.
        in this format:
        ```js
        defaultPrompt = `Human: Please provide a detailed, easy to read HTML summary of the given content 
        with 3-4 highlights per section with important keywords bolded and important links preserved, in this format:
        
        <h1>{title here}</h1>
        <h2>{section title here}</h2>
        <ul>
          <!-- if there is an important, relevant image --> <img src={main image, if any} style="height:8rem">
          <li><strong>{first point}</strong>: {short explanation with details, with any relevant links included}</li>
          <li><strong>{second point}</strong>: {short explanation with details, with any relevant links included}</li>
          <li><strong>{third point}</strong>: <!-- etc -->
          <!-- etc -->
        </ul>
        <h2>{second section here}</h2>
        <ul>
          <!-- etc -->
        </ul>
        <!-- etc -->

        With all the words in brackets replaced by the summary of the content. Only draw from the source content, do not hallucinate.

        Assistant:`;
        ```js
    - renders the Anthropic-generated HTML summary inside of the popup in a div with an id of content
  - at the bottom of the popup, show a textarea with an id of `userPrompt` with a short default value prompt, and a submit button with an id of `sendButton`.
    - when `sendButton` is clicked, lets the user re-ask Anthropic with the same page title and page content but different prompt (from `userPrompt`).
    - disable these inputs while it waits for the Anthropic api call to complete

Important Details:

- It has to run in a browser environment, so no Nodejs APIs allowed.

- the popup should show a "Read page content of {TITLE}" message with a big fat attractive juicy css animated candy stripe loading indicator `loadingIndicator` while waiting for the anthropic api to return, with the TITLE being the page title. do not show it until the api call begins, and clear it when it ends.

- the return signature of the anthropic api is curl https://api.anthropic.com/v1/complete\
  -H "x-api-key: $API_KEY"\
  -H 'content-type: application/json'\
  -d '{
    "prompt": "\n\nHuman: Tell me a haiku about trees\n\nAssistant: ",
    "model": "claude-v1", "max_tokens_to_sample": 1000, "stop_sequences": ["\n\nHuman:"]
  }'
{"completion":" Here is a haiku about trees:\n\nSilent sentinels, \nStanding solemn in the woods,\nBranches reaching sky.","stop":"\n\nHuman:","stop_reason":"stop_sequence","truncated":false,"log_id":"f5d95cf326a4ac39ee36a35f434a59d5","model":"claude-v1","exception":null}

- in the string prompt sent to Anthropic, first include the page title and page content, and finally append the prompt, clearly vertically separated by spacing.

- if the Anthropic api call is a 401, handle that by clearing the stored anthropic api key and asking for it again.

- add styles to make sure the popup's styling follows the basic rules of web design, for example having margins around the body, and a system font stack.

- style the popup body with a minimum width of 400 and height of 600.

## debugging notes

inside of background.js, just take the getPageContent response directly

```js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'storePageContent') {
    // dont access request.pageContent
    chrome.storage.local.set({ pageContent: request }, () => {
      sendResponse({ success: true });
    });
  } else if (request.action === 'getPageContent') {
    chrome.storage.local.get(['pageContent'], (result) => {
      // dont access request.pageContent
      sendResponse(result);
    });
  }
  return true;
});
```

inside of popup.js, Update the function calls to `requestAnthropicSummary`
in `popup.js` to pass the `apiKey`:

```javascript
chrome.storage.local.get(['apiKey'], (result) => {
  const apiKey = result.apiKey;
  requestAnthropicSummary(defaultPrompt, apiKey);
});

sendButton.addEventListener('click', () => {
  chrome.storage.local.get(['apiKey'], (result) => {
    const apiKey = result.apiKey;
    requestAnthropicSummary(userPrompt.value, apiKey);
  });
});
```

in `popup.js`, store the defaultPrompt at the top level.
also, give a HTML format to the anthropic prompt
