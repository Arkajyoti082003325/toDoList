import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Callable, Optional
from .todo_manager import Task, TodoManager

class TodoAppGUI:
    def __init__(self, root: tk.Tk, todo_manager: TodoManager):
        self.root = root
        self.todo_manager = todo_manager
        self.setup_window()
        self.create_widgets()
        self.refresh_task_list()

    def setup_window(self):
        self.root.title("To-Do List Application")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.title_label = ttk.Label(
            header_frame, 
            text="To-Do List", 
            font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(side="left")

        # Add task button
        add_button = ttk.Button(
            header_frame,
            text="+ Add Task",
            command=self.show_add_task_dialog
        )
        add_button.pack(side="right")

        # Task list
        self.task_list_frame = ttk.Frame(main_frame)
        self.task_list_frame.grid(row=1, column=0, sticky="nsew")
        self.task_list_frame.columnconfigure(0, weight=1)

        # Create treeview with scrollbar
        self.tree = ttk.Treeview(
            self.task_list_frame,
            columns=("title", "completed", "priority", "category", "due_date"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.tree.heading("title", text="Task")
        self.tree.heading("completed", text="Status")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("category", text="Category")
        self.tree.heading("due_date", text="Due Date")
        
        self.tree.column("title", width=200, anchor="w")
        self.tree.column("completed", width=80, anchor="center")
        self.tree.column("priority", width=80, anchor="center")
        self.tree.column("category", width=120, anchor="center")
        self.tree.column("due_date", width=120, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.task_list_frame,
            orient="vertical",
            command=self.tree.yview
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

        # Filter controls
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        ttk.Label(filter_frame, text="Filter:").pack(side="left")
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(
            filter_frame,
            text="All",
            variable=self.filter_var,
            value="all",
            command=self.refresh_task_list
        ).pack(side="left", padx=5)
        
        ttk.Radiobutton(
            filter_frame,
            text="Active",
            variable=self.filter_var,
            value="active",
            command=self.refresh_task_list
        ).pack(side="left", padx=5)
        
        ttk.Radiobutton(
            filter_frame,
            text="Completed",
            variable=self.filter_var,
            value="completed",
            command=self.refresh_task_list
        ).pack(side="left", padx=5)

    def refresh_task_list(self):
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get tasks based on filter
        filter_value = self.filter_var.get()
        if filter_value == "all":
            tasks = self.todo_manager.get_tasks()
        elif filter_value == "active":
            tasks = self.todo_manager.get_tasks(filter_completed=False)
        else:  # completed
            tasks = self.todo_manager.get_tasks(filter_completed=True)
        
        # Add tasks to treeview
        for task in tasks:
            status = "✓" if task.completed else " "
            priority = "★" * task.priority if task.priority else ""
            self.tree.insert(
                "", "end",
                values=(
                    task.title,
                    status,
                    priority,
                    task.category or "",
                    task.due_date or ""
                )
            )

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.task_menu.post(event.x_root, event.y_root)

    def get_selected_task_index(self) -> Optional[int]:
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
        task_index = self.get_selected_task_index()
        if task_index is not None:
            self.todo_manager.toggle_task_completion(task_index)
            self.refresh_task_list()

    def delete_selected_task(self):
        task_index = self.get_selected_task_index()
        if task_index is not None:
            if messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this task?"
            ):
                self.todo_manager.delete_task(task_index)
                self.refresh_task_list()

    def show_add_task_dialog(self):
        dialog = TaskDialog(
            self.root,
            title="Add New Task",
            on_submit=self.add_task
        )

    def show_edit_task_dialog(self):
        task_index = self.get_selected_task_index()
        if task_index is not None:
            task = self.todo_manager.get_tasks()[task_index]
            dialog = TaskDialog(
                self.root,
                title="Edit Task",
                task=task,
                on_submit=lambda **kwargs: self.update_task(task_index, **kwargs)
            )

    def add_task(self, title: str, **kwargs):
        self.todo_manager.add_task(title, **kwargs)
        self.refresh_task_list()

    def update_task(self, task_index: int, **kwargs):
        self.todo_manager.update_task(task_index, **kwargs)
        self.refresh_task_list()

class TaskDialog(tk.Toplevel):
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
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Task title
        ttk.Label(main_frame, text="Task Title:").grid(
            row=0, column=0, sticky="w", pady=(0, 5))
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Priority
        ttk.Label(main_frame, text="Priority:").grid(
            row=2, column=0, sticky="w", pady=(0, 5))
        self.priority_var = tk.IntVar(value=1)
        priority_frame = ttk.Frame(main_frame)
        priority_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 10))
        for i in range(1, 6):
            ttk.Radiobutton(
                priority_frame,
                text=str(i),
                variable=self.priority_var,
                value=i
            ).pack(side="left", padx=(0, 10))
        
        # Category
        ttk.Label(main_frame, text="Category:").grid(
            row=4, column=0, sticky="w", pady=(0, 5))
        self.category_entry = ttk.Entry(main_frame)
        self.category_entry.grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        # Due Date
        ttk.Label(main_frame, text="Due Date (YYYY-MM-DD):").grid(
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
            command=self.submit
        )
        submit_button.pack(side="right")

    def load_task_data(self):
        if self.task:
            self.title_entry.insert(0, self.task.title)
            self.priority_var.set(self.task.priority)
            if self.task.category:
                self.category_entry.insert(0, self.task.category)
            if self.task.due_date:
                self.due_date_entry.insert(0, self.task.due_date)

    def submit(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title cannot be empty")
            return
        
        data = {
            "title": title,
            "priority": self.priority_var.get(),
            "category": self.category_entry.get().strip() or None,
            "due_date": self.due_date_entry.get().strip() or None
        }
        
        if self.on_submit:
            self.on_submit(**data)
        
        self.destroy()