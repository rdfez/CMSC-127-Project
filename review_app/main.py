import mariadb
import os

from food_establishment import estab_menu, get_estab, view_estab, add_estab
from food_item import item_menu, viewItems, addItem, searchItem, searchItemEstablishment, deleteItem
from food_review import review_menu, add_review, view_reviews, update_review, delete_review

from misc import get_input, get_id, clear

# Initialize database/connection
def init():
    # Connect to MariaDB Platform
    conn_bool = True
    while conn_bool:
        mariadb_password = input("Enter password: ")

        try:
            conn = mariadb.connect(
                user = "root",
                password = mariadb_password,
                host = "localhost",
                autocommit = True
            )

            if(conn):
                conn_bool = False

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

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
            CONSTRAINT `foodestablishment_managerid_fk` FOREIGN KEY (`manager_id`) REFERENCES
        `user` (`user_id`)
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
            CONSTRAINT `fooditem_establishmentid_fk` FOREIGN KEY (`establishment_id`) REFERENCES
        `food_establishment` (`establishment_id`),
            CONSTRAINT `fooditem_managerid_fk` FOREIGN KEY (`manager_id`) REFERENCES
        `user` (`user_id`)
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
            CONSTRAINT `foodreview_establishmentid_fk` FOREIGN KEY(`establishment_id`) REFERENCES
        `food_establishment` (`establishment_id`),
            CONSTRAINT `foodreview_itemid_fk` FOREIGN KEY (`item_id`) REFERENCES
        `food_item` (`item_id`),
            CONSTRAINT `foodreview_userid_fk` FOREIGN KEY (`user_id`) REFERENCES
        `user` (`user_id`)
        );
    ''')

########################################################

print("\nReview Information System")
init()

while True:
  clear()
  print("\n======= Main Menu ======\n")
  print("[1] Food Establishments")
  print("[2] Food Items")
  print("[3] Reviews")
  print("[0] Exit")
  print("\n========================")
  choice = get_input("\nEnter Choice: ", "int", 0, 3, None, None)

  if choice == 1:
    clear()
    estab_menu(cur)
  elif choice == 2:
    clear()
    item_menu(cur)
  elif choice == 3:
    clear()
    review_menu(cur)
  elif choice == 0: break