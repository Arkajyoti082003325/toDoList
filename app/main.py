import tkinter as tk
from app.todo_manager import TodoManager
from app.gui import TodoAppGUI

def main():
    # Initialize the root window
    root = tk.Tk()
    
    # Initialize the todo manager
    todo_manager = TodoManager()
    
    # Initialize the GUI
    app = TodoAppGUI(root, todo_manager)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()