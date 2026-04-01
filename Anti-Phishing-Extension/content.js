// content.js
console.log("Anti-phishing content script loaded");

const currentUrl = window.location.href;

chrome.runtime.sendMessage(
  {
    type: "CHECK_URL",
    url: currentUrl
  },
  (response) => {
    if (response && response.suspicious) {
      showWarningBanner();
    }
  }
);

function showWarningBanner() {
  // Prevent duplicate banners
  if (document.getElementById("phishing-warning-banner")) {
    return;
  }

  // Create banner container
  const banner = document.createElement("div");
  banner.id = "phishing-warning-banner";

  // Banner content
  banner.innerHTML = `
    <strong>Security Warning:</strong>
    This website uses an IP-based URL, which is a common phishing indicator.
    <button id="dismiss-warning">Dismiss</button>
  `;

  // Banner styling
  banner.style.position = "fixed";
  banner.style.top = "0";
  banner.style.left = "0";
  banner.style.width = "100%";
  banner.style.backgroundColor = "#b71c1c";
  banner.style.color = "white";
  banner.style.padding = "12px";
  banner.style.fontFamily = "Arial, sans-serif";
  banner.style.fontSize = "14px";
  banner.style.zIndex = "9999";
  banner.style.display = "flex";
  banner.style.justifyContent = "space-between";
  banner.style.alignItems = "center";

  // Button styling
  const buttonStyle = `
    background: white;
    color: #b71c1c;
    border: none;
    padding: 6px 10px;
    cursor: pointer;
    font-weight: bold;
  `;

  banner.querySelector("button").style.cssText = buttonStyle;

  // Dismiss button logic
  banner.querySelector("#dismiss-warning").addEventListener("click", () => {
    banner.remove();
  });

  // Push page content down so it’s not hidden
  document.body.style.marginTop = "50px";

  // Add banner to page
  document.body.prepend(banner);
}
