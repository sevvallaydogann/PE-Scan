import customtkinter as ctk
import pandas as pd
import pickle
import random
import threading
import time
import os

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("green")  

class PEScanApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PEScan AI - Next Gen Malware Defense")
        self.geometry("600x450")
        self.resizable(False, False)

        self.model = self.load_model()
        self.data = self.load_data()

        self.label_title = ctk.CTkLabel(self, text="PEScan AI Defense System", font=("Roboto Medium", 24))
        self.label_title.pack(pady=20)

        self.status_frame = ctk.CTkFrame(self, width=500, height=150, corner_radius=10)
        self.status_frame.pack(pady=10)
        
        self.lbl_status = ctk.CTkLabel(self.status_frame, text="SYSTEM SECURE", font=("Roboto", 30, "bold"), text_color="#2CC985")
        self.lbl_status.place(relx=0.5, rely=0.4, anchor="center")
        
        self.lbl_file = ctk.CTkLabel(self.status_frame, text="Ready to scan...", font=("Roboto", 12), text_color="gray")
        self.lbl_file.place(relx=0.5, rely=0.7, anchor="center")

        self.progress = ctk.CTkProgressBar(self, width=400, mode="indeterminate")
        self.progress.pack(pady=20)
        self.progress.set(0)

        self.btn_scan = ctk.CTkButton(self, text="SCAN RANDOM FILE", width=200, height=50, 
                                      font=("Roboto", 15, "bold"), command=self.start_scan)
        self.btn_scan.pack(pady=10)

        self.console = ctk.CTkTextbox(self, width=500, height=100)
        self.console.pack(pady=10)
        self.console.insert("0.0", "[*] System Initialized...\n[*] AI Model Loaded Successfully.\n")

    def load_model(self):
        try:
            with open("pescan_model.pkl", "rb") as f:
                return pickle.load(f)
        except:
            return None

    def load_data(self):
        try:
            return pd.read_csv("data/dataset_malwares.csv")
        except:
            return None

    def log(self, message):
        self.console.insert("end", message + "\n")
        self.console.see("end")

    def start_scan(self):
        threading.Thread(target=self.run_scan_logic).start()

    def run_scan_logic(self):
        if self.model is None or self.data is None:
            self.log("[!] Error: Model or Data missing!")
            return

        self.btn_scan.configure(state="disabled")
        self.progress.start()
        self.lbl_status.configure(text="SCANNING...", text_color="#F1C40F") 
        
        idx = random.randint(0, len(self.data) - 1)
        sample = self.data.drop(["Name", "Malware"], axis=1, errors='ignore').iloc[[idx]]
        real_label = self.data["Malware"].iloc[idx]
        
        if "Name" in self.data.columns:
            filename = self.data["Name"].iloc[idx]
        else:
            filename = f"suspect_file_{random.randint(1000,9999)}.exe"

        self.lbl_file.configure(text=f"Analyzing: {filename}")
        self.log(f"[*] Scanning: {filename}")
        
        time.sleep(1.5)
        
        prediction = self.model.predict(sample)[0]
        confidence = max(self.model.predict_proba(sample)[0]) * 100

        self.progress.stop()
        self.progress.set(1 if prediction == 1 else 0)
        
        if prediction == 1:
            self.lbl_status.configure(text="MALWARE DETECTED!", text_color="#E74C3C") 
            self.log(f"[!!!] THREAT DETECTED: {filename}")
            self.log(f"      Confidence: {confidence:.2f}% | AI Analysis: MALICIOUS")
        else:
            self.lbl_status.configure(text="SYSTEM SAFE", text_color="#2CC985") 
            self.log(f"[+] Clean File: {filename}")
            self.log(f"      Confidence: {confidence:.2f}% | AI Analysis: BENIGN")

        self.btn_scan.configure(state="normal")

if __name__ == "__main__":
    app = PEScanApp()
    app.mainloop()