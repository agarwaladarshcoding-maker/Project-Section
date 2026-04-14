import json
import asyncio
import socket
import logging
import websockets
from websockets.exceptions import ConnectionClosed

from core import classifier
from core import history

logger = logging.getLogger(__name__)

# Module-level tracking
active_port = None
_event_loop = None
clients = {}  # Dictionary to route messages back correctly (tabId -> websocket)

def _find_available_port(start_port=7799, max_attempts=3):
    """Check for open ports in sequence"""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except socket.error:
                continue
    return None

async def send_to_client(tabId: int, message_dict: dict):
    """Returns True if successful, False if the connection was dead or missing"""
    if tabId in clients:
        ws = clients[tabId]
        try:
            await ws.send(json.dumps(message_dict))
            return True
        except ConnectionClosed:
            del clients[tabId] # Cleanup dead connection
    return False

def send_to_client_sync(tab_id: int, message_dict: dict):
    if _event_loop is None:
        logger.error("Event loop not ready")
        return
    asyncio.run_coroutine_threadsafe(
        send_to_client(tab_id, message_dict), _event_loop
    )

async def _client_handler(websocket, callback):
    """Handles an individual WebSocket connection session"""
    current_tab_id = None
    
    try:
        async for message in websocket:
            # 1. Parse JSON gracefully
            try:
                payload = json.loads(message)
            except json.JSONDecodeError:
                logger.error("Failed to parse incoming JSON payload.")
                continue
                
            tab_id = payload.get("tabId")
            
            # Register this websocket so send_to_client can find it
            if tab_id is not None:
                current_tab_id = tab_id
                clients[tab_id] = websocket
                
            text = payload.get("text", "")
            buttons = payload.get("buttons", "")
            ui_context = payload.get("ui_context", "")
            tool = payload.get("tool", "unknown")
            url = payload.get("url", "")
            window_id = payload.get("windowId")
            
            # Disregard empty noisy payloads
            if not text and not buttons and not ui_context:
                continue
            
            # 2. Classify the event
            cls_result = classifier.classify(text, buttons, ui_context)
            event_type = str(cls_result["event_type"]) # cast np.str_ to pure python string
            
            # 3. Log exactly as requested
            event_id = history.log_event(tool, event_type, text, buttons)
            
            # 4. Construct complete result payload
            result_dict = {
                "classification": cls_result,
                "event_id": event_id,
                "tabId": tab_id,
                "windowId": window_id,
                "url": url,
                "tool": tool,
                "original_text": text,
                "buttons": buttons
            }
            
            # 5. Decoupled Thread-safe callback bridging to Thread 2
            if callback:
                callback(result_dict)
                
    except ConnectionClosed:
        pass # Client disconnected gracefully
    except Exception as e:
        logger.exception(f"Unexpected error in WebSocket pipeline: {e}")
    finally:
        # Cleanup routine
        if current_tab_id is not None and current_tab_id in clients:
            del clients[current_tab_id]

async def start_server(callback):
    """
    Boots the local server. Meant to be wrapped inside asyncio.run() from Thread 1.
    """
    global active_port, _event_loop
    _event_loop = asyncio.get_running_loop()
    
    active_port = _find_available_port(7799, 3)
    
    if active_port is None:
        logger.error("Failed to bind port: 7799, 7800, and 7801 are all in use.")
        return
        
    async def _serve_handler(websocket, path=None):
        # We accept path optionally to remain compatible across all versions of the websockets library
        await _client_handler(websocket, callback)
        
    # Start the daemon
    server = await websockets.serve(_serve_handler, "localhost", active_port)
    
    # Run indefinitely
    await asyncio.Future()
