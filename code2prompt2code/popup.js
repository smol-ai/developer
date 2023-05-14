document.addEventListener("DOMContentLoaded", () => {
  const userPrompt = document.getElementById("userPrompt");
  const stylePrompt = document.getElementById("stylePrompt");
  const maxTokens = document.getElementById("maxTokens");
  const sendButton = document.getElementById("sendButton");
  const content = document.getElementById("content");
  const loadingIndicator = document.getElementById("loadingIndicator");

  sendButton.addEventListener("click", requestAnthropicSummary);

  async function requestAnthropicSummary() {
    loadingIndicator.style.display = "block";
    content.innerHTML = "";

    const tab = await new Promise(resolve => chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => resolve(tab)));
    chrome.runtime.sendMessage({ action: "getPageContent", tabId: tab.id }, async (pageContent) => {
      const prompt = `${userPrompt.value}\n\n${pageContent.title}\n\n${pageContent.content}`;
      const style = stylePrompt.value;
      const tokens = parseInt(maxTokens.value, 10);

      const response = await fetch("https://api.anthropic.com/claude", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt, style, tokens })
      });

      const summary = await response.json();
      content.innerHTML = summary;
      loadingIndicator.style.display = "none";
    });
  }
});