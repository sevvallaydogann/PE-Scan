import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import os

if not os.path.exists("images"):
    os.makedirs("images")

def train():
    print("\n" + "="*50)
    print("   PEScan v2.0 - Model Training & Visualization")
    print("="*50)

    print("[*] Loading Training Data...")
    try:
        data = pd.read_csv("data/dataset_malwares.csv")
    except FileNotFoundError:
        print("[!] Error: dataset_malwares.csv not found.")
        return

    X = data.drop(["Name", "Malware"], axis=1, errors='ignore') 
    y = data["Malware"]

    print(f"[*] Dataset Loaded: {X.shape[0]} samples.")
    print("[*] Training Random Forest Model... (Please wait)")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    predictions = clf.predict(X_test)
    accuracy = accuracy_score(y_test, predictions) * 100
    print(f"\n[+] Model Accuracy: {accuracy:.2f}% 🚀")

    print("[*] Generating Confusion Matrix...")
    cm = confusion_matrix(y_test, predictions)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Benign', 'Malware'], 
                yticklabels=['Benign', 'Malware'])
    plt.title('PEScan Confusion Matrix')
    plt.ylabel('Actual Label')
    plt.xlabel('Predicted Label')
    plt.savefig('images/confusion_matrix.png') 
    print("[+] Saved: images/confusion_matrix.png")

    print("[*] Analyzing Top Features...")
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1][:10] 
    
    plt.figure(figsize=(10, 6))
    plt.title('Top 10 Features used for Malware Detection')
    plt.bar(range(10), importances[indices], align='center', color='red')
    plt.xticks(range(10), [X.columns[i] for i in indices], rotation=45)
    plt.tight_layout()
    plt.savefig('images/feature_importance.png') 
    print("[+] Saved: images/feature_importance.png")

    with open("pescan_model.pkl", "wb") as f:
        pickle.dump(clf, f)
    print("\n[+] Training & Visualization Complete!")

if __name__ == "__main__":
    train()