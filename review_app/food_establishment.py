import mariadb
import sys

def formatItem(item):
     return (
        f"==============================\n"
        f"Establishment ID: {item[0]}\n"
        f"Establishment Name: {item[1]}\n"
        f"Establishmen Rating: {item[2]}\n"
        f"Location: {item[3]}\n"
        f"Manager ID: {item[4]}\n"
        f"==============================\n"
    )

def view_estab(choice):
    if choice == 1:
        cur.execute("SELECT * FROM food_establishment")
    elif choice == 2:
        cur.execute("SELECT * FROM food_establishment WHERE establishment_rating >= 4")
    
    results = cur.fetchall()
    print(f"Number of establishments found: {len(results)}")
    
    if results:
        for row in results:
            print(formatItem(row))
    else:
        print("No establishments found for the given criteria.")

def add_estab(estabId, estabName, loc, estabManagerId):
    try:
        cur.execute('''
            INSERT INTO food_establishment (establishment_id, establishment_name, establishment_rating, location, manager_id)        
            VALUES (?, ?, ?, ?, ?)
        ''', (estabId, estabName, None, loc, estabManagerId))
        print("Establishment added successfully.")
    except mariadb.Error as e:
        print(f"Error: {e}")

def edit_estab(id):
    cur.execute('''
       SELECT * FROM food_establishment WHERE establishment_id = ?     
    ''', (id,))
    item = cur.fetchone()
    if item:
        print(formatItem(item))
        new_estName = input("Insert new establishment name: ")
        new_estRating = input("Insert new rating here: ")
        new_loc = input("Insert new location here: ")
        cur.execute('''
            UPDATE food_establishment 
            SET establishment_name = ?, establishment_rating = ?, location = ?
            WHERE establishment_id = ?
        ''', (new_estName, new_estRating, new_loc, id))
        print("Establishment updated successfully.")
    else:
        print("Establishment not found.")

def delete_estab(id):
    cur.execute('''
        DELETE FROM food_establishment WHERE establishment_id = ?
    ''', (id,))
    print("Establishment deleted successfully.")

def search_estab(id):
    cur.execute('''
        SELECT * FROM food_establishment WHERE establishment_id = ?
    ''', (id,))
    result = cur.fetchone()
    if result:
        print(formatItem(result))
    else:
        print("Establishment not found.")

def main():
    estab_menu(cur)

def estab_menu(main_cur):
    global cur
    cur = main_cur
    while True:
        print("\n===== Food Establishments =====\n")
        print("[1] View all food establishments")
        print("[2] View Highest-rated Food establishments")
        print("[3] Add a food establishment")
        print("[4] Update a food establishment")
        print("[5] Delete a food establishment")
        print("[6] Search a food establishment")
        print("[0] Back to Menu")
        print("\n==============================")
        choice = int(input("\nEnter your choice: "))

        if choice == 1:
            view_estab(1)
        elif choice == 2:
            view_estab(2)
        elif choice == 3:
            try:
                estabId = int(input("\nInput Establishment ID: "))
                estabName = input("\nInput desired Establishment name: ")
                loc = input("\nInput Establishment Location: ")
                estabManagerId = int(input("\nInput Manager ID of Establishment: "))
                add_estab(estabId, estabName, loc, estabManagerId)
            except ValueError:
                print("Invalid input. Please enter valid data.")
        elif choice == 4:
            try:
                id = int(input("\nPlease enter the ID of the establishment you want to edit: "))
                edit_estab(id)
            except ValueError:
                print("Invalid input. Please enter a valid ID.")
        elif choice == 5:
            try:
                id = int(input("\nInsert the ID of the establishment to be deleted: "))
                delete_estab(id)
            except ValueError:
                print("Invalid input. Please enter a valid ID.")
        elif choice == 6:
            try:
                id = int(input("\nInsert the ID of the establishment to be searched: "))
                search_estab(id)
            except ValueError:
                print("Invalid input. Please enter a valid ID.")
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please select a valid option.")

global cur 

if __name__ == "__main__":
    main()