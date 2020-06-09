chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
    chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [
            new chrome.declarativeContent.PageStateMatcher({
                pageUrl: { hostContains: '.ro' },
            }),
            new chrome.declarativeContent.PageStateMatcher({
                pageUrl: { hostContains: '.com' },
            }),
            new chrome.declarativeContent.PageStateMatcher({
                pageUrl: { urlContains : 'localhost:10080' },
            })
        ],
        actions: [new chrome.declarativeContent.ShowPageAction()]
    }]);
});