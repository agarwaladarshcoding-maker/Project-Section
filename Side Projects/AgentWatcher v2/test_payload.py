import asyncio
import json
import websockets

async def test():
    uri = "ws://localhost:7799"
    async with websockets.connect(uri) as ws:
        
        payloads = [
            {
                "text": "I need to execute a command to delete the auth module. Proceed?",
                "buttons": "Allow,Deny",
                "ui_context": "Permission Request",
                "url": "https://chat.openai.com/test",
                "tabId": 101,
                "windowId": 201,
                "tool": "chatgpt"
            },
            {
                "text": "Unhandled exception in payment gateway: Connection refused.",
                "buttons": "View Logs,Retry",
                "ui_context": "Critical Error",
                "url": "https://claude.ai/test",
                "tabId": 102,
                "windowId": 202,
                "tool": "claude"
            },
            {
                "text": "Successfully deployed the login component to production.",
                "buttons": "Follow Up,Show,Dismiss",
                "ui_context": "Task Complete",
                "url": "https://app.antigravity.ai/test",
                "tabId": 103,
                "windowId": 203,
                "tool": "antigravity"
            }
        ]
        
        for p in payloads:
            print(f"Sending: {p['tool']} — {p['text'][:50]}")
            await ws.send(json.dumps(p))
            await asyncio.sleep(0.5)
        
        print("All payloads sent.")

asyncio.run(test())
