import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from datetime import datetime

class ProductivitySuite:
    def __init__(self, root):
        self.root = root
        self.root.title("CSBS Student Suite (Lite)")
        self.root.geometry("600x500")

        # --- DATA STORAGE (Simple Lists) ---
        self.exams = []      # List of dicts: {"sub": "", "date": ""}
        self.resources = []  # List of dicts: {"sub": "", "link": ""}
        self.stats = {}      # Dict: {"Subject": {"hours": 0, "marks": 0}}

        # --- TAB CONTROL ---
        self.tabs = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text="📅 Scheduler")
        self.tabs.add(self.tab2, text="📚 Resources")
        self.tabs.add(self.tab3, text="📈 Analytics")
        self.tabs.pack(expand=1, fill="both")

        self.setup_scheduler()
        self.setup_resources()
        self.setup_analytics()

    # ================= TAB 1: SCHEDULER =================
    def setup_scheduler(self):
        frame = ttk.Frame(self.tab1, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0)
        self.exam_sub = ttk.Entry(frame)
        self.exam_sub.grid(row=0, column=1)

        ttk.Label(frame, text="Date (DD-MM-YYYY):").grid(row=1, column=0)
        self.exam_date = ttk.Entry(frame)
        self.exam_date.grid(row=1, column=1)

        ttk.Button(frame, text="Add Exam", command=self.add_exam).grid(row=2, columnspan=2, pady=5)

        self.exam_tree = ttk.Treeview(self.tab1, columns=("Sub", "Days"), show='headings', height=8)
        self.exam_tree.heading("Sub", text="Subject")
        self.exam_tree.heading("Days", text="Days Remaining")
        self.exam_tree.pack(padx=10, fill="both")

    def add_exam(self):
        try:
            date_obj = datetime.strptime(self.exam_date.get(), "%d-%m-%Y")
            days_left = (date_obj - datetime.now()).days + 1
            self.exams.append({"sub": self.exam_sub.get(), "days": days_left})
            self.refresh_exams()
        except ValueError:
            messagebox.showerror("Error", "Use format: DD-MM-YYYY")

    def refresh_exams(self):
        for i in self.exam_tree.get_children(): self.exam_tree.delete(i)
        for e in self.exams:
            self.exam_tree.insert("", "end", values=(e["sub"], e["days"]))

    # ================= TAB 2: RESOURCES =================
    def setup_resources(self):
        frame = ttk.Frame(self.tab2, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0)
        self.res_sub = ttk.Entry(frame)
        self.res_sub.grid(row=0, column=1)

        ttk.Label(frame, text="URL Link:").grid(row=1, column=0)
        self.res_link = ttk.Entry(frame)
        self.res_link.grid(row=1, column=1)

        ttk.Button(frame, text="Save Link", command=self.add_res).grid(row=2, columnspan=2, pady=5)

        self.res_list = tk.Listbox(self.tab2)
        self.res_list.pack(padx=10, fill="both", expand=True)
        self.res_list.bind('<Double-1>', lambda e: webbrowser.open(self.res_list.get(tk.ACTIVE).split(" -> ")[1]))

    def add_res(self):
        s, l = self.res_sub.get(), self.res_link.get()
        if s and l:
            self.res_list.insert(tk.END, f"{s} -> {l}")
            self.res_sub.delete(0, tk.END); self.res_link.delete(0, tk.END)

    # ================= TAB 3: ANALYTICS =================
    def setup_analytics(self):
        frame = ttk.Frame(self.tab3, padding=10)
        frame.pack(fill="x")

        ttk.Label(frame, text="Subject:").grid(row=0, column=0)
        self.stat_sub = ttk.Entry(frame)
        self.stat_sub.grid(row=0, column=1)

        ttk.Label(frame, text="Hours Studied:").grid(row=1, column=0)
        self.stat_hrs = ttk.Entry(frame)
        self.stat_hrs.grid(row=1, column=1)

        ttk.Label(frame, text="Marks Obtained:").grid(row=2, column=0)
        self.stat_marks = ttk.Entry(frame)
        self.stat_marks.grid(row=2, column=1)

        ttk.Button(frame, text="Update Stats", command=self.update_stats).grid(row=3, columnspan=2, pady=5)

        self.stat_text = tk.Text(self.tab3, height=10, state='disabled')
        self.stat_text.pack(padx=10, pady=10, fill="both")

    def update_stats(self):
        try:
            sub = self.stat_sub.get()
            h = float(self.stat_hrs.get())
            m = float(self.stat_marks.get())
            
            # Simple Dictionary logic: if exists add, else create
            if sub in self.stats:
                self.stats[sub]["hours"] += h
                self.stats[sub]["marks"] = m
            else:
                self.stats[sub] = {"hours": h, "marks": m}
            
            self.show_analysis()
        except ValueError:
            messagebox.showerror("Error", "Enter numbers for Hours/Marks")

    def show_analysis(self):
        self.stat_text.config(state='normal')
        self.stat_text.delete('1.0', tk.END)
        for sub, data in self.stats.items():
            roi = round(data["marks"] / data["hours"], 2) if data["hours"] > 0 else 0
            self.stat_text.insert(tk.END, f"Subject: {sub} | ROI: {roi} Marks/Hr\n")
        self.stat_text.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivitySuite(root)
    root.mainloop()