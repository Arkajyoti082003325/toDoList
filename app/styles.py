import tkinter as tk
from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    
    # Configure the main window style
    style.configure(
        "TFrame",
        background="#f0f0f0"
    )
    
    # Configure button styles
    style.configure(
        "TButton",
        padding=6,
        relief="flat",
        background="#4a90e2",
        foreground="white"
    )
    
    style.map(
        "TButton",
        background=[("active", "#3a7bc8"), ("disabled", "#cccccc")],
        foreground=[("disabled", "#888888")]
    )
    
    # Configure treeview styles
    style.configure(
        "Treeview",
        background="#ffffff",
        fieldbackground="#ffffff",
        foreground="#333333",
        rowheight=25
    )
    
    style.configure(
        "Treeview.Heading",
        background="#e0e0e0",
        relief="flat",
        padding=5
    )
    
    style.map(
        "Treeview",
        background=[("selected", "#4a90e2")],
        foreground=[("selected", "white")]
    )
    
    # Configure entry styles
    style.configure(
        "TEntry",
        padding=5,
        relief="flat"
    )
    
    # Configure label styles
    style.configure(
        "TLabel",
        background="#f0f0f0",
        foreground="#333333"
    )
    
    # Configure radiobutton styles
    style.configure(
        "TRadiobutton",
        background="#f0f0f0"
    )