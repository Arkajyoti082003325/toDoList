import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

def configure_styles():
    # Create style object
    style = ttk.Style()
    
    # Modern color palette
    colors = {
        "primary": "#4f46e5",       # Indigo
        "primary_light": "#818cf8", # Lighter indigo
        "secondary": "#f43f5e",     # Rose
        "background": "#f8fafc",    # Lightest slate
        "surface": "#ffffff",      # White
        "text": "#1e293b",          # Slate 800
        "text_secondary": "#64748b", # Slate 500
        "border": "#e2e8f0",        # Slate 200
        "success": "#10b981",       # Emerald
        "warning": "#f59e0b",       # Amber
        "error": "#ef4444"          # Red
    }
    
    # Configure root window background
    style.configure(
        ".",
        background=colors["background"],
        foreground=colors["text"],
        bordercolor=colors["border"],
        darkcolor=colors["background"],
        lightcolor=colors["background"],
        troughcolor=colors["border"]
    )
    
    # Configure fonts
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(family="Segoe UI", size=10)
    
    heading_font = ("Segoe UI", 12, "bold")
    title_font = ("Segoe UI", 16, "bold")
    
    # Frame styles
    style.configure(
        "TFrame",
        background=colors["background"]
    )
    
    style.configure(
        "Card.TFrame",
        background=colors["surface"],
        relief="flat",
        borderwidth=0,
        bordercolor=colors["border"],
        padding=10
    )
    
    # Label styles
    style.configure(
        "TLabel",
        background=colors["surface"],
        foreground=colors["text"],
        font=default_font,
        padding=5
    )
    
    style.configure(
        "Title.TLabel",
        font=title_font,
        foreground=colors["primary"]
    )
    
    style.configure(
        "Heading.TLabel",
        font=heading_font,
        foreground=colors["text"]
    )
    
    # Button styles
    style.configure(
        "TButton",
        font=default_font,
        foreground=colors["surface"],
        background=colors["primary"],
        borderwidth=0,
        focusthickness=0,
        focuscolor=colors["background"],
        padding=8,
        relief="flat"
    )
    
    style.map(
        "TButton",
        background=[
            ("active", colors["primary_light"]),
            ("disabled", colors["border"])
        ],
        foreground=[
            ("disabled", colors["text_secondary"])
        ]
    )
    
    style.configure(
        "Accent.TButton",
        background=colors["secondary"],
        foreground=colors["surface"]
    )
    
    style.map(
        "Accent.TButton",
        background=[
            ("active", "#f87171"),  # Lighter red
            ("disabled", colors["border"])
        ]
    )
    
    # Entry styles
    style.configure(
        "TEntry",
        font=default_font,
        foreground=colors["text"],
        fieldbackground=colors["surface"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        padding=8,
        relief="flat",
        insertcolor=colors["primary"]
    )
    
    style.map(
        "TEntry",
        bordercolor=[
            ("focus", colors["primary"]),
            ("hover", colors["primary_light"])
        ],
        lightcolor=[
            ("focus", colors["primary"]),
            ("hover", colors["primary_light"])
        ],
        darkcolor=[
            ("focus", colors["primary"]),
            ("hover", colors["primary_light"])
        ]
    )
    
    # Combobox styles
    style.configure(
        "TCombobox",
        font=default_font,
        foreground=colors["text"],
        fieldbackground=colors["surface"],
        background=colors["surface"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        padding=8,
        relief="flat",
        arrowsize=12
    )
    
    style.map(
        "TCombobox",
        bordercolor=[
            ("focus", colors["primary"]),
            ("hover", colors["primary_light"])
        ],
        lightcolor=[
            ("focus", colors["primary"]),
            ("hover", colors["primary_light"])
        ],
        darkcolor=[
            ("focus", colors["primary"]),
            ("hover", colors["primary_light"])
        ],
        fieldbackground=[("readonly", colors["surface"])],
        selectbackground=[("readonly", colors["surface"])],
        selectforeground=[("readonly", colors["text"])]
    )
    
    # Treeview styles
    style.configure(
        "Treeview",
        font=default_font,
        background=colors["surface"],
        foreground=colors["text"],
        fieldbackground=colors["surface"],
        bordercolor=colors["border"],
        relief="flat",
        rowheight=32
    )
    
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 9, "bold"),
        background=colors["surface"],
        foreground=colors["text_secondary"],
        relief="flat",
        padding=8
    )
    
    style.map(
        "Treeview",
        background=[
            ("selected", colors["primary"])
        ],
        foreground=[
            ("selected", colors["surface"])
        ]
    )
    
    # Scrollbar styles
    style.configure(
        "TScrollbar",
        background=colors["surface"],
        troughcolor=colors["background"],
        bordercolor=colors["background"],
        arrowcolor=colors["text_secondary"],
        relief="flat"
    )
    
    style.map(
        "TScrollbar",
        background=[
            ("active", colors["primary_light"])
        ]
    )
    
    # Radiobutton styles
    style.configure(
        "TRadiobutton",
        font=default_font,
        background=colors["background"],
        foreground=colors["text"],
        indicatorbackground=colors["surface"],
        indicatorcolor=colors["surface"],
        indicatordiameter=16,
        padding=5
    )
    
    style.map(
        "TRadiobutton",
        background=[
            ("active", colors["background"])
        ],
        foreground=[
            ("active", colors["text"])
        ],
        indicatorcolor=[
            ("selected", colors["primary"]),
            ("!selected", colors["border"])
        ]
    )
    
    # Checkbutton styles
    style.configure(
        "TCheckbutton",
        font=default_font,
        background=colors["background"],
        foreground=colors["text"],
        indicatorbackground=colors["surface"],
        indicatorcolor=colors["surface"],
        indicatordiameter=16,
        padding=5
    )
    
    style.map(
        "TCheckbutton",
        background=[
            ("active", colors["background"])
        ],
        foreground=[
            ("active", colors["text"])
        ],
        indicatorcolor=[
            ("selected", colors["primary"]),
            ("!selected", colors["border"])
        ]
    )
    
    # Notebook styles
    style.configure(
        "TNotebook",
        background=colors["background"],
        bordercolor=colors["border"],
        tabmargins=(2, 2, 2, 0)
    )
    
    style.configure(
        "TNotebook.Tab",
        font=default_font,
        background=colors["background"],
        foreground=colors["text_secondary"],
        bordercolor=colors["border"],
        padding=(12, 6),
        relief="flat"
    )
    
    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", colors["surface"]),
            ("active", colors["background"])
        ],
        foreground=[
            ("selected", colors["primary"]),
            ("active", colors["text"])
        ],
        bordercolor=[
            ("selected", colors["border"])
        ]
    )