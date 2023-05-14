chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content_script.js"],
  });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "storePageContent") {
    const tabId = sender.tab.id;
    chrome.storage.local.set({ [tabId]: request.data }, () => {
      sendResponse({ success: true });
    });
    return true;
  } else if (request.action === "getPageContent") {
    const tabId = sender.tab.id;
    chrome.storage.local.get(tabId, (data) => {
      sendResponse(data[tabId]);
    });
    return true;
  }
});