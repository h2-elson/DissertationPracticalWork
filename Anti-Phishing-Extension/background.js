// background.js

function isIpBasedUrl(url) {
  const ipRegex = /https?:\/\/(\d{1,3}\.){3}\d{1,3}/;
  return ipRegex.test(url);
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "CHECK_URL") {
    const url = message.url;
    const ipDetected = isIpBasedUrl(url);

    console.log("Checked URL:", url);
    console.log("IP-based URL detected:", ipDetected);

    sendResponse({ suspicious: ipDetected });
  }

  // REQUIRED for async message handling in MV3
  return true;
});
