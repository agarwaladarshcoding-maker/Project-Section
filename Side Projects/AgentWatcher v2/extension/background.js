console.log("AgentWatch background.js loaded");
console.log("Attempting WebSocket connection...");

let ws = null;
let currentPortIndex = 0;
const ports = [7799, 7800, 7801];
let reconnectDelay = 1000;
const MAX_RECONNECT_DELAY = 30000;
let pingInterval = null;

function connect() {
    const port = ports[currentPortIndex];
    console.log(`AgentWatch: Attempting to connect to WS on port ${port}...`);
    
    ws = new WebSocket(`ws://localhost:${port}`);

    ws.onopen = () => {
        console.log(`AgentWatch: Successfully connected to Daemon on port ${port}.`);
        reconnectDelay = 1000; // Reset exponential backoff entirely
        currentPortIndex = 0;  // Lock onto this port for future fallback resets
        
        // Ping every 25 seconds to keep the socket fully awake
        if (pingInterval) clearInterval(pingInterval);
        pingInterval = setInterval(() => {
            if (ws && ws.readyState === WebSocket.OPEN) {
                // Lightweight ping signal
                ws.send(JSON.stringify({ type: "ping" }));
            }
        }, 25000);

        // "Re-register all active tabs" conceptually: 
        // Wakes up / forces state sync if needed. But runtime passing events dynamically is best.
        chrome.tabs.query({}, (tabs) => {
            console.log(`AgentWatch: Connected. Tracking ${tabs.length} open tabs.`);
        });
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const action = data.action;
            const tabId = data.tabId;
            const windowId = data.windowId;

            // Handle cross-pipe Focus UI logic directly via Chrome APIs
            if (action === "focus_tab" && tabId && windowId) {
                chrome.windows.update(windowId, { focused: true });
                chrome.tabs.update(tabId, { active: true });
            } 
            // Forward deeper interactions explicitly into the content.js isolation layer
            else if ((action === "inject_reply" || action === "click_button" || action === "retry") && tabId) {
                chrome.tabs.sendMessage(tabId, data);
            }
        } catch (e) {
            console.error("AgentWatch: Failed to parse incoming WebSocket transmission:", e);
        }
    };

    ws.onclose = () => {
        if (pingInterval) clearInterval(pingInterval);

        currentPortIndex++;
        
        // Cycle the 3 defined explicit ports. If exhausted, engage exponential backoff routine.
        if (currentPortIndex >= ports.length) {
            currentPortIndex = 0;
            console.warn(`AgentWatch: Connection dead. All ports exhausted. Backing off for ${reconnectDelay}ms`);
            
            setTimeout(() => {
                connect();
            }, reconnectDelay);
            
            // Increment exponential backoff capped at 30 seconds
            reconnectDelay = Math.min(reconnectDelay * 2, MAX_RECONNECT_DELAY);
        } else {
            // Rapid immediate fallback sequence for alternative ports 7800, 7801
            connect();
        }
    };
    
    ws.onerror = (error) => {
        console.warn("AgentWatch: WebSocket error", error.type);
    };
}

// Boot loop asynchronously
connect();

// Receive stateless events bubbling up from isolated content script worlds
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "AGENT_EVENT") {
        if (ws && ws.readyState === WebSocket.OPEN) {
            // Splice crucial chrome runtime identifiers into standard telemetry object
            const payload = {
                ...message,
                tabId: sender.tab ? sender.tab.id : null,
                windowId: sender.tab ? sender.tab.windowId : null
            };
            ws.send(JSON.stringify(payload));
        }
    }
});
