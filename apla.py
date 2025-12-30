import tkinter as tk
from tkinter import  ttk, messagebox
import pandas as pd # The star of the show
import os
import webbrowser
from datetime import datetime


EXAM_FILE = "data_exams.csv"
RESOURCE_FILE = "data_resources.csv"
ANALYTICS_FILE = "data_analytics.csv"



root = tk.Tk()
root.title("Productivity Suite")
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
#===================tab 1 starts=========================
def tab1():
    notebook.add(tab1, text="Smart Scheduler")
#for frame named add new exam
    fr=ttk.LabelFrame(tab1,text="Add new exam.")
    fr.pack(padx=10,pady=10,fill='x')
#for subject
    ttk.Label(fr,text="Subject:").grid(row=0)
    e1=ttk.Entry(fr)
    e1.grid(row=0,column=1)
#for date
    ttk.Label(fr,text="Date:(DD-MM-YYYY)").grid(row=0,column=2)
    e2=ttk.Entry(fr)
    e2.grid(row=0,column=3)
    ttk.Button(fr,text="Add").grid(row=0, column=4, padx=5)
    list1 = tk.Listbox(tab1, font=("Arial", 10))
    list1.pack(padx=10, pady=10, fill="both", expand=True)
#def add_exam():
  #  sub=e1.get()
   # date=e2.get()



    try:
            datetime.strftime(datetime, "%d-%m-%Y") # Validation
            
            # PANDAS LOGIC: Create a new row and add it
            new_row = pd.DataFrame([{"Subject": e1, "Date": e2}])
            fr.df_exams = pd.concat([fr.df_exams, new_row], ignore_index=True)
            
            pd.save_csv(fr.df_exams, EXAM_FILE)
           
            messagebox.showinfo("Success", "Exam Added!")
    except ValueError:
            messagebox.showerror("Error", "Invalid Date Format!")

#=========================tab 1 end ========================


#=========================tab 2 start=======================
notebook.add(tab2, text="Resource Hub")
#for frame named add new exam
fr1=ttk.LabelFrame(tab2,text="Add Resources.")
fr1.pack(padx=10,pady=10,fill='x')
#for subject
ttk.Label(fr1,text="Subject:").grid(row=0)
e1=ttk.Entry(fr1).grid(row=0,column=1)
#for date
ttk.Label(fr1,text="Link :").grid(row=1,column=0)
e2=ttk.Entry(fr1).grid(row=1,column=1)
ttk.Button(fr1,text="Save").grid(row=2, column=1, padx=10)
list2= tk.Listbox(tab2, font=("Arial", 10))
list2.pack(padx=10, pady=10, fill="both", expand=True)
#=========================tab 2 ends ========================


#========================= tab 3 starts =====================
notebook.add(tab3, text="Efficiency(ROI)")
#for frame named add new exam
fr2=ttk.LabelFrame(tab3,text="Log Study Daata")
fr2.pack(padx=10,pady=10,fill='x')
#for subject
ttk.Label(fr2,text="Subject:").grid(row=0)
e1=ttk.Entry(fr2).grid(row=0,column=1)
#for date
ttk.Label(fr2,text="Hours :").grid(row=1,column=0)
e2=ttk.Entry(fr2).grid(row=1,column=1)
ttk.Label(fr2,text="Marks :").grid(row=2,column=0)
e3=ttk.Entry(fr2).grid(row=2,column=1)
ttk.Button(fr2,text="Add").grid(row=3, column=1, padx=5)
list3 = tk.Listbox(tab3, font=("Arial", 10))
list3.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()