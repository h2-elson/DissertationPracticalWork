// rules.js

// Check if a URL contains an IP address instead of a domain name
function isIpBasedUrl(url) {
  const ipRegex =
    /https?:\/\/(\d{1,3}\.){3}\d{1,3}/;
  return ipRegex.test(url);
}
