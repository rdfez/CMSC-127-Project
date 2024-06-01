import mariadb
import tkinter as tk
from tkinter import messagebox, simpledialog

def format_item(item):
    return (
        f"==============================\n"
        f"Item ID: {item[0]}\n"
        f"Food Name: {item[1]}\n"
        f"Price: {item[2]}\n"
        f"Type: {item[3]}\n"
        f"Establishment ID: {item[4]}\n"
        f"Manager ID: {item[5]}\n"
        f"==============================\n"
    )

def view_items(cur, establishment_id, food_type, sort, text_widget):
    if food_type == 'NA':
        cur.execute("SELECT * FROM food_item WHERE establishment_id = ? ORDER BY price " + sort, (establishment_id,))
    else:
        cur.execute("SELECT * FROM food_item WHERE establishment_id = ? AND type = ? ORDER BY price " + sort, (establishment_id, food_type))

    items = cur.fetchall()
    text_widget.delete(1.0, tk.END)
    
    if items:
        text_widget.insert(tk.END, "Food Items:\n")
        for item in items:
            text_widget.insert(tk.END, format_item(item))
    else:
        text_widget.insert(tk.END, "No food items found for this establishment.\n")

def search_item_establishment(cur, choice, price_min, price_max, food_type, text_widget):
    if choice == 1:
        cur.execute("SELECT * FROM food_item WHERE price >= ? AND price <= ?", (price_min, price_max))
    elif choice == 2:
        cur.execute("SELECT * FROM food_item WHERE type = ?", (food_type,))
    elif choice == 3:
        cur.execute("SELECT * FROM food_item WHERE type = ? AND price >= ? AND price <= ?", (food_type, price_min, price_max))

    items = cur.fetchall()
    text_widget.delete(1.0, tk.END)

    if items:
        text_widget.insert(tk.END, "Food Items:\n")
        for item in items:
            text_widget.insert(tk.END, format_item(item))
    else:
        text_widget.insert(tk.END, "No food items found for this establishment.\n")

def add_item(cur, food_item_id, food_name, food_price, food_type, food_establishment_id, food_manager_id, text_widget):
    try:
        cur.execute("INSERT INTO food_item (item_id, food_name, price, type, establishment_id, manager_id) VALUES (?, ?, ?, ?, ?, ?)", 
                    (food_item_id, food_name, food_price, food_type, food_establishment_id, food_manager_id))
        text_widget.insert(tk.END, "Food item added successfully.\n")
    except mariadb.Error as e:
        text_widget.insert(tk.END, f"Error: {e}\n")

def update_item(cur, item_id, new_name, new_price, new_type, text_widget):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    text_widget.delete(1.0, tk.END)

    if item:
        cur.execute("UPDATE food_item SET food_name = ?, price = ?, type = ? WHERE item_id = ?", 
                    (new_name, new_price, new_type, item_id))
        text_widget.insert(tk.END, "Food item updated successfully.\n")
    else:
        text_widget.insert(tk.END, "Food item not found.\n")

def delete_item(cur, item_id, text_widget):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    text_widget.delete(1.0, tk.END)

    if item:
        cur.execute("DELETE FROM food_item WHERE item_id = ?", (item_id,))
        text_widget.insert(tk.END, "Food item deleted successfully.\n")
    else:
        text_widget.insert(tk.END, "Food item not found.\n")

def search_item(cur, item_id, text_widget):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    text_widget.delete(1.0, tk.END)

    if item:
        text_widget.insert(tk.END, format_item(item))
    else:
        text_widget.insert(tk.END, "Food item not found.\n")

def item_menu(cur):
    def view_all_ui():
        try:
            establishment_id = int(simpledialog.askstring("Input", "Enter Establishment ID:"))
            food_type = simpledialog.askstring("Input", "Enter Filter [MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]:")
            food_type = food_type.upper()
            sort = simpledialog.askstring("Input", "Enter Sort Price [DESC/ASC]:")
            sort = sort.upper()
            view_items(cur, establishment_id, food_type, sort, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")

    def search_item_establishment_ui():
        try:
            choice = int(simpledialog.askstring("Input", "Enter Filter Choice [1: Price Range, 2: Food Type, 3: Both]:"))
            price_min, price_max, food_type = None, None, None
            if choice == 1 or choice == 3:
                price_min = int(simpledialog.askstring("Input", "Enter Price Range Minimum:"))
                price_max = int(simpledialog.askstring("Input", "Enter Price Range Maximum:"))
            if choice == 2 or choice == 3:
                food_type = simpledialog.askstring("Input", "Enter Food Type [MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]:")
                food_type = food_type.upper()
            search_item_establishment(cur, choice, price_min, price_max, food_type, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")

    def add_item_ui():
        try:
            food_item_id = int(simpledialog.askstring("Input", "Enter Item ID:"))
            
            # Check if item ID already exists
            cur.execute("SELECT * FROM food_item WHERE item_id = ?", (food_item_id,))
            existing_item = cur.fetchone()

            if existing_item:
                messagebox.showerror("Error", "Item ID already exists. Please choose a different ID.")
            else:
                # Proceed to ask for other details
                food_name = simpledialog.askstring("Input", "Enter Food Name:")
                food_price = int(simpledialog.askstring("Input", "Enter Price:"))
                food_type = simpledialog.askstring("Input", "Enter Type [MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]:")
                food_establishment_id = int(simpledialog.askstring("Input", "Enter Establishment ID:"))
                food_manager_id = int(simpledialog.askstring("Input", "Enter Manager ID:"))
                add_item(cur, food_item_id, food_name, food_price, food_type, food_establishment_id, food_manager_id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")
            
    def update_item_ui():
        try:
            item_id = int(simpledialog.askstring("Input", "Enter Item ID:"))
            new_name = simpledialog.askstring("Input", "Updated Name:")
            new_price = int(simpledialog.askstring("Input", "Updated Price:"))
            new_type = simpledialog.askstring("Input", "Updated Type:")
            update_item(cur, item_id, new_name, new_price, new_type, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")

    def delete_item_ui():
        try:
            item_id = int(simpledialog.askstring("Input", "Enter Item ID:"))
            delete_item(cur, item_id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")

    def search_item_ui():
        try:
            item_id = int(simpledialog.askstring("Input", "Enter Item ID:"))
            search_item(cur, item_id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")

    item_window = tk.Toplevel()
    item_window.title("Food Items")

    tk.Label(item_window, text="Food Items Menu", font=("Arial", 16)).pack(pady=10)

    tk.Button(item_window, text="View all food items from a food establishment", command=view_all_ui).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(item_window, text="Search item from any establishment", command=search_item_establishment_ui).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(item_window, text="Add a food item", command=add_item_ui).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(item_window, text="Update a food item", command=update_item_ui).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(item_window, text="Delete a food item", command=delete_item_ui).pack(fill=tk.X, padx=20, pady=5)
    tk.Button(item_window, text="Search a food item", command=search_item_ui).pack(fill=tk.X, padx=20, pady=5)

    text_widget = tk.Text(item_window, wrap=tk.WORD, height=10)
    text_widget.pack(fill=tk.BOTH, padx=20, pady=10)

    tk.Button(item_window, text="Close", command=item_window.destroy).pack(pady=10)