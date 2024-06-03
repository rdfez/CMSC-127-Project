import mariadb
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog

# Format a given item to be outputted 
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

# View food items
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. establishment_id (int): input for establishment_id
#   3. food_type
#   4. sort
#   5. text_widget
def view_items(cur, establishment_id, food_type, sort, text_widget):
    food_types = {'MEAT', 'VEG', 'PASTA', 'BEVERAGE', 'DESSERT', 'NULL'}
    if food_type == 'NA':
        cur.execute("SELECT * FROM food_item WHERE establishment_id = ? ORDER BY price " + sort, (establishment_id,))
    elif (food_type not in food_types) and (sort == 'ASC' or sort == 'DESC'):
        cur.execute("SELECT * FROM food_item WHERE establishment_id = ? AND type = ? ORDER BY price " + sort, (establishment_id, food_type))
    else: 
        text_widget.insert(tk.END, "\nInvalid Input.\n")
        return

    items = cur.fetchall()
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, f"Number of food items found: {len(items)}\n")
    
    if items:
        text_widget.insert(tk.END, "Food Items:\n")
        for item in items:
            text_widget.insert(tk.END, format_item(item))
    else:
        text_widget.insert(tk.END, "\nNo food items found for this establishment.\n")

# Searches for an item from any establishment based on filter/sort
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. choice (int): determines the filter (minimum & maximum price) / sort (DESC/ASC)
#       2.1. price_min (int)
#       2.2. price_max (int)
#       3.3. food_type (string)
#   3. text_widget
def search_item_establishment(cur, choice, price_min, price_max, food_type, text_widget):
    food_types = {'MEAT', 'VEG', 'PASTA', 'BEVERAGE', 'DESSERT', 'NA'}

    if food_type:
        if food_type not in food_types:
            text_widget.insert(tk.END, "\nInvalid Food Type.\n")
            return

    if choice == 1:
        cur.execute("SELECT * FROM food_item WHERE price >= ? AND price <= ?", (price_min, price_max))
    elif choice == 2:
        if food_type == 'NA':
            cur.execute("SELECT * FROM food_item")
        else:
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
        text_widget.insert(tk.END, "\nNo food items found for this establishment.\n")

# Add a food item
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. Details when adding new item
#       2.1. food_item_id
#       2.2. food_name
#       2.3. food_price
#       2.4. food_type
#       2.5. food_establishment_id
#       2.6. food_manager_id
#   3. text_widget
def add_item(cur, food_item_id, food_name, food_price, food_type, food_establishment_id, food_manager_id, text_widget):
    text_widget.delete(1.0, tk.END)

    try:
        cur.execute("INSERT INTO food_item (item_id, food_name, price, type, establishment_id, manager_id) VALUES (?, ?, ?, ?, ?, ?)", 
                    (food_item_id, food_name, food_price, food_type, food_establishment_id, food_manager_id))

        cur.execute('SELECT * FROM food_item WHERE item_id = ?', (food_item_id,))
        item = cur.fetchone()
        text_widget.insert(tk.END, format_item(item))
        text_widget.insert(tk.END, "Food item added successfully.\n")

    except mariadb.Error as e:
        text_widget.insert(tk.END, f"Error: {e}\n")

# Update a food item
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. item_id (int): inputted item_id to be updated from food item
#   3. text_widget
def update_item(cur, item_id, text_widget):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    text_widget.delete(1.0, tk.END)

    if item:
        text_widget.insert(tk.END, format_item(item))
        new_name = simpledialog.askstring("Input", "Updated Name:")
        new_price = int(simpledialog.askstring("Input", "Updated Price:"))
        food_types = ["MEAT", "VEG", "PASTA", "BEVERAGE", "DESSERT"]
        new_type = None
        while new_type not in food_types:
            new_type = simpledialog.askstring("Input", f"Update Type:").upper()
            if new_type not in food_types:
                messagebox.showerror("Error", f"Invalid type. Please enter one of the following: {food_types}")
                

        cur.execute("UPDATE food_item SET food_name = ?, price = ?, type = ? WHERE item_id = ?", 
                    (new_name, new_price, new_type, item_id))
        
        cur.execute('SELECT * FROM food_item WHERE item_id = ?', (item_id,))
        updated_item = cur.fetchone()
        text_widget.insert(tk.END, format_item(updated_item))
        text_widget.insert(tk.END, "\nFood item updated successfully.\n")
    else:
        text_widget.insert(tk.END, "\nFood item not found.\n")

# Delete a food item
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. item_id (int): inputted item_id to be deleted from food item
#   3. text_widget
def delete_item(cur, item_id, text_widget):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    text_widget.delete(1.0, tk.END)

    if item:
        text_widget.insert(tk.END, "\nAre you sure you want to delete:")
        text_widget.insert(tk.END, format_item(item))
        choice = simpledialog.askstring("Input", "Choice (Y/N):").upper()

        if choice == 'Y':
            cur.execute("DELETE FROM food_item WHERE item_id = ?", (item_id,))
            text_widget.insert(tk.END, "\nFood item deleted successfully.\n")
        elif choice == 'N': 
        
            text_widget.insert(tk.END, "\nFood item deletion unsuccesful.\n")
        else:
            text_widget.insert(tk.END, "\nOption not Allowed.\n")

    else:
        text_widget.insert(tk.END, "\nFood item not found.\n")

#Search for a food item based on item ID
# - Parameters:
#   1. cursor (cursor): mariaDB cursor 
#   2. item_id (int): inputted item_id to search for a food item
#   3. text_widget
def search_item(cur, item_id, text_widget):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    text_widget.delete(1.0, tk.END)

    if item:
        text_widget.insert(tk.END, format_item(item))
    else:
        text_widget.insert(tk.END, "\nFood item not found.\n")

# Main food item menu
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
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")


    def search_item_establishment_ui():
        try:
            choice = int(simpledialog.askstring("Input", "Enter Filter Choice [1: Price Range, 2: Food Type, 3: Both]:"))
            price_min, price_max, food_type = None, None, None
            if choice == 1 or choice == 3:
                price_min = int(simpledialog.askstring("Input", "Enter Price Range Minimum:"))
                price_max = int(simpledialog.askstring("Input", "Enter Price Range Maximum:"))
            if choice == 2 or choice == 3:
                food_type = simpledialog.askstring("Input", "Enter Food Type [MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]:").upper()

            search_item_establishment(cur, choice, price_min, price_max, food_type, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

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
                
                # Use a dropdown menu for food type
                food_types = ["MEAT", "VEG", "PASTA", "BEVERAGE", "DESSERT"]
                food_type = None
                while food_type not in food_types:
                    food_type = simpledialog.askstring("Input", f"Enter Type {food_types}:").upper()
                    if food_type not in food_types:
                        messagebox.showerror("Error", f"Invalid type. Please enter one of the following: {food_types}")
                
                food_establishment_id = int(simpledialog.askstring("Input", "Enter Establishment ID:"))
                food_manager_id = int(simpledialog.askstring("Input", "Enter Manager ID:"))
                add_item(cur, food_item_id, food_name, food_price, food_type, food_establishment_id, food_manager_id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

    def update_item_ui():
        try:
            item_id = int(simpledialog.askstring("Input", "Enter Item ID:"))
            update_item(cur, item_id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

    def delete_item_ui():
        try:
            item_id = int(simpledialog.askstring("Input", "Enter Item ID:"))
            delete_item(cur, item_id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

    def search_item_ui():
        try:
            item_id = int(simpledialog.askstring("Input", "Enter Item ID:"))
            search_item(cur, item_id, text_widget)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")
        except TypeError:
            messagebox.showinfo("Info", "Transaction cancelled.")

    item_window = tk.Toplevel()
    item_window.title("Food Items")

    ttk.Label(item_window, text="Food Items Menu", font=("Arial", 16)).pack(pady=10)

    ttk.Button(item_window, text="View all food items from a food establishment", command=view_all_ui).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(item_window, text="Search item from any establishment", command=search_item_establishment_ui).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(item_window, text="Add a food item", command=add_item_ui).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(item_window, text="Update a food item", command=update_item_ui).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(item_window, text="Delete a food item", command=delete_item_ui).pack(fill=tk.X, padx=20, pady=5)
    ttk.Button(item_window, text="Search a food item", command=search_item_ui).pack(fill=tk.X, padx=20, pady=5)

    text_widget = tk.Text(item_window, wrap=tk.WORD, height=10)
    text_widget.pack(fill=tk.BOTH, padx=20, pady=10)

    ttk.Button(item_window, text="Close", command=item_window.destroy).pack(pady=10)