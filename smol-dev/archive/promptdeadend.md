a Chrome Manifest V3 extension that reads the current page, and offers a popup UI that sends the page content to the Anthropic Claude API along with a prompt to summarize it, and lets the user modify that prompt and re-send the prompt+content to get another summary view of the content.

When clicked:
- pops up a small window with a simple, modern, slick, minimalistic styled html popup
  - checks its own storage for an `apiKey`, and if it isn't stored, asks for an API key to Anthropic Claude and stores it.
  - which accesses the title and main content of the currently open page (extracted via an injected content script, and sent over using a 'pageContent' action) and renders it inside a <details> tag with a "Full article" <summary> at the top (tastefully styled).
  - from the popup script, calls the Anthropic model endpoint https://api.anthropic.com/v1/complete with the `claude-instant-v1` model with the page content, prompting it to ask for a detailed, bullet pointed, easy to read HTML summary of the given content with important keywords bolded and important images and links preserved.
  - renders the Anthropic-generated HTML summary inside of the popup in a div with an id of content
  - at the bottom of the popup, show a textbox with an id of `userPrompt` a default value of the same prompt that we used, and a submit button with an id of `sendButton` that lets the user re-ask Anthropic with the same content but different prompt. disable these inputs while it waits.

Important Details:

- It has to run in a browser environment, so no Nodejs APIs allowed.

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

- style the popup body with a minimum width of 400 and height of 600.

## bugs we have solved

In the `background.js` file, make sure that the message listener is forwarding the response from the content script to the `popup.js` file. You can do this by adding 
a callback function to the `chrome.tabs.sendMessage` method.

Second, the `chrome.tabs.query` function is used to get the active tab in the current window. However, the `tab` object returned
by this function might be undefined in some cases, causing the error.

To fix this issue, you can add a check to ensure that the `tab` object is defined before accessing its 'id' property. Here's the updated code for 
the background.js file:

```javascript
chrome.runtime.onInstalled.addListener(() => {
  chrome.action.onClicked.addListener((tab) => {
    if (tab) { // Add this check to ensure the tab object is defined
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["content_script.js"],
      });
    }
  });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "pageContent") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0]) { // Add this check to ensure the tabs object and the first tab are defined
        chrome.tabs.sendMessage(tabs[0].id, request, (response) => {
          sendResponse(response);
        });
      }
    });
    return true; // This is necessary to keep the message channel open for the asynchronous response
  }
});
```

 In `content_script.js`, wrap the `chrome.runtime.sendMessage`call inside a `setTimeout` function to add a delay before sending the message. This will give the background script enough time to set up the listener.

```javascript
function getPageContent() {
  // ...
}

setTimeout(() => {
  chrome.runtime.sendMessage({ action: "pageContent", ...getPageContent() });
}, 1000);
```