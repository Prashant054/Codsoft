import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Database setup
def setup_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        email TEXT,
                        address TEXT
                    )''')
    conn.commit()
    conn.close()


# Add contact
def add_contact(name, phone, email, address):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
                   (name, phone, email, address))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Contact added successfully")
    view_contacts()


# View all contacts
def view_contacts():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts")
    contacts = cursor.fetchall()
    conn.close()

    # Clear the listbox
    contact_listbox.delete(*contact_listbox.get_children())

    # Insert new contacts
    for contact in contacts:
        contact_listbox.insert("", "end", values=(contact[0], contact[1], contact[2]))


# Search contact
def search_contact(query):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                   ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    conn.close()

    # Clear the listbox
    contact_listbox.delete(*contact_listbox.get_children())

    # Insert search results
    for contact in results:
        contact_listbox.insert("", "end", values=(contact[0], contact[1], contact[2]))


# Update contact
def update_contact(id, name, phone, email, address):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
                   (name, phone, email, address, id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Contact updated successfully")
    view_contacts()


# Delete contact
def delete_contact(id):
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Contact deleted successfully")
    view_contacts()


# Select contact to update or delete
def select_contact(event):
    selected_item = contact_listbox.selection()
    if selected_item:
        item = contact_listbox.item(selected_item)
        contact_id = item['values'][0]
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
        contact = cursor.fetchone()
        conn.close()

        # Fill the form with the selected contact details
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)

        name_entry.insert(0, contact[1])
        phone_entry.insert(0, contact[2])
        email_entry.insert(0, contact[3])
        address_entry.insert(0, contact[4])

        # Update the current contact ID for updating
        global current_contact_id
        current_contact_id = contact_id


# Main window setup
def main_window():
    global contact_listbox, name_entry, phone_entry, email_entry, address_entry, current_contact_id

    root = tk.Tk()
    root.title("Contact Book")
    root.geometry("600x400")

    # Styles
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", padding=6, relief="flat", background="#ccc")
    style.configure("Treeview", rowheight=25)

    # Frames
    form_frame = ttk.Frame(root, padding="10")
    form_frame.pack(side=tk.TOP, fill=tk.X)

    list_frame = ttk.Frame(root, padding="10")
    list_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Form fields
    ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(form_frame, width=30)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
    phone_entry = ttk.Entry(form_frame, width=30)
    phone_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    email_entry = ttk.Entry(form_frame, width=30)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Address:").grid(row=3, column=0, padx=5, pady=5)
    address_entry = ttk.Entry(form_frame, width=30)
    address_entry.grid(row=3, column=1, padx=5, pady=5)

    # Buttons
    ttk.Button(form_frame, text="Add Contact",
               command=lambda: add_contact(name_entry.get(), phone_entry.get(), email_entry.get(),
                                           address_entry.get())).grid(row=4, column=0, padx=5, pady=10)
    ttk.Button(form_frame, text="Update Contact",
               command=lambda: update_contact(current_contact_id, name_entry.get(), phone_entry.get(),
                                              email_entry.get(), address_entry.get())).grid(row=4, column=1, padx=5,
                                                                                            pady=10)
    ttk.Button(form_frame, text="Delete Contact", command=lambda: delete_contact(current_contact_id)).grid(row=4,
                                                                                                           column=2,
                                                                                                           padx=5,
                                                                                                           pady=10)

    # Contact Listbox
    contact_listbox = ttk.Treeview(list_frame, columns=("ID", "Name", "Phone"), show='headings')
    contact_listbox.heading("ID", text="ID")
    contact_listbox.heading("Name", text="Name")
    contact_listbox.heading("Phone", text="Phone")
    contact_listbox.pack(fill=tk.BOTH, expand=True)

    contact_listbox.bind("<ButtonRelease-1>", select_contact)

    # Search Bar
    search_frame = ttk.Frame(list_frame)
    search_frame.pack(fill=tk.X)

    search_entry = ttk.Entry(search_frame, width=50)
    search_entry.pack(side=tk.LEFT, padx=10, pady=10)

    ttk.Button(search_frame, text="Search", command=lambda: search_contact(search_entry.get())).pack(side=tk.LEFT,
                                                                                                     padx=10, pady=10)

    # Initial data load
    view_contacts()

    root.mainloop()


if __name__ == "__main__":
    setup_db()
    current_contact_id = None  # To track the currently selected contact for updates
    main_window()
