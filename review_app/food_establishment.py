import mariadb

def  get_estab(cursor, choice):
    if choice == 1:
        cursor.execute("SELECT * FROM food_establishment")
    if choice == 2:
        cursor.execute("Select * FROM food_establishment WHERE reviews>=4")
    return cursor.fetchall()

def view_estab(cursor, choice):
    fEstab = get_estab(cursor, choice)
    print("Food Establishments:")
    if choice == 1:
        for estab in fEstab:
            print(f"Establishment ID: {estab[0]} \nEstablishment Name: {estab[1]} \nEstablishment Rating: {estab[3]} \nLocation: {estab[4]} \nManager ID: {estab[5]}\n")
    elif choice == 2:
        for estab in fEstab:
            print(f"Establishment ID: {estab[0]} \nEstablishment Name: {estab[1]} \nEstablishment Rating: {estab[3]} \nLocation: {estab[4]} \nManager ID: {estab[5]}\n")

def add_estab(cursor, estabId, estabName, loc, estabManagerId ):
    cursor.execute('''
        INSERT INTO food_establishment (establishment_id, establishment_name, establishment_rating, location, manager_id)        
        VALUES (?, ?, ?, ?, ?)
    ''', (estabId, estabName, None, loc, estabManagerId))

# def edit_estab(cursor, newEstID, newEstName, nReview, nloc, newEstManagerId):
#     cursor.execute('''

#     ''', ())

# def delete_estab(cursor, newEstID, newEstName, nReview, nloc, newEstManagerId):
#     cursor.execute('''

#     ''', ())


# Initialize database/connection
def main():
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
    conn.commit()
########################################################

print("\nReview Information System")

while True:
    print("====== Menu ======\n")
    print("1. View all food establishments\n")
    print("2. View Highest-rated Food establishments\n")
    print("3. Add a food establishment\n")
    print("4. Update a food establishment\n")
    print("5. Delete a food establishment\n")
    print("6. Search a food establishment\n")
    print("7. Exit\n")
    choice = input("\nEnter your choice: ")

    if choice == '1':
        view_estab(cur, 1)
    elif choice == '2':
        view_estab(cur, 2)
    elif choice == '3':
        estabId = input("\nInput desired Establishment ID: ")
        estabName = input("\nInput desired Establishment name: ")
        loc = input("\nInput Establishment Location: ")
        estabManagerId = input("\nInput Manager ID of Establishment: ")
        add_estab(cur, estabId, estabName, loc, estabManagerId)
    # elif choice == 4:
    #     newEstID= input("\nInput New Establishment ID: ")
    #     newEstName = input("\nInput New Establishment name: ")
    #     nReview = input("\nInput New review: ")
    #     nloc = input("\nInput New Establishment Location: ")
    #     newEstManagerId = input("\nInput New Manager ID: ")
    #     edit_estab(cur, newEstID, newEstName, nReview, nloc, newEstManagerId)
    elif choice == '7':
        break
