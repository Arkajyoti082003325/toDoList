import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Callable, Optional
from datetime import datetime
from .todo_manager import Task, TodoManager
from .styles import configure_styles

class TodoAppGUI:
    def __init__(self, root: tk.Tk, todo_manager: TodoManager):
        self.root = root
        self.todo_manager = todo_manager
        configure_styles()
        self.setup_window()
        self.create_widgets()
        self.refresh_task_list()
        self.setup_menus()

    def setup_window(self):
        """Configure the main window settings"""
        self.root.title("To-Do List Application")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.configure(bg="#f8fafc")
        
        # Set window icon if available
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def setup_menus(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Task", command=self.show_add_task_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Edit Task", command=self.show_edit_task_dialog)
        edit_menu.add_command(label="Delete Task", command=self.delete_selected_task)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_radiobutton(label="All Tasks", variable=self.filter_var, value="all", command=self.refresh_task_list)
        view_menu.add_radiobutton(label="Active Only", variable=self.filter_var, value="active", command=self.refresh_task_list)
        view_menu.add_radiobutton(label="Completed Only", variable=self.filter_var, value="completed", command=self.refresh_task_list)
        menubar.add_cascade(label="View", menu=view_menu)
        
        self.root.config(menu=menubar)

    def create_widgets(self):
        """Create and arrange all widgets in the window"""
        # Main container with card-like appearance
        main_frame = ttk.Frame(self.root, style="Card.TFrame", padding=(25, 20))
        main_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header with app title and action buttons
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # App title
        self.title_label = ttk.Label(
            header_frame, 
            text="To-Do List", 
            style="Title.TLabel"
        )
        self.title_label.pack(side="left")

        # Action buttons container
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side="right")
        
        # Add Task button
        add_button = ttk.Button(
            button_frame,
            text="＋ Add Task",
            style="Accent.TButton",
            command=self.show_add_task_dialog
        )
        add_button.pack(side="left", padx=(0, 10))
        
        # Refresh button
        refresh_button = ttk.Button(
            button_frame,
            text="⟳ Refresh",
            command=self.refresh_task_list
        )
        refresh_button.pack(side="left")

        # Task list container
        self.task_list_frame = ttk.Frame(main_frame, style="Card.TFrame")
        self.task_list_frame.grid(row=1, column=0, sticky="nsew")
        self.task_list_frame.columnconfigure(0, weight=1)
        self.task_list_frame.rowconfigure(0, weight=1)

        # Create treeview with scrollbar
        self.tree = ttk.Treeview(
            self.task_list_frame,
            columns=("title", "completed", "priority", "category", "due_date"),
            show="headings",
            selectmode="browse",
            style="Treeview"
        )
        
        # Configure columns
        self.tree.heading("title", text="Task", anchor="w")
        self.tree.heading("completed", text="Status", anchor="center")
        self.tree.heading("priority", text="Priority", anchor="center")
        self.tree.heading("category", text="Category", anchor="center")
        self.tree.heading("due_date", text="Due Date", anchor="center")
        
        self.tree.column("title", width=300, anchor="w")
        self.tree.column("completed", width=100, anchor="center")
        self.tree.column("priority", width=120, anchor="center")
        self.tree.column("category", width=180, anchor="center")
        self.tree.column("due_date", width=150, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.task_list_frame,
            orient="vertical",
            command=self.tree.yview,
            style="TScrollbar"
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Context menu for tasks
        self.task_menu = tk.Menu(self.root, tearoff=0)
        self.task_menu.add_command(
            label="Mark Complete/Incomplete",
            command=self.toggle_selected_task
        )
        self.task_menu.add_command(
            label="Edit Task",
            command=self.show_edit_task_dialog
        )
        self.task_menu.add_command(
            label="Delete Task",
            command=self.delete_selected_task
        )

        # Bind right-click to show context menu
        self.tree.bind("<Button-3>", self.show_context_menu)
        # Bind double-click to toggle completion
        self.tree.bind("<Double-1>", lambda e: self.toggle_selected_task())
        # Bind keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.show_add_task_dialog())
        self.root.bind("<Delete>", lambda e: self.delete_selected_task())
        self.root.bind("<F5>", lambda e: self.refresh_task_list())

        # Filter controls
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        
        ttk.Label(filter_frame, text="Filter:", style="Heading.TLabel").pack(side="left")
        
        self.filter_var = tk.StringVar(value="all")
        
        ttk.Radiobutton(
            filter_frame,
            text="All Tasks",
            variable=self.filter_var,
            value="all",
            command=self.refresh_task_list
        ).pack(side="left", padx=10)
        
        ttk.Radiobutton(
            filter_frame,
            text="Active Only",
            variable=self.filter_var,
            value="active",
            command=self.refresh_task_list
        ).pack(side="left", padx=10)
        
        ttk.Radiobutton(
            filter_frame,
            text="Completed Only",
            variable=self.filter_var,
            value="completed",
            command=self.refresh_task_list
        ).pack(side="left", padx=10)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=(10, 5)
        )
        status_bar.grid(row=3, column=0, sticky="ew", pady=(20, 0))

    def refresh_task_list(self):
        """Refresh the task list display based on current filter"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get tasks based on filter
        filter_value = self.filter_var.get()
        if filter_value == "all":
            tasks = self.todo_manager.get_tasks()
            self.status_var.set(f"Showing all tasks - {len(tasks)} total")
        elif filter_value == "active":
            tasks = self.todo_manager.get_tasks(filter_completed=False)
            self.status_var.set(f"Showing active tasks - {len(tasks)} remaining")
        else:  # completed
            tasks = self.todo_manager.get_tasks(filter_completed=True)
            self.status_var.set(f"Showing completed tasks - {len(tasks)} done")
        
        # Add tasks to treeview with appropriate tags
        for task in tasks:
            status = "✓" if task.completed else "◯"
            priority = "★" * task.priority if task.priority else "☆"
            
            # Format due date if exists
            due_date = ""
            if task.due_date:
                try:
                    due_date_obj = datetime.fromisoformat(task.due_date)
                    due_date = due_date_obj.strftime("%b %d, %Y")
                    
                    # Highlight overdue tasks
                    if not task.completed and due_date_obj < datetime.now():
                        due_date += " (Overdue)"
                except:
                    due_date = task.due_date
            
            # Insert task with appropriate tags
            tags = ("completed" if task.completed else "active",)
            if task.priority and task.priority >= 4:
                tags += ("high-priority",)
            
            self.tree.insert(
                "", "end",
                values=(
                    task.title,
                    status,
                    priority,
                    task.category or "-",
                    due_date or "-"
                ),
                tags=tags
            )
        
        # Configure tag colors
        self.tree.tag_configure("completed", foreground="#64748b")
        self.tree.tag_configure("active", foreground="#1e293b")
        self.tree.tag_configure("high-priority", background="#fee2e2")

    def show_context_menu(self, event):
        """Show context menu for selected task"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.task_menu.post(event.x_root, event.y_root)

    def get_selected_task_index(self) -> Optional[int]:
        """Get the index of the currently selected task"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            item_index = self.tree.index(item)
            
            # Adjust for filter if needed
            filter_value = self.filter_var.get()
            if filter_value == "all":
                return item_index
            elif filter_value == "active":
                all_tasks = self.todo_manager.get_tasks(filter_completed=False)
                task = all_tasks[item_index]
                return self.todo_manager.get_tasks().index(task)
            else:  # completed
                all_tasks = self.todo_manager.get_tasks(filter_completed=True)
                task = all_tasks[item_index]
                return self.todo_manager.get_tasks().index(task)
        return None

    def toggle_selected_task(self):
        """Toggle completion status of selected task"""
        task_index = self.get_selected_task_index()
        if task_index is not None:
            self.todo_manager.toggle_task_completion(task_index)
            self.refresh_task_list()
            self.status_var.set("Task status updated")

    def delete_selected_task(self):
        """Delete the selected task after confirmation"""
        task_index = self.get_selected_task_index()
        if task_index is not None:
            task = self.todo_manager.get_tasks()[task_index]
            if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{task.title}'?",
                icon="warning"
            ):
                self.todo_manager.delete_task(task_index)
                self.refresh_task_list()
                self.status_var.set("Task deleted")

    def show_add_task_dialog(self):
        """Show dialog to add a new task"""
        dialog = TaskDialog(
            self.root,
            title="Add New Task",
            on_submit=self.add_task
        )

    def show_edit_task_dialog(self):
        """Show dialog to edit selected task"""
        task_index = self.get_selected_task_index()
        if task_index is not None:
            task = self.todo_manager.get_tasks()[task_index]
            dialog = TaskDialog(
                self.root,
                title="Edit Task",
                task=task,
                on_submit=lambda **kwargs: self.update_task(task_index, **kwargs)
            )
        else:
            messagebox.showwarning(
                "No Task Selected",
                "Please select a task to edit",
                parent=self.root
            )

    def add_task(self, title: str, **kwargs):
        """Add a new task to the list"""
        self.todo_manager.add_task(title, **kwargs)
        self.refresh_task_list()
        self.status_var.set("New task added")

    def update_task(self, task_index: int, **kwargs):
        """Update an existing task"""
        self.todo_manager.update_task(task_index, **kwargs)
        self.refresh_task_list()
        self.status_var.set("Task updated")

class TaskDialog(tk.Toplevel):
    """Dialog window for adding/editing tasks"""
    def __init__(
        self,
        parent,
        title: str,
        task: Optional[Task] = None,
        on_submit: Optional[Callable] = None
    ):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.grab_set()
        
        self.task = task
        self.on_submit = on_submit
        
        self.create_widgets()
        
        if task:
            self.load_task_data()
        
        self.bind("<Return>", lambda e: self.submit())
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        # Center the dialog
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def create_widgets(self):
        """Create widgets for the dialog"""
        main_frame = ttk.Frame(self, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        # Task title
        ttk.Label(main_frame, text="Task Title:", style="Heading.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 5))
        
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        self.title_entry.focus_set()
        
        # Priority
        ttk.Label(main_frame, text="Priority:", style="Heading.TLabel").grid(
            row=2, column=0, sticky="w", pady=(0, 5))
        
        self.priority_var = tk.IntVar(value=3)
        priority_frame = ttk.Frame(main_frame)
        priority_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        for i in range(1, 6):
            ttk.Radiobutton(
                priority_frame,
                text=str(i),
                variable=self.priority_var,
                value=i
            ).pack(side="left", padx=(0, 10))
        
        # Category
        ttk.Label(main_frame, text="Category:", style="Heading.TLabel").grid(
            row=4, column=0, sticky="w", pady=(0, 5))
        
        self.category_var = tk.StringVar()
        self.category_entry = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            values=["Work", "Personal", "Shopping", "Health", "Other"]
        )
        self.category_entry.grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Due Date
        ttk.Label(main_frame, text="Due Date (YYYY-MM-DD):", style="Heading.TLabel").grid(
            row=6, column=0, sticky="w", pady=(0, 5))
        
        self.due_date_entry = ttk.Entry(main_frame)
        self.due_date_entry.grid(
            row=7, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, sticky="e")
        
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy
        )
        cancel_button.pack(side="right", padx=(5, 0))
        
        submit_button = ttk.Button(
            button_frame,
            text="Submit",
            style="Accent.TButton",
            command=self.submit
        )
        submit_button.pack(side="right")

    def load_task_data(self):
        """Load task data into the form fields"""
        if self.task:
            self.title_entry.insert(0, self.task.title)
            self.priority_var.set(self.task.priority)
            if self.task.category:
                self.category_var.set(self.task.category)
            if self.task.due_date:
                self.due_date_entry.insert(0, self.task.due_date)

    def submit(self):
        """Submit the form data"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title cannot be empty", parent=self)
            return
        
        # Validate due date format
        due_date = self.due_date_entry.get().strip()
        if due_date:
            try:
                datetime.fromisoformat(due_date)
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Please enter date in YYYY-MM-DD format",
                    parent=self
                )
                return
        
        data = {
            "title": title,
            "priority": self.priority_var.get(),
            "category": self.category_var.get().strip() or None,
            "due_date": due_date or None
        }
        
        if self.on_submit:
            self.on_submit(**data)
        
        self.destroy()