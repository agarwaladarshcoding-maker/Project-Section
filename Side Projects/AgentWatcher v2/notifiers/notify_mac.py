import os
import json
import logging
import threading
from Foundation import NSObject
from UserNotifications import (
    UNUserNotificationCenter,
    UNAuthorizationOptionAlert,
    UNAuthorizationOptionSound,
    UNAuthorizationOptionBadge,
    UNNotificationRequest,
    UNMutableNotificationContent,
    UNNotificationAction,
    UNTextInputNotificationAction,
    UNNotificationCategory,
    UNTimeIntervalNotificationTrigger,
    UNNotificationActionOptionForeground
)

from core import history
from core import websocket_server

logger = logging.getLogger(__name__)

# CRITICAL RULE 2: Module-level strong reference to delegate
_notification_delegate = None

class AgentNotificationDelegate(NSObject):
    def userNotificationCenter_didReceiveNotificationResponse_withCompletionHandler_(self, center, response, completionHandler):
        try:
            # Parse userInfo to get metadata
            user_info = response.notification().request().content().userInfo()
            event_id = user_info.get("event_id")
            tab_id = user_info.get("tab_id")
            window_id = user_info.get("window_id")
            
            action_identifier = str(response.actionIdentifier())
            
            reply_text = None
            if hasattr(response, "userText") and response.userText():
                reply_text = str(response.userText())
            
            # Action identifiers are the button labels
            button_label = action_identifier
            
            if event_id is not None:
                history.mark_resolved(event_id, button_label)
                
            if button_label in ["Show", "View Logs", "View"]:
                if tab_id and window_id:
                    websocket_server.send_to_client_sync(
                        tab_id, 
                        {"action": "focus_tab", "tabId": tab_id, "windowId": window_id}
                    )
            elif button_label == "Reply" and reply_text:
                if tab_id:
                    websocket_server.send_to_client_sync(
                        tab_id,
                        {"action": "inject_reply", "text": reply_text, "tabId": tab_id}
                    )
            elif button_label == "Retry":
                if tab_id:
                    websocket_server.send_to_client_sync(
                        tab_id,
                        {"action": "retry", "tabId": tab_id}
                    )
                    
        except Exception as e:
            logger.exception("Error handling notification response: %s", e)
        finally:
            try:
                if completionHandler:
                    completionHandler()
            except Exception as e:
                logger.error("completionHandler error: %s", e)

def _create_category(identifier, action_labels, is_reply=False):
    ns_actions = []
    for label in action_labels:
        if is_reply and label == "Reply":
            action = UNTextInputNotificationAction.actionWithIdentifier_title_options_textInputButtonTitle_textInputPlaceholder_(
                label, label, UNNotificationActionOptionForeground, "Send", "Type reply..."
            )
        else:
            opts = 0
            if label in ["Show", "View Logs", "View"]:
                 opts = UNNotificationActionOptionForeground
            action = UNNotificationAction.actionWithIdentifier_title_options_(
                label, label, opts
            )
        ns_actions.append(action)
        
    return UNNotificationCategory.categoryWithIdentifier_actions_intentIdentifiers_options_(
        identifier, ns_actions, [], 0
    )

def setup_notifications():
    """
    Called once at startup from the main thread.
    Requests permissions, registers the delegate, and pre-registers all categories.
    """
    global _notification_delegate
    
    center = UNUserNotificationCenter.currentNotificationCenter()
    
    # Needs to be a module-level strong reference
    if _notification_delegate is None:
        _notification_delegate = AgentNotificationDelegate.alloc().init()
    
    center.setDelegate_(_notification_delegate)
    
    # ---------------------------------------------------------
    # Register all static categories
    # ---------------------------------------------------------
    categories = set()
    
    # Static primary categories
    categories.add(_create_category("cat_error", ["View Logs", "Retry", "Dismiss"]))
    categories.add(_create_category("cat_blocked", ["View", "Unblock", "Dismiss"]))
    categories.add(_create_category("cat_limit", ["View", "Dismiss"]))
    categories.add(_create_category("cat_decision", ["Reply"], is_reply=True))
    categories.add(_create_category("cat_recommend", ["View", "Dismiss"]))
    categories.add(_create_category("cat_completed", ["Follow Up", "Show", "Dismiss"]))
    
    # PERMISSION categories permutations
    categories.add(_create_category("cat_permission_1", ["Allow", "Deny"]))
    categories.add(_create_category("cat_permission_2", ["Proceed", "Cancel"]))
    categories.add(_create_category("cat_permission_3", ["Yes", "No"]))
    categories.add(_create_category("cat_permission_4", ["Approve", "Reject"]))
    categories.add(_create_category("cat_permission_5", ["Run", "Cancel"]))
    
    center.setNotificationCategories_(categories)
    
    # ---------------------------------------------------------
    
    # Request permissions
    options = UNAuthorizationOptionAlert | UNAuthorizationOptionSound | UNAuthorizationOptionBadge
    
    def permission_handler(granted, error):
        if not granted:
            logger.warning("Notification permission denied by user.")
        if error:
            logger.error("Notification permission error: %s", error)
            
    center.requestAuthorizationWithOptions_completionHandler_(options, permission_handler)

def check_notification_permission(callback):
    """
    Checks current notification authorization status.
    Calls callback(True) if authorized, callback(False) if not.
    Useful for startup diagnostics.
    """
    center = UNUserNotificationCenter.currentNotificationCenter()
    center.getNotificationSettingsWithCompletionHandler_(
        lambda settings: callback(
            settings.authorizationStatus() == 2  # UNAuthorizationStatusAuthorized
        )
    )

def _send_notification(event_id, title, body, category_id, tool, tab_id, window_id):
    center = UNUserNotificationCenter.currentNotificationCenter()
    
    content = UNMutableNotificationContent.alloc().init()
    content.setTitle_(title)
    content.setBody_(body)
    content.setSubtitle_(f"Agent: {tool}")
    content.setCategoryIdentifier_(category_id)
    content.setUserInfo_({
        "event_id": event_id,
        "tab_id": tab_id,
        "window_id": window_id
    })
    
    trigger = UNTimeIntervalNotificationTrigger.triggerWithTimeInterval_repeats_(0.1, False)
    
    request_identifier = f"agentwatch_{event_id}"
    request = UNNotificationRequest.requestWithIdentifier_content_trigger_(
        request_identifier, content, trigger
    )
    
    def completion(error):
        if error:
            logger.error(f"Failed to deliver notification: {error}")
            
    center.addNotificationRequest_withCompletionHandler_(request, completion)

def show_error_popup(event_id, preview, tool, tab_id, window_id):
    _send_notification(event_id, "Agent Error", preview, "cat_error", tool, tab_id, window_id)

def show_blocked_popup(event_id, preview, tool, buttons_list, tab_id, window_id):
    _send_notification(event_id, "Agent Blocked", preview, "cat_blocked", tool, tab_id, window_id)

def show_permission_popup(event_id, preview, tool, buttons_list, tab_id, window_id):
    # Match buttons list to one of the 5 permission categories
    btn_str = ",".join(buttons_list).lower() if buttons_list else ""
    
    if "proceed" in btn_str:
        cat_id = "cat_permission_2"
    elif "yes" in btn_str:
        cat_id = "cat_permission_3"
    elif "approve" in btn_str:
        cat_id = "cat_permission_4"
    elif "run" in btn_str:
        cat_id = "cat_permission_5"
    else:
        cat_id = "cat_permission_1" # Default Allow/Deny
        
    _send_notification(event_id, "Permission Required", preview, cat_id, tool, tab_id, window_id)

def show_limit_popup(event_id, preview, tool, tab_id, window_id):
    _send_notification(event_id, "Agent Limit Reached", preview, "cat_limit", tool, tab_id, window_id)

def show_decision_popup(event_id, preview, tool, context_lines, tab_id, window_id):
    body = context_lines if context_lines else preview
    _send_notification(event_id, "Decision Needed", body, "cat_decision", tool, tab_id, window_id)

def show_recommend_popup(event_id, preview, tool, tab_id, window_id):
    _send_notification(event_id, "Agent Recommendation", preview, "cat_recommend", tool, tab_id, window_id)
    def cancel():
        center = UNUserNotificationCenter.currentNotificationCenter()
        center.removeDeliveredNotificationsWithIdentifiers_([f"agentwatch_{event_id}"])
    threading.Timer(15.0, cancel).start()

def show_completed_popup(event_id, preview, tool, tab_id, window_id):
    _send_notification(event_id, "Task Completed", preview, "cat_completed", tool, tab_id, window_id)
    def cancel():
        center = UNUserNotificationCenter.currentNotificationCenter()
        center.removeDeliveredNotificationsWithIdentifiers_([f"agentwatch_{event_id}"])
    threading.Timer(10.0, cancel).start()

def route_popup(result_dict):
    """
    Called by main.py callback to route events to the correct specific popup definition
    """
    cls = result_dict["classification"]
    event_type = cls["event_type"]
    preview = cls["truncated_preview"]
    original_text = result_dict.get("original_text", "")
    
    event_id = result_dict.get("event_id")
    tab_id = result_dict.get("tabId")
    window_id = result_dict.get("windowId")
    tool = result_dict.get("tool", "unknown")
    
    buttons_raw = result_dict.get("buttons", "") 
    buttons_list = [b.strip() for b in buttons_raw.split(',')] if buttons_raw else []
    
    lines = original_text.split('\n')
    context_lines = "\n".join(lines[-3:]) if len(lines) >= 3 else original_text

    if event_type == "ERROR":
        show_error_popup(event_id, preview, tool, tab_id, window_id)
    elif event_type == "BLOCKED":
        show_blocked_popup(event_id, preview, tool, buttons_list, tab_id, window_id)
    elif event_type == "PERMISSION":
        show_permission_popup(event_id, preview, tool, buttons_list, tab_id, window_id)
    elif event_type == "LIMIT":
        show_limit_popup(event_id, preview, tool, tab_id, window_id)
    elif event_type == "DECISION":
        show_decision_popup(event_id, preview, tool, context_lines, tab_id, window_id)
    elif event_type == "RECOMMEND":
        show_recommend_popup(event_id, preview, tool, tab_id, window_id)
    elif event_type == "COMPLETED":
        show_completed_popup(event_id, preview, tool, tab_id, window_id)
