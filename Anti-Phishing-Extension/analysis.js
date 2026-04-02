// analysis.js

// Check if URL uses IP instead of domain
export function isIpBasedUrl(url) {
  const ipRegex = /https?:\/\/(\d{1,3}\.){3}\d{1,3}/;
  return ipRegex.test(url);
}

// Check if URL is a shortened link
export function isShortenedUrl(url) {
  const shorteners = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co",
    "ow.ly",
    "is.gd"
  ];
  return shorteners.some(domain => url.includes(domain));
}

// Check if domain is in local reputation list
export function isSuspiciousDomain(url, reputationList) {
  try {
    const domain = new URL(url).hostname;
    return reputationList.includes(domain);
  } catch {
    return false;
  }
}

// Main analysis function
export function analyzeUrl(url, reputationList) {
  return {
    ipBased: isIpBasedUrl(url),
    shortUrl: isShortenedUrl(url),
    suspiciousDomain: isSuspiciousDomain(url, reputationList)
  };
}