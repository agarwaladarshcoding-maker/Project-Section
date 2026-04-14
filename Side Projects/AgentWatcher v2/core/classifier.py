import os
import joblib
import numpy as np

# Absolute paths based on project structure
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'classifier', 'model')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')
CALIBRATED_MODEL_PATH = os.path.join(MODEL_DIR, 'calibrated_model.pkl')

PRIORITY_ORDER = {
    "ERROR": 1,
    "BLOCKED": 2,
    "PERMISSION": 3,
    "LIMIT": 4,
    "DECISION": 5,
    "RECOMMEND": 6,
    "COMPLETED": 7
}

_vectorizer = None
_model = None

def _load_models():
    """Lazily load models to avoid huge memory footprint until needed"""
    global _vectorizer, _model
    if _vectorizer is None or _model is None:
        _vectorizer = joblib.load(VECTORIZER_PATH)
        _model = joblib.load(CALIBRATED_MODEL_PATH)

def _get_truncated_preview(text: str) -> str:
    """Returns the last 15-20 words of the input text"""
    words = text.split()
    if len(words) > 20:
        return "… " + " ".join(words[-20:])
    return text

def classify(text: str, buttons: str, ui_context: str) -> dict:
    """
    Classifies an agent message into one of 7 event types using the offline model.
    Applies a priority fallback mechanism if confidence < 0.75.
    """
    _load_models()
    
    # 1. Combine inputs -> exact same format as train.py
    combined = f"{text} [BUTTONS] {buttons} [CTX] {ui_context}"
    
    # 2. Vectorize
    X = _vectorizer.transform([combined])
    
    # 3. Predict & assess confidence
    probs = _model.predict_proba(X)[0]
    classes = _model.classes_
    
    sorted_indices = np.argsort(probs)[::-1]
    
    top_class = classes[sorted_indices[0]]
    max_prob = probs[sorted_indices[0]]
    
    event_type = top_class
    used_fallback = False
    
    # 4. Priority fallback mechanism 
    if max_prob < 0.75:
        used_fallback = True
        candidate1 = classes[sorted_indices[0]]
        candidate2 = classes[sorted_indices[1]]
        
        priority1 = PRIORITY_ORDER.get(candidate1, 99)
        priority2 = PRIORITY_ORDER.get(candidate2, 99)
        
        event_type = candidate1 if priority1 <= priority2 else candidate2

    # 5. Return dict
    return {
        "event_type": event_type,
        "confidence": float(max_prob),
        "truncated_preview": _get_truncated_preview(text),
        "used_fallback": used_fallback
    }

if __name__ == "__main__":
    print("Running classifier self-test...\n")
    
    test_cases = [
        ("Unhandled exception in database schema: Connection refused.", "View Logs,Dismiss", "Critical Error"),
        ("I need to execute a command to delete Docker container. Proceed?", "Allow,Deny", "Permission Request"),
        ("Successfully deployed Redis cache to production.", "Follow Up,Hide", "Task Complete")
    ]
    
    for text, buttons, ctx in test_cases:
        res = classify(text, buttons, ctx)
        print(f"INPUT: {text}")
        print(f"BUTTONS: {buttons}")
        print(f"CTX: {ctx}")
        print(f"OUTPUT: {res}\n")
