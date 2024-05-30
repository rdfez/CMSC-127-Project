import mariadb

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
# Food Item
# 1. View all food items from a food establishment
# == no filter/sort
# == filter by food type (no filter / meat / veg / etc.)
# == sort by price
# 2. Search item from any establishment 
# == based on price range  
# == based on food type
# == based on price range and food type
# 3. Add a food item
# 4. Update a food item
# 5. Delete a food item
# 6. Search a food item (?)

def viewItems(establishment_id):
    filter = input("Enter Filter[MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]: ")
    sort = input("Enter Sort Price[DESC/ASC]: ")

    if filter == 'NA':
        cur.execute("SELECT * FROM food_item WHERE establishment_id = ? ORDER BY price "+ sort , (establishment_id,))
    else:
        cur.execute("SELECT * FROM food_item WHERE establishment_id = ? type = ? ORDER BY price "+ sort, (establishment_id, filter))

    items = cur.fetchall()
    
    if items:
        print("Food Items:")
        for item in items:
            print(item)
    else:
        print("No food items found for this establishment.")


def searchItemEstablishment(item_id):
    price_min = int(input("Enter Price Range Minimum: "))
    price_max = int(input("Enter Price Range Maximum: "))
    food_type = input("Enter Food Type [MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]:")

    if filter == 'NA':
        cur.execute("SELECT * FROM food_item WHERE item_id = ? AND price BETWEEN ? AND ?", (item_id, price_min, price_max))
    else:
        cur.execute("SELECT * FROM food_item WHERE item_id = ? AND type = ? AND price BETWEEN ? AND ?", (item_id, food_type, price_min, price_max))

    items = cur.fetchall()
    
    if items:
        print("Food Items:")
        for item in items:
            print(item)
    else:
        print("No food items found for this establishment.")


def addItem():
    food_item_id = int(input("Enter Item ID: "))
    food_name = input("Enter Food Name: ")
    food_price = int(input("Enter Price: "))
    food_type = input("Enter Enter Type: ")
    food_establishment_id = int(input("Enter Establishment ID: "))
    food_manager_id = int(input("Enter Manager ID: "))

    cur.execute("INSERT INTO food_item (item_id, food_name, price, type, establishment_id, manager_id) VALUES (?, ?, ?, ?, ?, ?)", (food_item_id, food_name, food_price, food_type, food_establishment_id, food_manager_id))


def updateItem(item_id):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))

    item = cur.fetchone()
    if item:
        print(item)
        new_name  = input("Updated Name: ")
        new_price  = int(input("Updated Price: "))
        new_type = input("Updated Type: ")
    
        cur.execute("UPDATE food_item SET food_name = ?, price = ?, type = ? WHERE item_id = ?", (new_name, new_price, new_type, item_id))
    else:
        print("Food item not found.")
    

def deleteItem(item_id):
    cur.execute("DELETE FROM food_item WHERE item_id = ?", item_id)


def searchItem(item_id):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    if item:
        print(item)
    else:
        print("Food item not found.")

########################################################

# print("\nReview Information System")
# init()
global cur

def item_menu(main_cur):
  global cur
  cur = main_cur
  while True:
      print("======= Menu =======")
      print("[1] View all food items from a food establishment")
      print("[2] Search item from any establishment")
      print("[3] Add a food item")
      print("[4] Update a food item")
      print("[5] Delete a food item")
      print("[6] Search a food item")
      print("[0] Exit\n")
      choice = input("Enter your choice: ")

      if choice == '1':
          establishment_id = int(input("Enter Establishment ID: "))
          viewItems(establishment_id)

      elif choice == '2':
          item_id = input("Enter Item ID: ")
          searchItemEstablishment(item_id)

      elif choice == '3':
          addItem()

      elif choice == '4':
          item_id = int(input("Enter Item ID: "))
          updateItem(item_id)

      elif choice == '5':
          item_id = int(input("Enter Item ID: "))
          deleteItem(item_id)

      elif choice == '6':
          item_id = int(input("Enter Item ID: "))
          searchItem(item_id)

      elif choice == '0':

          break