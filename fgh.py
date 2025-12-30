import tkinter as tk
from tkinter import ttk

def create_app():
    root = tk.Tk()
    root.title("Multi-Tab System")
    root.geometry("400x300")

    # 1. Create the Notebook (The Parent Container)
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # 2. Create the Frames (The "Pages")
    # You create these all at once during initialization
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    # 3. Add the Frames to the Notebook with Labels
    notebook.add(tab1, text="Home")
    notebook.add(tab2, text="Analytics")
    notebook.add(tab3, text="Settings")

    # 4. Adding Content to Tab 1
    tk.Label(tab1, text="Welcome to the Home Screen", pady=20).pack()

    # 5. Adding Content to Tab 2
    tk.Label(tab2, text="Data Analytics View", pady=20).pack()
    tk.Button(tab2, text="Export CSV").pack()

    root.mainloop()

create_app()