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




# def  get_estab(choice):
#     if choice == 1:
#         cur.execute("SELECT * FROM food_establishment")
#     if choice == 2:
#         cur.execute("Select * FROM food_establishment WHERE reviews>=4")
#     return cur.fetchall()

def view_estab(choice):
    print("Food Establishments:")
    if choice == 1:
            cur.execute("SELECT * FROM food_establishment")
    elif choice == 2:
            cur.execute("Select * FROM food_establishment WHERE reviews >= 4")

def add_estab(estabId, estabName, loc, estabManagerId ):
    cur.execute('''
        INSERT INTO food_establishment (establishment_id, establishment_name, establishment_rating, location, manager_id)        
        VALUES (?, ?, ?, ?, ?)
    ''', (estabId, estabName, None, loc, estabManagerId,))

def edit_estab(id):
    cur.execute('''
       SELECT * FROM food_establishment WHERE establishment_id = ?     
    ''', (id,))

    item = cur.fetchone()
    if item:
        print(item)
        new_estName = input("Insert new establishment name: ")
        new_estRating = input("Insert new rating here: ")
        new_loc = input("Insert new location here: ")

        cur.execute("UPDATE food_establishment SET establishment_name = ?, establishment_rating = ?, location = ?", (new_estName), (new_estRating), (new_loc))
    else:
        print("Establishment not found.")
    

def delete_estab(id):
    cur.execute('''
        DELETE * FROM food_establishment WHERE establishment_id = ?
    ''', (id,))

def search_estab(id):
    cur.execute('''
        SELECT * FROM food establishment WHERE establishment_id =?
    ''', (id,))

########################################################

print("\nReview Information System")
init()
while True:
    print("====== Menu ======\n")
    print("1. View all food establishments\n")
    print("2. View Highest-rated Food establishments\n")
    print("3. Add a food establishment\n")
    print("4. Update a food establishment\n")
    print("5. Delete a food establishment\n")
    print("6. Search a food establishment\n")
    print("7. Exit\n")
    choice = int(input("\nEnter your choice: "))

    if choice == 1:
        view_estab(1)
    elif choice == 2:
        view_estab(2)
    elif choice == 3:
        estabId = input("\nInput desired Establishment ID: ")
        estabName = input("\nInput desired Establishment name: ")
        loc = input("\nInput Establishment Location: ")
        estabManagerId = input("\nInput Manager ID of Establishment: ")
        add_estab(estabId, estabName, loc, estabManagerId)
    elif choice == 4:
        id = int(input("\nPlease enter the ID of the establishment you want to edit: "))
        edit_estab(id)
    elif choice == 5:
        id = int(input("\nInsert the ID of the establishment to be deleted: "))
        delete_estab(id)
    elif choice == 6:
        id = int(input("\nInsert the ID of the establishment to be searched: "))
        search_estab(id)
    elif choice == 7:
        break