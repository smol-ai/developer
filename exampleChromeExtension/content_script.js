function extractPageContent() {
  const pageTitle = document.title;
  const pageContent = document.body.innerText;
  return { pageTitle, pageContent };
}

function sendMessageToBackground(action, data) {
  chrome.runtime.sendMessage({ action, ...data }, (response) => {
    if (response.success) {
      console.log('Page content sent to background.');
    } else {
      console.error('Failed to send page content to background.');
    }
  });
}

const pageData = extractPageContent();
sendMessageToBackground('storePageContent', pageData);