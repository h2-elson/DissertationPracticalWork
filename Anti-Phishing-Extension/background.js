// background.js

function isIpBasedUrl(url) {
  const ipRegex = /https?:\/\/(\d{1,3}\.){3}\d{1,3}/;
  return ipRegex.test(url);
}

import { analyzeUrl } from "./analysis.js";
import { LOCAL_REPUTATION_LIST } from "./reputation.js";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // URL check request
  if (message.type === "CHECK_URL") {
    const url = message.url;
    const result = analyzeUrl(url, LOCAL_REPUTATION_LIST);

    const suspicious =
      result.ipBased || result.shortUrl || result.suspiciousDomain;

    logDetectionEvent(url, result, suspicious);

    sendResponse({ suspicious, details: result });
  }

  // User decision logging
  if (message.type === "LOG_USER_ACTION") {
    logUserAction(message.url, message.action);
  }

  return true;
});

// --- Logging functions ---

async function logDetectionEvent(url, analysis, flagged) {
  const { phishingLogs = [] } = await chrome.storage.local.get("phishingLogs");

  phishingLogs.push({
    timestamp: new Date().toISOString(),
    type: "DETECTION",
    url,
    analysis,
    flagged
  });

  await chrome.storage.local.set({ phishingLogs });
}

async function logUserAction(url, action) {
  const { phishingLogs = [] } = await chrome.storage.local.get("phishingLogs");

  phishingLogs.push({
    timestamp: new Date().toISOString(),
    type: "USER_ACTION",
    url,
    action
  });

  await chrome.storage.local.set({ phishingLogs });
}