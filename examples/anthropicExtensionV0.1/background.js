chrome.runtime.onInstalled.addListener(() => {
  chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content_script.js'],
    });
  });
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'storePageContent') {
    chrome.storage.local.set({ pageContent: request }, () => {
      sendResponse({ success: true });
    });
  } else if (request.action === 'getPageContent') {
    chrome.storage.local.get(['pageContent'], (result) => {
      sendResponse(result);
    });
  }
  return true;
});