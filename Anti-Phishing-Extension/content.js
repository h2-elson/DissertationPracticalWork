// content.js
console.log("Anti-phishing content script loaded");

const currentUrl = window.location.href;

chrome.runtime.sendMessage(
  {
    type: "CHECK_URL",
    url: window.location.href
  },
  (response) => {
    if (response && response.suspicious) {
      showWarningBanner(response.details);
    }
  }
);

function showWarningBanner(details) {
  if (document.getElementById("phishing-warning-banner")) return;

  const currentUrl = window.location.href;

  const banner = document.createElement("div");
  banner.id = "phishing-warning-banner";

  banner.innerHTML = `
    <strong>Security Warning:</strong>
    Suspicious indicators detected:
    <ul>
      ${details.ipBased ? "<li>IP-based URL</li>" : ""}
      ${details.shortUrl ? "<li>Shortened URL</li>" : ""}
      ${details.suspiciousDomain ? "<li>Known suspicious domain</li>" : ""}
    </ul>
    <button id="dismiss-warning">Dismiss</button>
  `;

  banner.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100%;
    background-color: #b71c1c; color: white; padding: 12px;
    font-family: Arial, sans-serif; font-size: 14px;
    z-index: 9999; display: flex; justify-content: space-between;
    align-items: center;
  `;

  banner.querySelector("#dismiss-warning").addEventListener("click", () => {
    // Log user decision
    chrome.runtime.sendMessage({
      type: "LOG_USER_ACTION",
      url: currentUrl,
      action: "DISMISSED_WARNING"
    });

    banner.remove();
  });

  document.body.style.marginTop = "50px";
  document.body.prepend(banner);
}