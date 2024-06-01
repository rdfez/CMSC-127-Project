from misc import count, get_id, get_input, validate_id
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import mariadb
import tkinter.messagebox as tkMessageBox

def show_message(message):
    messagebox.showinfo("Information", message)

# Helper function to get user input through a dialog
def get_user_input(prompt, input_type="string", min_val=None, max_val=None, options=None):
    if input_type == "int":
        value = simpledialog.askinteger("Input", prompt, minvalue=min_val, maxvalue=max_val)
        if value is None:
            tkMessageBox.showinfo("Information", "Transaction cancelled")
            return value
        else:
            return value
    elif input_type == "date":
        value = simpledialog.askstring("Input", prompt)
        if value is None:
            tkMessageBox.showinfo("Information", "Transaction cancelled")
            return value
        else:
            return value
    elif input_type == "bool":
        value = messagebox.askyesno("Input", prompt)
        if value is None:
            tkMessageBox.showinfo("Information", "Transaction cancelled")
            return value
        else:
            return value
    else:
        value = simpledialog.askstring("Input", prompt)
        if value is None:
            tkMessageBox.showinfo("Information", "Transaction cancelled")
            return value
        else:
            return value
        
# Add a review
def add_review(cur):
    # Get total number of establishments
    establishment_total = count(cur, "food_establishment", False)
    # Get total number of items
    item_total = count(cur, "food_item", False)

    # Halt if there are no entities (both establishment and item)
    if(not(establishment_total > 0) and not(item_total > 0)):
        show_message("There are no food establishments or food items!")
        return

    # Add menu
    type_input = get_user_input("Please select one you would like to create a review for:\n[1] Food Establishment\n[2] Food Item\n[0] Cancel", "int", 0, 2)
    # Declare type based on user input
    if (type_input == 1):
        if (not(establishment_total > 0)):
            show_message("There are no food establishments!")
            return
        else:
            type = "food_establishment"
    elif (type_input == 2):
        if (not(item_total > 0)):
            show_message("There are no food items!")
            return
        else:
            type = "food_item"
    elif (type_input == 0):
        return

    # Get total number of reviews
    review_total = count(cur, "food_review", False)

    new_review_id = review_total+1

    # Entity id
    if (type == "food_establishment"):
        establishment_id = get_id("Enter the establishment ID: ", "food_establishment", None, None, cur)
        item_id = None
    elif (type == "food_item"):
        item_id = get_id("Enter the food item ID: ", "food_item", None, None, cur)
        cur.execute("SELECT establishment_id FROM food_item WHERE item_id = ?;", (item_id,))
        establishment_id = cur.fetchone()[0]

    # Rating
    rating = get_user_input("Enter rating (from 1 to 5): ", "int", 1, 5)

    # User id
    user_id = get_id("Enter the user ID: ", "user", None, None, cur)

    # Date
    use_today = messagebox.askyesno("Input", "Use date today for review date?")
    if use_today:
        date = datetime.today().strftime('%Y-%m-%d')
    else:
        date = get_user_input("Enter review date (YYYY-MM-DD): ", "date")

    # Insert new review
    cur.execute("INSERT INTO food_review VALUES (?, ?, ?, ?, ?, ?);", (new_review_id, rating, date, establishment_id, item_id, user_id))

    # Update establishment ratings
    cur.execute("UPDATE food_establishment e SET establishment_rating = (SELECT TRUNCATE(SUM(rating)/COUNT(rating),1) FROM food_review r WHERE r.establishment_id = e.establishment_id);")

    show_message("Review added successfully!")

# Update a review
def update_review(cur):
    # Get total number of reviews
    review_total = count(cur, "food_review", False)
    # Display all reviews
    view_all_reviews(cur)

    # Return if there are no reviews
    if (not(review_total > 0)):
        return

    review_id = get_id("Enter the ID of review to be updated: ", "food_review", None, None, cur)
    show_message(f"Review Info: {view_a_review(cur, review_id)}")

    # Update menu
    choice = get_user_input("Update:\n[1] Rating\n[2] Food Establishment\n[3] Food Item\n[0] Cancel", "int", 0, 3)

    if choice == 1:
        attribute = "rating"
        value = get_user_input("Enter new rating (from 1 to 5): ", "int", 1, 5)
    elif choice == 2:
        attribute = "establishment_id"
        value = get_id("Enter new establishment ID: ", "food_establishment", None, None, cur)
    elif choice == 3:
        attribute = "item_id"
        value = get_id("Enter new food item ID: ", "food_item", "Just remove food item? (y/n)", True, cur)
    elif choice == 0:
        return
    else:
        show_message("Invalid choice!")
        return

    # Update chosen field
    cur.execute(f"UPDATE food_review SET {attribute} = ? WHERE review_id = ?;", (value, review_id))

    # Update establishment ratings
    cur.execute("UPDATE food_establishment e SET establishment_rating = (SELECT TRUNCATE(SUM(rating)/COUNT(rating),1) FROM food_review r WHERE r.establishment_id = e.establishment_id);")

    show_message(f"Review's {attribute} was successfully updated!")

# Delete a review
def delete_review(cur):
    # Get total number of reviews
    review_total = count(cur, "food_review", False)
    # Display all reviews
    view_all_reviews(cur)

    # Return if there are no reviews
    if (not(review_total > 0)):
        return

    review_id = get_id("Enter the ID of the review to be deleted: ", "food_review", None, None, cur)

    # Update establishment ratings
    cur.execute("UPDATE food_establishment e SET establishment_rating = (SELECT TRUNCATE(SUM(rating)/COUNT(rating),1) FROM food_review r WHERE r.establishment_id = e.establishment_id);")
    # Delete review
    cur.execute("DELETE FROM food_review WHERE review_id = ?", (review_id,))

    show_message("Review deleted.")

# View all reviews
def view_all_reviews(cur):
    cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review")

    # Fetch all results
    reviews = cur.fetchall()

    # Prompt for no review
    if (len(reviews) == 0):
        show_message("There are no reviews!")
    else:
        reviews_text = "\n=============================="
        for (review_id, rating, date, establishment_id, item_id, user_id) in reviews:
            # User name
            cur.execute("SELECT username FROM user WHERE user_id = ?", (user_id,))
            username = cur.fetchone()[0]

            # Establishment name
            cur.execute("SELECT establishment_name FROM food_establishment WHERE establishment_id = ?", (establishment_id,))
            establishment_name = cur.fetchone()[0]

            if (item_id):
                # Food name
                cur.execute("SELECT food_name FROM food_item WHERE item_id = ?", (item_id,))
                food_name = cur.fetchone()[0]
                # Print w/ food
                reviews_text += f"\n[Review ID: {review_id}]\nUser: {username}\nRating: {rating}/5 \tDate: {date}\nEstablishment: \t\"{establishment_name}\"\nFood Name: \t\"{food_name}\"\n=============================="
            else:
                # Print w/o food
                reviews_text += f"\n[Review ID: {review_id}]\nUser: {username}\nRating: {rating}/5 \t Date: {date}\nEstablishment: \t\"{establishment_name}\"\n=============================="
        show_message(reviews_text)

# View a specific review
def view_a_review(cur, id):
    cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review WHERE review_id = ?", (id,))

    # Fetch all results
    review = cur.fetchall()

    # Print the review
    review_text = "\n=============================="
    for (review_id, rating, date, establishment_id, item_id, user_id) in review:
        # User name
        cur.execute("SELECT username FROM user WHERE user_id = ?", (user_id,))
        username = cur.fetchone()[0]

        # Establishment name
        cur.execute("SELECT establishment_name FROM food_establishment WHERE establishment_id = ?", (establishment_id,))
        establishment_name = cur.fetchone()[0]

        if (item_id):
            # Food name
            cur.execute("SELECT food_name FROM food_item WHERE item_id = ?", (item_id,))
            food_name = cur.fetchone()[0]
            # Print w/ food
            review_text += f"\n[Review ID: {review_id}]\nUser: {username}\nRating: {rating}/5 \tDate: {date}\nEstablishment: \t\"{establishment_name}\"\nFood Name: \t\"{food_name}\"\n=============================="
        else:
            # Print w/o food
            review_text += f"\n[Review ID: {review_id}]\nUser: {username}\nRating: {rating}/5 \t Date: {date}\nEstablishment: \t\"{establishment_name}\"\n=============================="
    return review_text

# View reviews for a food item or establishment
def view_reviews(cur):
    # Get total number of establishments
    establishment_total = count(cur, "food_establishment", False)
    # Get total number of items
    item_total = count(cur, "food_item", False)

    # Halt if there are no entities (both establishment and item)
    if (establishment_total <= 0 and item_total <= 0):
        show_message("There are no food establishments or food items!")
        return

    # Add menu
    type_input = get_user_input("Please select one you would like to view the reviews for:\n[1] Food Establishment\n[2] Food Item\n[0] Cancel", "int", 0, 2)
    # Declare type based on user input
    if (type_input == 1):
        if (not(establishment_total > 0)):
            show_message("There are no food establishments!")
            return
        else:
            type = "food_establishment"
            id_type = "establishment"
    elif (type_input == 2):
        if (not(item_total > 0)):
            show_message("There are no food items!")
            return
        else:
            type = "food_item"
            id_type = "item"

    elif (type_input == 0):
        return

    # Get user input for bool for recent reviews
    is_recent = get_user_input("View only recent reviews? (y/n): ", "bool")
    # Get entity id
    id = get_id(f"Enter the {type} ID: ", type, None, None, cur)

    # Get all reviews for chosen type and id
    if (is_recent):
        cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review WHERE {id_type}_id = ? AND DATEDIFF(NOW(), date) <= 30", (id,))
    else:
        cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review WHERE {id_type}_id = ?", (id,))

    # Fetch all results
    reviews = cur.fetchall()

    # Prompt for no review
    if (len(reviews) == 0):
        if (is_recent):
            show_message(f"There are no recent reviews for that food {id_type}!")
        else:
            show_message(f"There are no reviews for that food {id_type}!")
    else:
        reviews_text = "\n=============================="
        for (review_id, rating, date, establishment_id, item_id, user_id) in reviews:
            # User name
            cur.execute("SELECT username FROM user WHERE user_id = ?", (user_id,))
            username = cur.fetchone()[0]

            # Establishment name
            cur.execute("SELECT establishment_name FROM food_establishment WHERE establishment_id = ?", (establishment_id,))
            establishment_name = cur.fetchone()[0]

            if (type == "food_item"):
                # Food name
                cur.execute("SELECT food_name FROM food_item WHERE item_id = ?", (item_id,))
                food_name = cur.fetchone()[0]
                # Print w/ food
                reviews_text += f"\n[Review ID: {review_id}]\nUser: {username}\nRating: {rating}/5 \tDate: {date}\nEstablishment: \t\"{establishment_name}\"\nFood Name: \t\"{food_name}\"\n=============================="
            else:
                # Print w/o food
                reviews_text += f"\n[Review ID: {review_id}]\nUser: {username}\nRating: {rating}/5 \t Date: {date}\nEstablishment: \t\"{establishment_name}\"\n=============================="
        show_message(reviews_text)

# Menu for reviews
def review_menu(cur):
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root = tk.Tk()
    root.title("Review Menu")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    def view_reviews_callback():
        view_reviews(cur)

    def add_review_callback():
        add_review(cur)

    def update_review_callback():
        update_review(cur)

    def delete_review_callback():
        delete_review(cur)

    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    tk.Button(frame, text="View Reviews for a Food Establishment or Item", command=view_reviews_callback).pack(pady=5)
    tk.Button(frame, text="Add a Review", command=add_review_callback).pack(pady=5)
    tk.Button(frame, text="Edit a Review", command=update_review_callback).pack(pady=5)
    tk.Button(frame, text="Delete a Review", command=delete_review_callback).pack(pady=5)
    tk.Button(frame, text="Back to Menu", command=root.destroy).pack(pady=5)

    root.mainloop()

# Utility functions
def count(cur, entity, condition=None):
    if condition:
        cur.execute(f"SELECT COUNT(*) FROM {entity} WHERE {condition}")
    else:
        cur.execute(f"SELECT COUNT(*) FROM {entity}")
    return cur.fetchone()[0]

def validate_id(cur, entity, id):
    cur.execute(f"SELECT COUNT(*) FROM {entity} WHERE {id} = ?", (id,))
    return cur.fetchone()[0]

def get_id(prompt, entity, condition=None, is_optional=None, cur=None):
    if is_optional:
        use_existing = get_user_input(f"{prompt} \n (Leave blank to skip)", "bool")
        if not use_existing:
            return None
    while True:
        id = get_user_input(prompt, "int")
        if validate_id(cur, entity, id) > 0:
            return id
        else:
            show_message(f"Invalid {entity} ID! Please try again.")