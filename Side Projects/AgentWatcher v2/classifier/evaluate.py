import os
import csv
import joblib
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.calibration import CalibratedClassifierCV

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'training_data.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')
CALIBRATED_MODEL_PATH = os.path.join(MODEL_DIR, 'calibrated_model.pkl')

def load_data():
    X_raw = []
    y = []
    original_texts = []
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            msg = row['message_text']
            buttons = row['buttons_present']
            ctx = row['ui_context']
            label = row['event_type']
            
            combined = f"{msg} [BUTTONS] {buttons} [CTX] {ctx}"
            X_raw.append(combined)
            y.append(label)
            original_texts.append(msg)
            
    return X_raw, np.array(y), original_texts

def main():
    print("Loading vectorizer and full dataset...")
    vectorizer = joblib.load(VECTORIZER_PATH)
    X_raw, y, original_texts = load_data()
    
    X = vectorizer.transform(X_raw)
    
    print("\nRunning cross-validation on 100% of data (cv=5)...")
    base_clf = LinearSVC(class_weight='balanced', max_iter=2000, random_state=42)
    y_pred_cv = cross_val_predict(base_clf, X, y, cv=5)
    
    acc = accuracy_score(y, y_pred_cv)
    print(f"\nOverall Cross-Validated Accuracy: {acc:.4f}\n")
    print("Classification Report:")
    print(classification_report(y, y_pred_cv))
    print("Confusion Matrix:")
    cm = confusion_matrix(y, y_pred_cv)
    print(cm)
    
    print("\nTraining CalibratedClassifierCV on full dataset for probabilities...")
    calibrated_clf = CalibratedClassifierCV(base_clf, cv=5)
    calibrated_clf.fit(X, y)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(calibrated_clf, CALIBRATED_MODEL_PATH)
    print(f"Saved calibrated model to {CALIBRATED_MODEL_PATH}")
    
    print("\nEvaluating Confidence Scores...")
    # Calculate probabilities across the full dataset to find inherently ambiguous cases
    probs = calibrated_clf.predict_proba(X)
    classes = calibrated_clf.classes_
    
    low_confidence_count = 0
    print("\n=== LOW CONFIDENCE EXAMPLES (Max Confidence < 0.60) ===")
    for i in range(len(y)):
        max_prob = np.max(probs[i])
        if max_prob < 0.60:
            low_confidence_count += 1
            # Get top 2 predictions for context
            top_two_indices = np.argsort(probs[i])[-2:][::-1]
            pred1 = classes[top_two_indices[0]]
            prob1 = probs[i][top_two_indices[0]]
            pred2 = classes[top_two_indices[1]]
            prob2 = probs[i][top_two_indices[1]]
            
            print(f"ACTUAL: {y[i]:<10} | PRED1 (Top): {pred1} ({prob1:.2f}) | PRED2: {pred2} ({prob2:.2f})")
            print(f"TEXT: {original_texts[i]}")
            print("-" * 60)
            
    print("\n=== SUMMARY ===")
    print(f"Total examples analyzed: {len(y)}")
    print(f"Total below 0.60 confidence: {low_confidence_count}")
    
    # Calculate which class pairs confused the model most based on CV predictions
    print("\nMost Confused Class Pairs (from CV errors):")
    confused_pairs = {}
    class_labels = np.unique(y)
    for i, true_label in enumerate(class_labels):
        for j, pred_label in enumerate(class_labels):
            if i != j and cm[i, j] > 0:
                pair = tuple(sorted([true_label, pred_label]))
                confused_pairs[pair] = confused_pairs.get(pair, 0) + cm[i, j]
                
    sorted_pairs = sorted(confused_pairs.items(), key=lambda item: item[1], reverse=True)
    if not sorted_pairs:
        print("None! Perfect CV predictions (highly unlikely but possible).")
    for pair, count in sorted_pairs[:5]: # Show top 5
        print(f" - {pair[0]} & {pair[1]}: {count} errors")

if __name__ == '__main__':
    main()
