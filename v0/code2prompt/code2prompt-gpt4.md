# Anthropic Claude Summary Extension

A Chrome extension that summarizes web pages using the 
Anthropic Claude API.

## Files

### popup.js

This file contains the main logic for the popup window of the
extension. It listens for the DOMContentLoaded event and 
initializes the following DOM elements:

- `userPrompt`: A textarea for the user to input a prompt.
- `stylePrompt`: A textarea for the user to input a style 
prompt.
- `maxTokens`: An input field for the user to set the maximum
number of tokens for the summary.
- `sendButton`: A button to submit the form and request a 
summary.
- `content`: A div to display the summary.
- `loadingIndicator`: A div to display a loading indicator 
while waiting for the summary.

The `sendButton` has a click event listener that calls the 
`requestAnthropicSummary` function. This function sends a 
message to the background script to get the page content, 
constructs a prompt using the user input and page content, 
and sends a POST request to the Anthropic Claude API. The 
response is then displayed in the `content` div.

### styles.css

This file contains the CSS styles for the popup window. It 
defines styles for the body, textarea, input, button, 
content, and loadingIndicator elements.

### background.js

This file contains the background script for the extension. 
It listens for the following events:

- `chrome.action.onClicked`: Executes the content_script.js 
file on the active tab when the extension icon is clicked.
- `chrome.runtime.onMessage`: Listens for messages with the 
following actions:
  - `storePageContent`: Stores the page title and content in 
the local storage using the tab ID as the key.
  - `getPageContent`: Retrieves the page title and content 
from the local storage using the tab ID and sends it as a 
response.

### popup.html

This file contains the HTML structure for the popup window. 
It includes the following elements:

- A form with labels and inputs for userPrompt, stylePrompt, 
and maxTokens.
- A submit button with the ID "sendButton".
- A div with the ID "content" to display the summary.
- A div with the ID "loadingIndicator" to display a loading 
indicator.

The file also includes a link to the styles.css file and a 
script tag for the popup.js file.

### shared_dependencies.md

This file lists the shared dependencies, variables, DOM 
element IDs, message names, and function names used in the 
extension.

### content_script.js

This file contains a function called `storePageContent` that 
retrieves the page title and content and sends a message to 
the background script with the action "storePageContent" and 
the data as an object containing the title and content.

It also listens for messages with the action 
"storePageContent" and calls the `storePageContent` function 
when received.

### manifest.json

This file contains the manifest for the extension. It 
includes the following properties:

- `manifest_version`: Set to 2.
- `name`: Set to "Anthropic Claude Summary Extension".
- `version`: Set to "1.0".
- `description`: Set to "A Chrome extension that summarizes 
web pages using the Anthropic Claude API."
- `permissions`: Includes "activeTab" and "storage".
- `action`: Defines the default_popup, and default_icon for 
the extension.
- `background`: Includes the background.js script and sets 
the "persistent" property to false.
- `content_scripts`: Includes the content_script.js file and 
matches all URLs.
- `icons`: Defines the icons for the extension.

**Note**: Ensure that all the IDs of the DOM elements and the
data structure of `pageContent` referenced/shared by the 
JavaScript files match up exactly. Use only Chrome Manifest 
V3 APIs. Rename the extension to "code2prompt2code".