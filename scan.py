"""
PEScan - Static Malware Analysis Tool
Module: Scanner (Simulation)
Description: Loads the trained AI model and scans random files for demo purposes.
"""
import pandas as pd
import pickle
import random
import time
import os

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def load_model():
    print(f"[*] Loading AI Model ({Colors.YELLOW}pescan_model.pkl{Colors.RESET})...")
    try:
        with open("pescan_model.pkl", "rb") as f:
            model = pickle.load(f)
        print(f"{Colors.GREEN}[+] Model loaded successfully!{Colors.RESET}")
        return model
    except FileNotFoundError:
        print(f"{Colors.RED}[!] Error: Model file not found. Run train_model.py first!{Colors.RESET}")
        exit()

def load_data():
    print(f"[*] Loading Database for Simulation ({Colors.YELLOW}data/dataset_malwares.csv{Colors.RESET})...")
    try:
        data = pd.read_csv("data/dataset_malwares.csv")
        return data
    except FileNotFoundError:
        print(f"{Colors.RED}[!] Error: Data file not found.{Colors.RESET}")
        exit()

def scan():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{Colors.BLUE}")
    print(r"""
    ____  ______ _____
   / __ \/ ____// ___/_________ _____
  / /_/ / __/   \__ \/ ___/ __ `/ __ \
 / ____/ /___  ___/ / /__/ /_/ / / / /
/_/   /_____/ /____/\___/\__,_/_/ /_/  v1.0
    """)
    print(f"{Colors.RESET}")
    print("AI-Powered Static Malware Analysis Tool")
    print("="*50 + "\n")

    model = load_model()
    data = load_data()
    
    if "Malware" not in data.columns:
        print(f"{Colors.RED}[!] Error: The dataset is missing the 'Malware' label column.{Colors.RESET}")
        exit()

    X = data.drop(["Name", "Malware"], axis=1, errors='ignore')
    y_true = data["Malware"]
    
    if "Name" in data.columns:
        file_names = data["Name"]
    else:
        file_names = pd.Series([f"sample_{i}.exe" for i in range(len(data))])

    print("\n" + "="*50)
    print(f"[*] Starting Random Scan Simulation...")
    print("="*50)

    while True:
        input(f"\nPress {Colors.YELLOW}[ENTER]{Colors.RESET} to scan a random file (or 'q' to quit)...")
        
        idx = random.randint(0, len(data) - 1)
        
        sample = X.iloc[[idx]]
        real_label = y_true.iloc[idx]
        file_name = file_names.iloc[idx]
        
        print(f"\n[*] Scanning file: {Colors.BLUE}{file_name}{Colors.RESET}")
        print("[*] Extracting PE Header features...")
        time.sleep(0.3) 
        
        prediction = model.predict(sample)[0]
        
        proba = model.predict_proba(sample)[0]
        confidence = max(proba) * 100

        print("-" * 40)
        
        if prediction == 1:
            print(f"   RESULT: {Colors.RED}MALWARE DETECTED! {Colors.RESET}")
        else:
            print(f"   RESULT: {Colors.GREEN}BENIGN (SAFE) {Colors.RESET}")
            
        print(f"   Confidence: {confidence:.2f}%")
        
        truth = "MALWARE" if real_label == 1 else "BENIGN"
        is_correct = (prediction == real_label)
        
        verify_color = Colors.GREEN if is_correct else Colors.RED
        print(f"   Actual Type: {truth} | AI Accuracy: {verify_color}{'CORRECT' if is_correct else 'WRONG'}{Colors.RESET}")
        print("-" * 40)

if __name__ == "__main__":
    scan()