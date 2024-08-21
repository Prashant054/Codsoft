import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


# Database setup
def setup_database():
    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Add a task to the database
def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect('todo_list.db')
        c = conn.cursor()
        c.execute('INSERT INTO tasks (task, status) VALUES (?, ?)', (task, 'Pending'))
        conn.commit()
        conn.close()
        task_entry.delete(0, tk.END)
        update_task_list()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty")


# Update the task status
def update_task_status(task_id, status):
    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()
    update_task_list()


# Delete a task from the database
def delete_task(task_id):
    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    update_task_list()


# Update the task list in the GUI
def update_task_list():
    for widget in task_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('todo_list.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()

    for task in tasks:
        task_id, task_name, status = task
        task_row = tk.Frame(task_frame, padx=10, pady=5, bg='#f4f4f4')
        task_row.pack(fill=tk.X, pady=2)

        task_label = tk.Label(task_row, text=task_name, bg='#f4f4f4', width=50, anchor='w', font=('Arial', 12))
        task_label.pack(side=tk.LEFT, fill=tk.X, padx=(0, 10))

        status_label = tk.Label(task_row, text=status, bg='#f4f4f4', width=10, anchor='w', font=('Arial', 12))
        status_label.pack(side=tk.LEFT, fill=tk.X, padx=(0, 10))

        complete_button = tk.Button(task_row, text="Complete",
                                    command=lambda id=task_id: update_task_status(id, 'Completed'), width=10)
        complete_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(task_row, text="Delete", command=lambda id=task_id: delete_task(id), width=10,
                                  bg='red', fg='white')
        delete_button.pack(side=tk.LEFT, padx=5)


# GUI setup
def setup_gui():
    global task_entry
    global task_frame

    root = tk.Tk()
    root.title("To-Do List Application")
    root.geometry("800x400")
    root.configure(bg='#e1e1e1')

    # Title Label
    title_label = tk.Label(root, text="To-Do List", bg='#e1e1e1', font=('Arial', 18, 'bold'))
    title_label.pack(pady=10)

    # Entry Frame
    entry_frame = tk.Frame(root, bg='#e1e1e1')
    entry_frame.pack(pady=10)

    task_entry = tk.Entry(entry_frame, width=50, font=('Arial', 12))
    task_entry.pack(side=tk.LEFT, padx=5, pady=5)

    add_button = tk.Button(entry_frame, text="Add Task", command=add_task, font=('Arial', 12), bg='#4CAF50', fg='white')
    add_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Task Frame
    task_frame = tk.Frame(root, bg='#e1e1e1')
    task_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    update_task_list()

    root.mainloop()


if __name__ == '__main__':
    setup_database()
    setup_gui()
