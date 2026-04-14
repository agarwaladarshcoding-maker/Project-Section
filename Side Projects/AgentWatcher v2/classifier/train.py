import os
import csv
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'training_data.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'model')

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
            
            # Combine the three fields into one single signal string
            combined = f"{msg} [BUTTONS] {buttons} [CTX] {ctx}"
            
            X_raw.append(combined)
            y.append(label)
            original_texts.append(msg)
            
    return X_raw, y, original_texts

def main():
    print("Loading data...")
    X_raw, y, original_texts = load_data()
    print(f"Loaded {len(X_raw)} records.")
    
    print("Splitting data...")
    X_train_raw, X_test_raw, y_train, y_test, txt_train, txt_test = train_test_split(
        X_raw, y, original_texts, 
        test_size=0.2, 
        stratify=y, 
        random_state=42
    )
    
    print("Vectorizing Text...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), 
        max_features=8000, 
        sublinear_tf=True
    )
    
    X_train = vectorizer.fit_transform(X_train_raw)
    X_test = vectorizer.transform(X_test_raw)
    
    print("Training LinearSVC model...")
    clf = LinearSVC(class_weight='balanced', random_state=42, max_iter=2000)
    clf.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    
    # Validation & Output
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {acc:.4f}\n")
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save Model & Vectorizer
    print("\nSaving model & vectorizer...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(clf, os.path.join(MODEL_DIR, 'model.pkl'))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, 'vectorizer.pkl'))
    print(f"Saved artifacts to {MODEL_DIR}")
    
    # Identify failures
    print("\n=== TOP ERRORS (Max 10) ===")
    errors = 0
    for i in range(len(y_test)):
        if y_test[i] != y_pred[i]:
            print(f"ACTUAL: {y_test[i]:<10} PREDICTED: {y_pred[i]:<10} | TEXT: {txt_test[i]}")
            errors += 1
            if errors >= 10:
                break
                
    if errors == 0:
         print("Zero errors encountered in test set!")

if __name__ == '__main__':
    main()
