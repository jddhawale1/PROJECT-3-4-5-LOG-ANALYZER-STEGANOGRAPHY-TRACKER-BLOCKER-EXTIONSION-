chrome.action.getBadgeText({}, (text) => {
    document.getElementById("count").innerText =
        "Blocked: " + (text || 0);
});