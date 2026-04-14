// ---------------------------------------------------------
// 1. TOOL IDENTIFICATION & DOM SELECTORS
// ---------------------------------------------------------

const TOOL_SELECTORS = {
    "chat.openai.com": {
        response: "[data-message-author-role='assistant']:last-child, .markdown:last-of-type, [class*='prose']:last-child, main",
        input: "#prompt-textarea",
        stop: "button[aria-label='Stop generating']"
    },
    "claude.ai": {
        response: ".font-claude-message:last-child",
        input: "div[contenteditable='true']",
        stop: "button[aria-label='Stop']" 
    },
    "gemini.google.com": {
        response: "message-content",
        input: "div[role='textbox']",
        stop: "button[aria-label='Stop generating']"
    },
    "www.perplexity.ai": {
        response: "main",
        input: "textarea",
        stop: "button[aria-label='Stop']" 
    },
    "grok.x.ai": {
        response: "main",
        input: "textarea",
        stop: "button[aria-label='Stop']"
    },
    "chat.mistral.ai": {
        response: "main",
        input: "textarea",
        stop: "button[aria-label='Stop']"
    },
    "antigravity.ai": {
        response: "#conversation-container, main",
        input: "textarea, #chat-input",
        stop: "button[aria-label='Stop']"
    },
    "cline.bot": {
        response: "main",
        input: "textarea",
        stop: "button[aria-label='Stop']"
    },
    "github.com": { // Copilot domains
        response: ".copilot-chat-container",
        input: "textarea",
        stop: ".stop-generating-button"
    },
    "cursor.sh": {
        response: ".cursor-pane",
        input: "textarea",
        stop: ".stop-generating"
    }
};

let currentTool = "unknown";
let selectors = null;

// Determine if we are tracking this URL
for (const [key, value] of Object.entries(TOOL_SELECTORS)) {
    if (window.location.hostname.includes(key)) {
        currentTool = key;
        selectors = value;
        break;
    }
}

console.log("AgentWatch content.js loaded on:", window.location.hostname);
console.log("AgentWatch using tool:", currentTool);
console.log("AgentWatch selectors:", JSON.stringify(selectors));

// ---------------------------------------------------------
// 2. NETWORK INTERCEPTION & DOM FALLBACK PIPELINE
// ---------------------------------------------------------

// Inject main-world script to intercept page's fetch
function injectMainWorldScript() {
    const script = document.createElement('script');
    script.src = chrome.runtime.getURL('injected.js');
    script.onload = function() { this.remove(); };
    (document.head || document.documentElement).appendChild(script);
}
injectMainWorldScript();

// ── Deduplication state ──────────────────────────
let lastSentHash = "";
let lastSentTime = 0;
const MIN_SEND_INTERVAL_MS = 8000;
let lastNetworkEventTime = 0;

function simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash) + str.charCodeAt(i);
        hash |= 0;
    }
    return hash.toString();
}

function extractUIContext() {
    const h1 = document.querySelector('h1');
    if (h1 && h1.innerText.trim()) return h1.innerText.trim();
    return document.title;
}

function sendToCore(text) {
    if (!text || text.length < 20) return;
    const hash = simpleHash(text.slice(-500));
    const now = Date.now();
    if (hash === lastSentHash) return;
    if (now - lastSentTime < MIN_SEND_INTERVAL_MS) return;
    lastSentHash = hash;
    lastSentTime = now;
    lastNetworkEventTime = now;

    const buttonLabels = Array.from(document.querySelectorAll("button"))
        .map(b => (b.innerText.trim() || 
                   b.getAttribute("aria-label") || "").trim())
        .filter(l => l.length > 0 && l.length < 35);

    chrome.runtime.sendMessage({
        type: "AGENT_EVENT",
        text: text.slice(-1000),
        buttons: [...new Set(buttonLabels)].join(","),
        ui_context: extractUIContext(),
        url: window.location.href,
        tool: currentTool
    });
    console.log("AgentWatch: sent payload, type will be classified by daemon");
}

window.addEventListener("message", (event) => {
    if (event.source !== window) return;
    if (!event.data || event.data.source !== "agentwatch-injected") return;
    
    const text = event.data.text;
    if (!text || text.length < 20) return;
    
    const hash = simpleHash(text.slice(-500));
    const now = Date.now();
    if (hash === lastSentHash) return;
    if (now - lastSentTime < MIN_SEND_INTERVAL_MS) return;
    lastSentHash = hash;
    lastSentTime = now;
    lastNetworkEventTime = now;
    
    const buttonLabels = Array.from(document.querySelectorAll("button"))
        .map(b => (b.innerText.trim() || 
                   b.getAttribute("aria-label") || "").trim())
        .filter(l => l.length > 0 && l.length < 35);

    chrome.runtime.sendMessage({
        type: "AGENT_EVENT",
        text: text,
        buttons: [...new Set(buttonLabels)].join(","),
        ui_context: event.data.title || document.title,
        url: event.data.url || window.location.href,
        tool: currentTool
    });
    console.log("AgentWatch: forwarded intercepted payload to daemon");
});

// ── MutationObserver FALLBACK ────────────────────
// Only fires for tools where network interception
// catches nothing (e.g. tools using WebSocket internally)
// Will not fire if a network event occurred in last 30s

let debounceTimer = null;

function domFallbackEvaluate() {
    if (Date.now() - lastNetworkEventTime < 30000) return;
    if (!selectors) return;

    let container = null;
    const sels = selectors.response.split(',');
    for (const s of sels) {
        container = document.querySelector(s.trim());
        if (container) break;
    }
    if (!container) container = document.body;
    const text = (container.innerText || '').slice(-1000);
    sendToCore(text);
}

if (selectors) {
    const observer = new MutationObserver(() => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(domFallbackEvaluate, 5000);
    });
    observer.observe(document.body, {
        childList: true, subtree: true, characterData: true
    });
}

// ---------------------------------------------------------
// 3. RECIEVE INJECT & CLICK ACTIONS
// ---------------------------------------------------------

function setNativeValue(element, value) {
    if (element.isContentEditable) {
        element.focus();
        document.execCommand('selectAll', false, null);
        document.execCommand('insertText', false, value);
        element.dispatchEvent(new Event('input', { bubbles: true }));
        return;
    }

    // Direct value setter (React/Vue/Svelte ignores primitive dom assignment)
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, "value"
    ) || Object.getOwnPropertyDescriptor(
        window.HTMLTextAreaElement.prototype, "value"
    );
    
    if (nativeInputValueSetter && nativeInputValueSetter.set) {
        nativeInputValueSetter.set.call(element, value);
    } else {
        element.value = value;
    }
    
    // Bubble native event hierarchy to force framework reconcilers to re-render
    element.dispatchEvent(new Event('input', { bubbles: true }));
    element.dispatchEvent(new Event('change', { bubbles: true }));
}

function simulateSubmit(element) {
    element.dispatchEvent(new KeyboardEvent('keydown', {
        key: 'Enter', code: 'Enter', keyCode: 13,
        bubbles: true, cancelable: true
    }));
    setTimeout(() => {
        const sendBtn = document.querySelector(
            'button[aria-label="Send message"], ' +
            'button[data-testid="send-button"], ' +
            'button[aria-label="Send"], ' +
            'button[type="submit"]'
        );
        if (sendBtn && !sendBtn.disabled) sendBtn.click();
    }, 100);
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "inject_reply") {
        if (!selectors) return false;
        
        const inputSelectors = selectors.input.split(',');
        let inputEl = null;
        for (const sel of inputSelectors) {
            inputEl = document.querySelector(sel.trim());
            if (inputEl) break;
        }
        
        if (inputEl) {
            setNativeValue(inputEl, msg.text);
            simulateSubmit(inputEl);
        }
    } 
    else if (msg.action === "click_button") {
        const btns = document.querySelectorAll("button");
        const targetLabel = msg.label.toLowerCase();
        
        for (const b of btns) {
            const label = (b.innerText.trim() || b.getAttribute("aria-label") || "").toLowerCase();
            if (label.includes(targetLabel) && b.checkVisibility && b.checkVisibility()) {
                b.click();
                break;
            }
        }
    }
    return false;
});
