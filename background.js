async function loadTrackers() {
    const res = await fetch(chrome.runtime.getURL("trackers.json"));
    const data = await res.json();
    return data.trackers;
}

async function blockTrackers() {
    const trackers = await loadTrackers();

    const rules = trackers.map((domain, index) => ({
        id: index + 1,
        priority: 1,
        action: { type: "block" },
        condition: {
            urlFilter: domain,
            resourceTypes: ["script", "xmlhttprequest"]
        }
    }));

    chrome.declarativeNetRequest.updateDynamicRules({
        removeRuleIds: rules.map(r => r.id),
        addRules: rules
    });
}

blockTrackers();