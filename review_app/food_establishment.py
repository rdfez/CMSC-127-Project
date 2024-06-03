import mariadb
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog

# Format a given item to be outputted 
def format_item(item):
    return (
        f"==============================\n"
        f"Establishment ID: {item[0]}\n"
        f"Establishment Name: {item[1]}\n"
        f"Establishment Rating: {item[2]}\n"
        f"Location: {item[3]}\n"
        f"Manager ID: {item[4]}\n"
        f"==============================\n"
    )

# View food establishments
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. choice (int): input to determine if all food establishments are fetched or highly rated food establishments
#   3. text_widget
def view_estab(cur, choice, text_widget):
    # View all food establishments
    if choice == 1:
        cur.execute("SELECT * FROM food_establishment")

    #View all highly rated food establishments (rating >= 4)
    elif choice == 2:
        cur.execute("SELECT * FROM food_establishment WHERE establishment_rating >= 4")

    results = cur.fetchall()
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, f"Number of establishments found: {len(results)}\n")

    if results:
        for row in results:
            text_widget.insert(tk.END, format_item(row))
    else:
        text_widget.insert(tk.END, "No establishments found for the given criteria.\n")

# Add a food establishment
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. Details when adding new food establishment
#       2.1. estab_id (int): 
#       2.2. estab_name (string):
#       2.3. loc (string):
#       2.4. estab_manager_id (int):
#   3. text_widget
def add_estab(cur, estab_id, estab_name, loc, estab_manager_id, text_widget):
    text_widget.delete(1.0, tk.END)
    try:
        cur.execute("SELECT * FROM user WHERE user_id = ? AND is_manager = 1", (estab_manager_id,))
        manager_exists = cur.fetchone()

        if not manager_exists:
            text_widget.insert(tk.END, "Error: Manager ID does not exist.\n")
            return
        
        cur.execute('''
            INSERT INTO food_establishment (establishment_id, establishment_name, establishment_rating, location, manager_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (estab_id, estab_name, None, loc, estab_manager_id))

        cur.execute('SELECT * FROM food_establishment WHERE establishment_id = ?', (estab_id,))
        item = cur.fetchone()
        text_widget.insert(tk.END, format_item(item))
        text_widget.insert(tk.END, "Establishment added successfully.\n")
        
        
    except mariadb.Error as e:
        text_widget.insert(tk.END, f"\nError: {e}\n")

# Update a food establishment
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. id (int): inputtted establishment_id to be updated from 
#   3. text_widget
def edit_estab(cur, id, text_widget):
    cur.execute('''
        SELECT * FROM food_establishment WHERE establishment_id = ?
    ''', (id,))
    item = cur.fetchone()
    text_widget.delete(1.0, tk.END)

    if item:
        text_widget.insert(tk.END, format_item(item))
        new_est_name = simpledialog.askstring("Input", "Insert new establishment name:")
        new_est_rating = simpledialog.askstring("Input", "Insert new rating here (1-5):")
        new_loc = simpledialog.askstring("Input", "Insert new location here:")
        cur.execute('''
            UPDATE food_establishment 
            SET establishment_name = ?, establishment_rating = ?, location = ?
            WHERE establishment_id = ?
        ''', (new_est_name, new_est_rating, new_loc, id))

        cur.execute('SELECT * FROM food_establishment WHERE establishment_id = ?', (id,))
        updated_item = cur.fetchone()
        text_widget.insert(tk.END, format_item(updated_item))
        text_widget.insert(tk.END, "\nEstablishment updated successfully.\n")
        
    else:
        text_widget.insert(tk.END, "\nEstablishment not found.\n")

# Delete a food establishment
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. id (int): inputted establishment_id to be deleted from food establishment
#   3. text_widget
def delete_estab(cur, id, text_widget):
    text_widget.delete(1.0, tk.END)
    cur.execute('''
        SELECT * FROM food_establishment WHERE establishment_id = ?
    ''', (id,))
    result = cur.fetchone()
    if result:
        text_widget.insert(tk.END, "\nAre you sure you want to delete:")
        text_widget.insert(tk.END, format_item(result))
        choice = simpledialog.askstring("Input", "Choice (Y/N):").upper()

        if choice == 'Y':
        # Check if there are associated food items
            cur.execute("SELECT * FROM food_item WHERE establishment_id = ?", (id,))
            associated_items = cur.fetchall()
            if associated_items:
                # Display error message if there are associated items
                text_widget.insert(tk.END, "Unable to delete establishment. It has associated food items.\n")
            else:
                # No associated items, proceed with deletion
                cur.execute('''
                    DELETE FROM food_establishment WHERE establishment_id = ?
                ''', (id,))
                text_widget.insert(tk.END, format_item(result)+"\n")
                text_widget.insert(tk.END, "Establishment deleted successfully.\n")
        elif choice == 'N':
                text_widget.insert(tk.END, "\nEstablishment deletion unsuccesful.\n")
        else:
            text_widget.insert(tk.END, "\nOption not Allowed.\n")


    else:
        text_widget.insert(tk.END, "Establishment not found.\n")

# Search a food establishment
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. id (int): inputted establishment_id to search for a food establishment
#   3. text_widget
def search_estab(cur, id, text_widget):
    cur.execute('''
        SELECT * FROM food_establishment WHERE establishment_id = ?
    ''', (id,))
    result = cur.fetchone()
    text_widget.delete(1.0, tk.END)

    if result:
        text_widget.insert(tk.END, format_item(result))
    else:
        text_widget.insert(tk.END, "\nEstablishment not found.\n")

# Main food establishments menu
def estab_menu(cur):
    def view_all():
        view_estab(cur, 1, text_widget)

    def view_high_rated():
        view_estab(cur, 2, text_widget)

    def add_estab_ui():
        try:
            estab_id = int(simpledialog.askstring("Input", "Input Establishment ID:"))

            cur.execute("SELECT * FROM food_establishment WHERE establishment_id = ?", (estab_id,))
            existing_estab = cur.fetchone()

            if existing_estab:
                messagebox.showerror("Error", "Establishment ID is already in use. Please choose a different ID." )
            else:
                estab_name = simpledialog.askstring("Input", "Input desired Establishment name:")
                loc = simpledialog.askstring("Input", "Input Establishment Location:")
                estab_manager_id = int(simpledialog.askstring("Input", "Input Manager ID of Establishment:"))
                add_estab(cur, estab_id, estab_name, loc, estab_manager_id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

    def edit_estab_ui():
        try:
            id = int(simpledialog.askstring("Input", "Please enter the ID of the establishment you want to edit:"))
            edit_estab(cur, id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid ID.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

    def delete_estab_ui():
        view_all()
        try:
            id = int(simpledialog.askstring("Input", "Insert the ID of the establishment to be deleted:"))
            delete_estab(cur, id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid ID.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

    def search_estab_ui():
        try:
            id = int(simpledialog.askstring("Input", "Insert the ID of the establishment to be searched:"))
            search_estab(cur, id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid ID.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

    estab_window = tk.Toplevel()
    estab_window.title("Food Establishments")

    ttk.Label(estab_window, text="Food Establishments Menu", font=("Arial", 16)).pack(pady=10)

    ttk.Button(estab_window, text="View all food establishments", command=view_all).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(estab_window, text="View Highest-rated Food establishments", command=view_high_rated).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(estab_window, text="Add a food establishment", command=add_estab_ui).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(estab_window, text="Update a food establishment", command=edit_estab_ui).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(estab_window, text="Delete a food establishment", command=delete_estab_ui).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(estab_window, text="Search a food establishment", command=search_estab_ui).pack(fill=tk.X, padx=20, pady=5)

    text_widget = tk.Text(estab_window, wrap=tk.WORD, height=10)
    text_widget.pack(fill=tk.BOTH, padx=20, pady=10)

    ttk.Button(estab_window, text="Close", command=estab_window.destroy).pack(pady=10)
