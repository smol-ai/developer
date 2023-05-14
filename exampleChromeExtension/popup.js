document.addEventListener('DOMContentLoaded', () => {
  const content = document.getElementById('content');
  const userPrompt = document.getElementById('userPrompt');
  const sendButton = document.getElementById('sendButton');
  const loadingIndicator = document.getElementById('loadingIndicator');

  const defaultPrompt = `Human: Please provide a detailed, easy to read HTML summary of the given content with 3-4 highlights per section with important keywords bolded and important links preserved, in this format:

  <h1>{title here}</h1>
  <h2>{section title here}</h2>
  <ul>
    <li><strong>{first point}</strong>: {short explanation with details, and important links}</li>
    <li><strong>{second point}</strong>: {short explanation with details, and important links}</li>
    <!-- etc -->
  </ul>
  <h2>{second section here}</h2>
  <ul>
    <!-- etc -->
  </ul>
  <!-- etc -->

  With all the words in brackets replaced by the summary of the content.

  Assistant:`;

  function requestAnthropicSummary(prompt, apiKey) {
    chrome.runtime.sendMessage({ action: 'getPageContent' }, (response) => {
      const { pageTitle, pageContent } = response.pageContent;
      const fullPrompt = `${pageTitle}\n\n${pageContent}\n\n${prompt}`;

      loadingIndicator.innerHTML = `Read page content of ${pageTitle}`;
      loadingIndicator.style.display = 'block';
      content.innerHTML = '';
      userPrompt.disabled = true;
      sendButton.disabled = true;

      fetch('https://api.anthropic.com/v1/complete', {
        method: 'POST',
        headers: {
          'x-api-key': apiKey,
          'content-type': 'application/json',
        },
        body: JSON.stringify({
          prompt: fullPrompt,
          model: 'claude-instant-v1-100k',
          max_tokens_to_sample: 1000,
          stop_sequences: ['\n\nHuman:'],
        }),
      })
        .then((res) => {
          if (res.status === 401) {
            chrome.storage.local.remove(['apiKey']);
            throw new Error('Invalid API key');
          }
          return res.json();
        })
        .then((data) => {
          content.innerHTML = data.completion;
          loadingIndicator.style.display = 'none';
          userPrompt.disabled = false;
          sendButton.disabled = false;
        })
        .catch((error) => {
          console.error(error);
          loadingIndicator.style.display = 'none';
          userPrompt.disabled = false;
          sendButton.disabled = false;
        });
    });
  }

  chrome.storage.local.get(['apiKey'], (result) => {
    if (!result.apiKey) {
      const apiKey = prompt('Please enter your Anthropic Claude API key:');
      chrome.storage.local.set({ apiKey }, () => {
        requestAnthropicSummary(defaultPrompt, apiKey);
      });
    } else {
      requestAnthropicSummary(defaultPrompt, result.apiKey);
    }
  });

  sendButton.addEventListener('click', () => {
    chrome.storage.local.get(['apiKey'], (result) => {
      requestAnthropicSummary(userPrompt.value, result.apiKey);
    });
  });
});