a Chrome Manifest V3 extension that reads the current page, and offers a popup UI that has the page title+content and a textarea for a prompt (with a default value we specify). When the user hits submit, it sends the page title+content to the Anthropic Claude API along with the up to date prompt to summarize it. The user can modify that prompt and re-send the prompt+content to get another summary view of the content.

- Only when clicked:
  - it injects a content script `content_script.js` on the currently open tab, and accesses the title `pageTitle` and main content (innerText) `pageContent` of the currently open page 
  (extracted via an injected content script, and sent over using a `storePageContent` action) 
  - in the background, receives the `storePageContent` data and stores it
  - only once the new page content is stored, then it pops up a full height window with a minimalistic styled html popup
  - in the popup script
    - the popup should display a 10px tall rounded css animated red and white candy stripe loading indicator `loadingIndicator`, while waiting for the anthropic api to return
      - with the currently fetching page title and a running timer in the center showing time elapsed since call started
      - do not show it until the api call begins, and hide it when it ends.
    - retrieves the page content data using a `getPageContent` action (and the background listens for the `getPageContent` action and retrieves that data) and displays the title at the top of the popup
    - check extension storage for an `apiKey`, and if it isn't stored, asks for an API key to Anthropic Claude and stores it.
    - at the bottom of the popup, show a vertically resizable form that has:
      - a 2 line textarea with an id and label of `userPrompt`
        - `userPrompt` has a default value of
            ```js
            defaultPrompt = `Please provide a detailed, easy to read HTML summary of the given content`;
            ```js
      - a 4 line textarea with an id and label of `stylePrompt`
        - `stylePrompt` has a default value of
            ```js
            defaultStyle = `Respond with 3-4 highlights per section with important keywords, people, numbers, and facts bolded in this HTML format:
            
            <h1>{title here}</h1>
            <h3>{section title here}</h3>
            <details>
              <summary>{summary of the section with <strong>important keywords, people, numbers, and facts bolded</strong> and key quotes repeated}</summary>
              <ul>
                <li><strong>{first point}</strong>: {short explanation with <strong>important keywords, people, numbers, and facts bolded</strong>}</li>
                <li><strong>{second point}</strong>: {same as above}</li>
                <li><strong>{third point}</strong>: {same as above}</li>
                <!-- a fourth point if warranted -->
              </ul>
            </details>
            <h3>{second section here}</h3>
            <p>{summary of the section with <strong>important keywords, people, numbers, and facts bolded</strong> and key quotes repeated}</p>
            <details>
              <summary>{summary of the section with <strong>important keywords, people, numbers, and facts bolded</strong> and key quotes repeated}</summary>
              <ul>
                <!-- as many points as warranted in the same format as above -->
              </ul>
            </details>
            <h3>{third section here}</h3>
            <!-- and so on, as many sections and details/summary subpoints as warranted -->

            With all the words in brackets replaced by the summary of the content. sanitize non visual HTML tags with HTML entities, so <template> becomes &lt;template&gt; but <strong> stays the same. Only draw from the source content, do not hallucinate. Finally, end with other questions that the user might want answered based on this source content:

            <hr>
            <h2>Next prompts</h2>
            <ul>
              <li>{question 1}</li>
              <li>{question 2}</li>
              <li>{question 3}</li>
            </ul>`;
            ```js
      - and in the last row, on either side,
        - and a nicely styled submit button with an id of `sendButton` (tactile styling that "depresses" on click)
      - only when `sendButton` is clicked, calls the Anthropic model endpoint https://api.anthropic.com/v1/complete with: 
        - append the page title
        - append the page content
        - add the prompt which is a concatenation of
            ```js
            finalPrompt = `Human: ${userPrompt} \n\n ${stylePrompt} \n\n Assistant:`
            ```
        - and use the `claude-instant-v1` model (if `pageContent` is <70k words) or the `claude-instant-v1-100k` model (if more) 
        - requesting max tokens = the higher of (25% of the length of the page content, or 750 words)
        - if another submit event is hit while the previous api call is still inflight, cancel that and start the new one
    - renders the Anthropic-generated result at the top of the popup in a div with an id of `content`

Important Details:

- It has to run in a browser environment, so no Nodejs APIs allowed.

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

- style the popup body with <link rel="stylesheet" href="https://unpkg.com/mvp.css@1.12/mvp.css"> but insist on body margins of 16 and a minimum width of 400 and height of 600.

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
