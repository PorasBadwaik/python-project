import tkinter as tk
from tkinter import  ttk, messagebox
import pandas as pd # The star of the show
import os
import webbrowser
from datetime import datetime



root = tk.Tk()
root.title("Productivity Suite")
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
#tab 1 starts
notebook.add(tab1, text="Smart Scheduler")
#for frame named add new exam
fr=ttk.LabelFrame(tab1,text="Add new exam.")
fr.pack(padx=10,pady=10,fill='x')
#for subject
ttk.Label(fr,text="Subject:").grid(row=0)
e1=ttk.Entry(fr).grid(row=0,column=1)
#for date
ttk.Label(fr,text="Date:").grid(row=0,column=2)
e2=ttk.Entry(fr).grid(row=0,column=3)
ttk.Button(fr,text="Add").grid(row=0, column=4, padx=5)
#tab 1 end
#tab 2 start
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
#tab 2 ends 
# tab 3 starts 
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

root.mainloop()