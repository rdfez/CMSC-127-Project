import mariadb
import tkinter as tk
from tkinter import messagebox, simpledialog

from food_establishment import estab_menu
from food_item import item_menu
from food_review import review_menu

# Initialize database/connection
def init():
    # Connect to MariaDB Platform
    conn_bool = True
    while conn_bool:
        mariadb_password = simpledialog.askstring("Password", "Enter password:", show='*')

        try:
            conn = mariadb.connect(
                user="root",
                password=mariadb_password,
                host="localhost",
                autocommit=True
            )

            if conn:
                conn_bool = False

        except mariadb.Error as e:
            messagebox.showerror("Error", f"Error connecting to MariaDB Platform: {e}")

    # Get Cursor for DB functions
    global cur
    cur = conn.cursor()

    # Create database/tables on initial boot and use app database
    cur.execute("CREATE DATABASE IF NOT EXISTS `review_app`;")
    cur.execute("USE `review_app`;")
    cur.execute('''
        CREATE TABLE IF NOT EXISTS `user` (
            `user_id` INT (50) NOT NULL,
            `email` VARCHAR (50) NOT NULL,
            `username` VARCHAR (50) NOT NULL,
            `login_credentials` VARCHAR (50) NOT NULL,
            `is_customer` BOOLEAN,
            `is_manager` BOOLEAN,
            PRIMARY KEY (`user_id`)
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS `food_establishment` (
            `establishment_id` INT (50) NOT NULL,
            `establishment_name` VARCHAR (50) NOT NULL,
            `establishment_rating` INT (1) DEFAULT NULL,
            `location` VARCHAR (50),
            `manager_id` INT (50) NOT NULL,
            PRIMARY KEY (`establishment_id`),
            CONSTRAINT `foodestablishment_managerid_fk` 
              FOREIGN KEY (`manager_id`) REFERENCES `user` (`user_id`)
              ON DELETE CASCADE
              ON UPDATE CASCADE
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS `food_item` (
            `item_id` INT (50) NOT NULL,
            `food_name` VARCHAR (50) NOT NULL,
            `price` INT (50) NOT NULL,
            `type` VARCHAR (50) NOT NULL,
            `establishment_id` INT (50) NOT NULL,
            `manager_id` INT (50) NOT NULL,
            PRIMARY KEY (`item_id`),
            CONSTRAINT `fooditem_establishmentid_fk` 
              FOREIGN KEY (`establishment_id`) REFERENCES `food_establishment` (`establishment_id`)
              ON DELETE CASCADE
              ON UPDATE CASCADE,
            CONSTRAINT `fooditem_managerid_fk` 
              FOREIGN KEY (`manager_id`) REFERENCES `user` (`user_id`)
              ON DELETE CASCADE
              ON UPDATE CASCADE
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS `food_review` (
            `review_id` INT (50) NOT NULL,
            `rating` INT (1) NOT NULL,
            `date` DATE NOT NULL,
            `establishment_id` INT (50) NOT NULL,
            `item_id` INT (50),
            `user_id` INT (50) NOT NULL, 
            PRIMARY KEY (`review_id`),
            CONSTRAINT `foodreview_establishmentid_fk` 
              FOREIGN KEY(`establishment_id`) REFERENCES `food_establishment` (`establishment_id`)
              ON DELETE CASCADE
              ON UPDATE CASCADE,
            CONSTRAINT `foodreview_itemid_fk` 
              FOREIGN KEY (`item_id`) REFERENCES `food_item` (`item_id`)
              ON DELETE CASCADE
              ON UPDATE CASCADE,
            CONSTRAINT `foodreview_userid_fk` 
              FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
              ON DELETE CASCADE
              ON UPDATE CASCADE
        );
    ''')

# Create the main application window
class ReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Review Information System")
        self.main_menu()

    def main_menu(self):
        self.clear()
        tk.Label(self.root, text="Main Menu", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Food Establishments", command=self.food_establishments).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Food Items", command=self.food_items).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Reviews", command=self.reviews).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(fill=tk.X, padx=20, pady=5)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def food_establishments(self):
        estab_menu(cur)

    def food_items(self):
        item_menu(cur)

    def reviews(self):
        review_menu(cur)

if __name__ == "__main__":
    root = tk.Tk()
    init()
    app = ReviewApp(root)
    root.mainloop()