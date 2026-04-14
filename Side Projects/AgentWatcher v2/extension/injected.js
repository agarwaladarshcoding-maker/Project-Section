(function() {
    // Prevent double injection
    if (window.__agentWatchInjected) return;
    window.__agentWatchInjected = true;

    console.log("AgentWatch injected.js running in main world");

    const AI_PATTERNS = [
        'backend-api/conversation',
        'backend-api',
        '/api/append_message',
        '/api/generate',
        'completions',
        '/api/chat',
        '/chat/completions',
        'streamGenerateContent',
        'generateContent',
        'claude.ai/api',
    ];

    function isAIUrl(url) {
        if (!url) return false;
        return AI_PATTERNS.some(p => url.includes(p));
    }

    function parseSSE(rawText) {
        let fullText = '';
        for (const line of rawText.split('\n')) {
            if (!line.startsWith('data: ')) continue;
            if (line.includes('[DONE]')) continue;
            try {
                const j = JSON.parse(line.slice(6));
                const delta = j?.choices?.[0]?.delta?.content;
                if (delta) { fullText += delta; continue; }
                const claudeDelta = j?.delta?.text;
                if (claudeDelta) { fullText += claudeDelta; continue; }
                const gemini = j?.candidates?.[0]?.content?.parts?.[0]?.text;
                if (gemini) { fullText += gemini; continue; }
                const generic = j?.completion || j?.text || j?.content;
                if (generic) fullText += generic;
            } catch(e) {}
        }
        return fullText.trim();
    }

    function sendToContentScript(text) {
        if (!text || text.length < 20) return;
        window.postMessage({
            source: "agentwatch-injected",
            text: text.slice(-1000),
            url: window.location.href,
            title: document.title
        }, "*");
    }

    // Override fetch in PAGE context
    const _origFetch = window.fetch;
    window.fetch = async function(...args) {
        const url = typeof args[0] === 'string' ? args[0] :
                    (args[0]?.url || '');
        
        const response = await _origFetch.apply(this, args);
        
        if (isAIUrl(url)) {
            console.log("AgentWatch: intercepted", url.substring(0, 80));
            const clone = response.clone();
            clone.text().then(raw => {
                const parsed = parseSSE(raw);
                sendToContentScript(parsed || raw);
            }).catch(() => {});
        }
        
        return response;
    };

    // Override XHR in PAGE context
    const _origOpen = XMLHttpRequest.prototype.open;
    const _origSend = XMLHttpRequest.prototype.send;

    XMLHttpRequest.prototype.open = function(m, url, ...r) {
        this._awUrl = url;
        return _origOpen.apply(this, [m, url, ...r]);
    };
    XMLHttpRequest.prototype.send = function(...args) {
        this.addEventListener('load', function() {
            if (isAIUrl(this._awUrl)) {
                const parsed = parseSSE(this.responseText);
                sendToContentScript(parsed || this.responseText);
            }
        });
        return _origSend.apply(this, args);
    };

})();
