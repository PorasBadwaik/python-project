import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import webbrowser
from datetime import datetime

# ==========================================
# FILE HANDLING & LOGIC
# ==========================================
DATA_FILE = "student_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {"exams": [], "resources": {}, "analytics": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# ==========================================
# MAIN GUI APPLICATION
# ==========================================
class ProductivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSBS Productivity Suite 🚀")
        self.root.geometry("600x500")
        
        # Load Data
        self.data = load_data()

        # Create Tabs
        self.tabs = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text="📅 Smart Scheduler")
        self.tabs.add(self.tab2, text="📚 Resource Hub")
        self.tabs.add(self.tab3, text="📈 Efficiency (ROI)")
        self.tabs.pack(expand=1, fill="both")

        # Initialize UI for each tab
        self.setup_scheduler_tab()
        self.setup_resource_tab()
        self.setup_analytics_tab()

    # ----------------------------------------------------
    # TAB 1: SMART SCHEDULER
    # ----------------------------------------------------
    def setup_scheduler_tab(self):
        # Input Frame
        frame = ttk.LabelFrame(self.tab1, text="Add New Exam")
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0, padx=5, pady=5)
        self.exam_sub_entry = ttk.Entry(frame)
        self.exam_sub_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Date (DD-MM-YYYY):").grid(row=0, column=2, padx=5, pady=5)
        self.exam_date_entry = ttk.Entry(frame)
        self.exam_date_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame, text="Add Exam", command=self.add_exam).grid(row=0, column=4, padx=5, pady=5)

        # List Area
        self.schedule_list = tk.Listbox(self.tab1, font=("Arial", 10))
        self.schedule_list.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.refresh_schedule_list()

    def add_exam(self):
        sub = self.exam_sub_entry.get()
        date = self.exam_date_entry.get()
        
        try:
            datetime.strptime(date, "%d-%m-%Y") # Validate date
            self.data["exams"].append({"subject": sub, "date": date})
            save_data(self.data)
            self.refresh_schedule_list()
            self.exam_sub_entry.delete(0, tk.END)
            self.exam_date_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Exam for {sub} added!")
        except ValueError:
            messagebox.showerror("Error", "Invalid Date Format! Use DD-MM-YYYY")

    def refresh_schedule_list(self):
        self.schedule_list.delete(0, tk.END)
        today = datetime.now()
        for exam in self.data["exams"]:
            exam_date = datetime.strptime(exam['date'], "%d-%m-%Y")
            days_left = (exam_date - today).days + 1
            status = "🚨 URGENT" if days_left <= 3 else "🟢 On Track"
            display_text = f"{exam['subject']} | {exam['date']} | {days_left} Days Left | {status}"
            self.schedule_list.insert(tk.END, display_text)

    # ----------------------------------------------------
    # TAB 2: RESOURCE HUB
    # ----------------------------------------------------
    def setup_resource_tab(self):
        frame = ttk.LabelFrame(self.tab2, text="Add Resource")
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0, padx=5)
        self.res_sub_entry = ttk.Entry(frame)
        self.res_sub_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Link/Path:").grid(row=1, column=0, padx=5)
        self.res_link_entry = ttk.Entry(frame, width=30)
        self.res_link_entry.grid(row=1, column=1, padx=5)

        ttk.Button(frame, text="Save Resource", command=self.add_resource).grid(row=2, column=1, pady=5)

        # Viewer
        ttk.Label(self.tab2, text="Double-click a resource to open:").pack(pady=5)
        self.res_list = tk.Listbox(self.tab2)
        self.res_list.pack(padx=10, fill="both", expand=True)
        self.res_list.bind('<Double-1>', self.open_resource) # Double click event

        self.refresh_resource_list()

    def add_resource(self):
        sub = self.res_sub_entry.get()
        link = self.res_link_entry.get()
        if sub and link:
            self.data["resources"][sub] = link
            save_data(self.data)
            self.refresh_resource_list()
            messagebox.showinfo("Saved", "Resource link saved successfully!")
        else:
            messagebox.showwarning("Input Error", "Please fill both fields")

    def refresh_resource_list(self):
        self.res_list.delete(0, tk.END)
        for sub, link in self.data["resources"].items():
            self.res_list.insert(tk.END, f"{sub} : {link}")

    def open_resource(self, event):
        selection = self.res_list.get(self.res_list.curselection())
        link = selection.split(" : ")[1]
        webbrowser.open(link)

    # ----------------------------------------------------
    # TAB 3: EFFICIENCY ENGINE (ROI)
    # ----------------------------------------------------
    def setup_analytics_tab(self):
        frame = ttk.LabelFrame(self.tab3, text="Log Data")
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0)
        self.roi_sub_entry = ttk.Entry(frame)
        self.roi_sub_entry.grid(row=0, column=1)

        ttk.Label(frame, text="Hours Studied:").grid(row=1, column=0)
        self.roi_hours_entry = ttk.Entry(frame)
        self.roi_hours_entry.grid(row=1, column=1)
        
        ttk.Label(frame, text="Marks Obtained:").grid(row=2, column=0)
        self.roi_marks_entry = ttk.Entry(frame)
        self.roi_marks_entry.grid(row=2, column=1)

        ttk.Button(frame, text="Update Data", command=self.update_analytics).grid(row=3, column=1, pady=10)

        self.roi_display = tk.Text(self.tab3, height=10, width=50)
        self.roi_display.pack(padx=10, pady=10)
        
        ttk.Button(self.tab3, text="Calculate ROI Report", command=self.show_roi).pack()

    def update_analytics(self):
        sub = self.roi_sub_entry.get()
        try:
            h = float(self.roi_hours_entry.get())
            m = float(self.roi_marks_entry.get())
            
            if sub not in self.data["analytics"]:
                self.data["analytics"][sub] = {"hours": 0, "marks": 0}
            
            self.data["analytics"][sub]["hours"] += h
            self.data["analytics"][sub]["marks"] = m # Updates marks to latest
            save_data(self.data)
            messagebox.showinfo("Success", f"Data logged for {sub}")
        except ValueError:
            messagebox.showerror("Error", "Hours and Marks must be numbers!")

    def show_roi(self):
        self.roi_display.delete('1.0', tk.END)
        self.roi_display.insert(tk.END, f"{'Subject':<15} {'ROI (Marks/Hr)':<15} {'Status'}\n")
        self.roi_display.insert(tk.END, "-"*45 + "\n")
        
        for sub, stats in self.data["analytics"].items():
            h = stats["hours"]
            m = stats["marks"]
            roi = round(m/h, 2) if h > 0 else 0
            
            status = "🔥 High Eff." if roi > 5 else "⚠️ Low Eff."
            self.roi_display.insert(tk.END, f"{sub:<15} {roi:<15} {status}\n")

# ==========================================
# DRIVER CODE
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivityApp(root)
    root.mainloop()