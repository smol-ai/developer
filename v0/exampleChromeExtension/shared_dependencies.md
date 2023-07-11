the app is: a Chrome Manifest V3 extension that reads the current page, and offers a popup UI that sends the page content to the Anthropic Claude API along with a prompt to summarize it, and lets the user modify that prompt and re-send the prompt+content to get another summary view of the content.

the files we have decided to generate are: content_script.js, background.js, popup.html, popup.js, popup.css

Shared dependencies:

1. Exported variables:
   - pageTitle
   - pageContent

2. Data schemas:
   - storePageContent action data: { action: 'storePageContent', pageTitle, pageContent }
   - getPageContent action data: { action: 'getPageContent' }

3. ID names of DOM elements:
   - content
   - userPrompt
   - sendButton
   - loadingIndicator

4. Message names:
   - storePageContent
   - getPageContent

5. Function names:
   - requestAnthropicSummary

6. API endpoints:
   - https://api.anthropic.com/v1/complete

7. Model name:
   - claude-instant-v1-100k

8. Default prompt:
   - defaultPrompt