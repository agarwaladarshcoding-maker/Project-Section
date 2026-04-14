import threading
import time
import signal
import sys
import logging
import asyncio

_shutdown_event = threading.Event()

from core import websocket_server
from core import popup_router
from notifiers import notify_mac

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

def on_event_received(result_dict):
    """
    Callback — bridge from Thread 1 to Thread 2
    """
    event_type = result_dict["classification"]["event_type"]
    confidence = result_dict["classification"]["confidence"]
    tool = result_dict["tool"]
    preview = result_dict["classification"]["truncated_preview"]
    fallback = result_dict["classification"]["used_fallback"]
    
    print(f"\n{'='*50}")
    print(f"EVENT RECEIVED")
    print(f"  Tool:       {tool}")
    print(f"  Type:       {event_type}")
    print(f"  Confidence: {confidence:.2%}")
    print(f"  Fallback:   {fallback}")
    print(f"  Preview:    {preview}")
    print(f"  Event ID:   {result_dict['event_id']}")
    print(f"{'='*50}\n")
    
    popup_router.route(result_dict)

def run_server():
    """
    Thread 1 — background daemon thread processing WebSocket lifecycle
    """
    asyncio.run(websocket_server.start_server(on_event_received))

def shutdown(signum, frame):
    print("\nShutting down AgentWatch...")
    _shutdown_event.set()
    from PyObjCTools import AppHelper
    AppHelper.stopEventLoop()

def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    
    # Startup banner
    print("╔══════════════════════════════╗")
    print("║      AgentWatch v1.0         ║")  
    print("║  Universal Agent Notifier    ║")
    print("╚══════════════════════════════╝")
    print("Classifier loaded")
    print("History DB ready")
    print("Starting WebSocket server...")
    
    notify_mac.setup_notifications()
    
    # Small delay then check permission status
    def _check_perms():
        import time
        time.sleep(1.5)
        def _report(authorized):
            if authorized:
                print("Notification permission: GRANTED ✓")
            else:
                print("WARNING: Notification permission DENIED")
                print("Go to System Settings → Notifications → Terminal → Allow")
        notify_mac.check_notification_permission(_report)
    threading.Thread(target=_check_perms, daemon=True).start()
    
    # Fire off Thread 1 daemon
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    
    # Thread 2 - Wait for Thread 1 bind
    time.sleep(1)
    
    active_port = websocket_server.active_port
    if active_port:
        print(f"WebSocket server running on port {active_port}")
    else:
        logger.error("Failed to start WebSocket server - no available ports.")
        sys.exit(1)
        
    print("Waiting for agent events...")
        
    # Thread 2 - Main placeholder blocking loop
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()

if __name__ == "__main__":
    main()
