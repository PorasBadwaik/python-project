import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd # The star of the show
import os
import webbrowser
from datetime import datetime

# ==========================================
# FILE CONFIGURATION
# ==========================================
# We now use CSV files (Excel compatible) instead of JSON
EXAM_FILE = "data_exams.csv"
RESOURCE_FILE = "data_resources.csv"
ANALYTICS_FILE = "data_analytics.csv"

# ==========================================
# PANDAS HELPER FUNCTIONS
# ==========================================
def load_csv(filename, columns):
    """
    Loads a CSV into a Pandas DataFrame. 
    If file doesn't exist, returns an empty DataFrame with specified columns.
    """
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=columns)

def save_csv(df, filename):
    """Saves the DataFrame to a CSV file."""
    df.to_csv(filename, index=False)

# ==========================================
# MAIN GUI APPLICATION
# ==========================================
class ProductivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSBS Productivity Suite (Pandas Edition) 🐼")
        self.root.geometry("650x550")
        
        # Load DataFrames directly into memory
        self.df_exams = load_csv(EXAM_FILE, ["Subject", "Date"])
        self.df_resources = load_csv(RESOURCE_FILE, ["Subject", "Link"])
        self.df_analytics = load_csv(ANALYTICS_FILE, ["Subject", "Hours", "Marks"])

        # Create Tabs
        self.tabs = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text="📅 Smart Scheduler")
        self.tabs.add(self.tab2, text="📚 Resource Hub")
        self.tabs.add(self.tab3, text="📈 Efficiency (ROI)")
        self.tabs.pack(expand=1, fill="both")

        self.setup_scheduler_tab()
        self.setup_resource_tab()
        self.setup_analytics_tab()

    # ----------------------------------------------------
    # TAB 1: SCHEDULER (Using Pandas)
    # ----------------------------------------------------
    def setup_scheduler_tab(self):
        frame = ttk.LabelFrame(self.tab1, text="Add New Exam")
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0, padx=5)
        self.exam_sub_entry = ttk.Entry(frame)
        self.exam_sub_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Date (DD-MM-YYYY):").grid(row=0, column=2, padx=5)
        self.exam_date_entry = ttk.Entry(frame)
        self.exam_date_entry.grid(row=0, column=3, padx=5)

        ttk.Button(frame, text="Add", command=self.add_exam).grid(row=0, column=4, padx=5)

        self.schedule_list = tk.Listbox(self.tab1, font=("Arial", 10))
        self.schedule_list.pack(padx=10, pady=10, fill="both", expand=True)
        self.refresh_schedule()

    def add_exam(self):
        sub = self.exam_sub_entry.get()
        date = self.exam_date_entry.get()
        
        try:
            datetime.strptime(date, "%d-%m-%Y") # Validation
            
            # PANDAS LOGIC: Create a new row and add it
            new_row = pd.DataFrame([{"Subject": sub, "Date": date}])
            self.df_exams = pd.concat([self.df_exams, new_row], ignore_index=True)
            
            save_csv(self.df_exams, EXAM_FILE)
            self.refresh_schedule()
            messagebox.showinfo("Success", "Exam Added!")
        except ValueError:
            messagebox.showerror("Error", "Invalid Date Format!")

    def refresh_schedule(self):
        self.schedule_list.delete(0, tk.END)
        today = datetime.now()
        
        # PANDAS LOGIC: Iterate over rows
        for index, row in self.df_exams.iterrows():
            exam_date = datetime.strptime(row['Date'], "%d-%m-%Y")
            days_left = (exam_date - today).days + 1
            status = "🚨 URGENT" if days_left <= 3 else "🟢 On Track"
            
            self.schedule_list.insert(tk.END, f"{row['Subject']} | {row['Date']} | {days_left} Days | {status}")

    # ----------------------------------------------------
    # TAB 2: RESOURCES (Using Pandas)
    # ----------------------------------------------------
    def setup_resource_tab(self):
        frame = ttk.LabelFrame(self.tab2, text="Add Resource")
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0, padx=5)
        self.res_sub = ttk.Entry(frame)
        self.res_sub.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Link:").grid(row=1, column=0, padx=5)
        self.res_link = ttk.Entry(frame, width=30)
        self.res_link.grid(row=1, column=1, padx=5)

        ttk.Button(frame, text="Save", command=self.add_resource).grid(row=2, column=1, pady=5)

        self.res_list = tk.Listbox(self.tab2)
        self.res_list.pack(padx=10, fill="both", expand=True)
        self.res_list.bind('<Double-1>', self.open_resource)
        self.refresh_resources()

    def add_resource(self):
        sub = self.res_sub.get()
        link = self.res_link.get()
        
        if sub and link:
            # PANDAS LOGIC: Append new row
            new_row = pd.DataFrame([{"Subject": sub, "Link": link}])
            self.df_resources = pd.concat([self.df_resources, new_row], ignore_index=True)
            save_csv(self.df_resources, RESOURCE_FILE)
            self.refresh_resources()
        else:
            messagebox.showwarning("Error", "Fill all fields")

    def refresh_resources(self):
        self.res_list.delete(0, tk.END)
        for index, row in self.df_resources.iterrows():
            self.res_list.insert(tk.END, f"{row['Subject']} : {row['Link']}")

    def open_resource(self, event):
        selection = self.res_list.get(self.res_list.curselection())
        link = selection.split(" : ")[1]
        webbrowser.open(link)

    # ----------------------------------------------------
    # TAB 3: ANALYTICS (Using Pandas Power ⚡)
    # ----------------------------------------------------
    def setup_analytics_tab(self):
        frame = ttk.LabelFrame(self.tab3, text="Log Study Data")
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0)
        self.roi_sub = ttk.Entry(frame)
        self.roi_sub.grid(row=0, column=1)

        ttk.Label(frame, text="Hours:").grid(row=1, column=0)
        self.roi_hours = ttk.Entry(frame)
        self.roi_hours.grid(row=1, column=1)
        
        ttk.Label(frame, text="Marks:").grid(row=2, column=0)
        self.roi_marks = ttk.Entry(frame)
        self.roi_marks.grid(row=2, column=1)

        ttk.Button(frame, text="Update", command=self.update_analytics).grid(row=3, column=1, pady=10)

        # We use a Treeview here because Pandas data looks like a table
        self.tree = ttk.Treeview(self.tab3, columns=("Subject", "ROI", "Status"), show='headings')
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("ROI", text="ROI (Marks/Hr)")
        self.tree.heading("Status", text="Status")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Button(self.tab3, text="Calculate ROI Report", command=self.show_roi).pack()

    def update_analytics(self):
        sub = self.roi_sub.get()
        try:
            h = float(self.roi_hours.get())
            m = float(self.roi_marks.get())
            
            # PANDAS LOGIC: Check if subject exists
            mask = self.df_analytics['Subject'] == sub
            
            if mask.any():
                # Update existing row using .loc
                self.df_analytics.loc[mask, 'Hours'] += h
                self.df_analytics.loc[mask, 'Marks'] = m
            else:
                # Add new row
                new_row = pd.DataFrame([{"Subject": sub, "Hours": h, "Marks": m}])
                self.df_analytics = pd.concat([self.df_analytics, new_row], ignore_index=True)
            
            save_csv(self.df_analytics, ANALYTICS_FILE)
            messagebox.showinfo("Success", "Data Updated")
            
        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers")

    def show_roi(self):
        # Clear current table
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        if self.df_analytics.empty:
            return

        # ==========================================
        # THE "CSBS" FLEX: Vectorized Calculation
        # ==========================================
        # instead of a loop, we calculate ALL rows at once
        temp_df = self.df_analytics.copy()
        
        # Calculate ROI Column
        # Avoid division by zero
        temp_df['ROI'] = temp_df.apply(lambda x: round(x['Marks'] / x['Hours'], 2) if x['Hours'] > 0 else 0, axis=1)
        
        # Sort by Efficiency (Lowest first = needs attention)
        temp_df = temp_df.sort_values(by='ROI', ascending=True)

        # Populate GUI
        for index, row in temp_df.iterrows():
            roi = row['ROI']
            status = "🔥 High Eff." if roi > 5 else "⚠️ Low Eff."
            self.tree.insert("", tk.END, values=(row['Subject'], roi, status))

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivityApp(root)
    root.mainloop()