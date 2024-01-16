import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('partners.db')
c = conn.cursor()

c.execute('''
        CREATE TABLE IF NOT EXISTS partners (
                id INTEGER PRIMARY KEY,
                name TEXT,
                organization_type TEXT,
                resources_available TEXT,
                contact_name TEXT,
                contact_email TEXT,
                contact_phone TEXT
        )
''')

def add_partner():
    name = name_entry.get()
    organization_type = org_type_entry.get()
    resources_available = resources_entry.get()
    contact_name = contact_name_entry.get()
    contact_email = contact_email_entry.get()
    contact_phone = contact_phone_entry.get()

    c.execute('''
            INSERT INTO partners (name, organization_type, resources_available, contact_name, contact_email, contact_phone)
            VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, organization_type, resources_available, contact_name, contact_email, contact_phone))

    conn.commit()
    messagebox.showinfo("Success", "Partner added successfully!")

def search_partners():
    keyword = search_entry.get()
    c.execute('''
            SELECT * FROM partners
            WHERE name LIKE ? OR organization_type LIKE ? OR resources_available LIKE ? OR contact_name LIKE ?
    ''', ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))

    partners = c.fetchall()
    if partners:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        for partner in partners:
            result_text.insert(tk.END, f"{partner}\n")
        result_text.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("No Results", "No matching partners found.")

root = tk.Tk()
root.title("Partner Management System")
root.configure(bg='#2C3E50')

tk.Label(root, text="1. Name", bg='#2C3E50', fg='white').grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="2. Organization Type", bg='#2C3E50', fg='white').grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="3. Resources", bg='#2C3E50', fg='white').grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="4. Contact Name", bg='#2C3E50', fg='white').grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="5. Contact Email", bg='#2C3E50', fg='white').grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
tk.Label(root, text="6. Contact Phone", bg='#2C3E50', fg='white').grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

name_entry = tk.Entry(root, bg='#34495E', fg='white', insertbackground='white')
org_type_entry = tk.Entry(root, bg='#34495E', fg='white', insertbackground='white')
resources_entry = tk.Entry(root, bg='#34495E', fg='white', insertbackground='white')
contact_name_entry = tk.Entry(root, bg='#34495E', fg='white', insertbackground='white')
contact_email_entry = tk.Entry(root, bg='#34495E', fg='white', insertbackground='white')
contact_phone_entry = tk.Entry(root, bg='#34495E', fg='white', insertbackground='white')

search_entry = tk.Entry(root, bg='#34495E', fg='white', insertbackground='white')
result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED, bg='#34495E', fg='white')

name_entry.grid(row=0, column=1, padx=10, pady=5)
org_type_entry.grid(row=1, column=1, padx=10, pady=5)
resources_entry.grid(row=2, column=1, padx=10, pady=5)
contact_name_entry.grid(row=3, column=1, padx=10, pady=5)
contact_email_entry.grid(row=4, column=1, padx=10, pady=5)
contact_phone_entry.grid(row=5, column=1, padx=10, pady=5)

search_entry.grid(row=1, column=2, padx=10, pady=5)
result_text.grid(row=2, column=2, rowspan=4, padx=10, pady=5)

add_button = tk.Button(root, text="Add Partner", command=add_partner, bg='#3498DB', fg='white')
search_button = tk.Button(root, text="Search Partners", command=search_partners, bg='#3498DB', fg='white')
exit_button = tk.Button(root, text="Exit", command=root.destroy, bg='#E74C3C', fg='white') 


add_button.grid(row=6, column=0, columnspan=2, pady=10)
search_button.grid(row=6, column=2, pady=10)
exit_button.grid(row=7, column=0, columnspan=3, pady=10)

root.mainloop()

conn.close()
