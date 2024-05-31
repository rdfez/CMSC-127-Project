import mariadb

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
# 6. Search a food item

def formatItem(item):
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


def viewItems():

    establishment_id = input("Enter Establishment ID: ")

    food_type = input("Enter Filter[MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]: ")
    sort = input("Enter Sort Price[DESC/ASC]: ")

    if filter == 'NA':
        cur.execute("SELECT * FROM food_item WHERE establishment_id = ? ORDER BY price "+ sort , (establishment_id,))
    else:
        cur.execute("SELECT * FROM food_item WHERE establishment_id = ? AND type = ? ORDER BY price "+ sort, (establishment_id, food_type))

    items = cur.fetchall()
    
    if items:
        print("Food Items:")
        for item in items:
            print(formatItem(item))
    else:
        print("No food items found for this establishment.")


def searchItemEstablishment():

    print("\n==============================\n")
    print("[1] Based on Price Range")
    print("[2] Based on Food Type")
    print("[3] Based on Price Range and Food Type")
    
    choice = int(input("\nEnter Filter Choice: "))

    if choice == 1:
        price_min = int(input("Enter Price Range Minimum: "))
        price_max = int(input("Enter Price Range Maximum: "))
        cur.execute("SELECT * FROM food_item WHERE price >= ? AND price <= ?", (price_min, price_max))

    elif choice == 2:  
        food_type = input("Enter Food Type [MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]:")
        cur.execute("SELECT * FROM food_item WHERE type = ?", (food_type,))

    elif choice == 3: 
        price_min = int(input("Enter Price Range Minimum: "))
        price_max = int(input("Enter Price Range Maximum: "))
        food_type = input("Enter Food Type [MEAT/VEG/PASTA/BEVERAGE/DESSERT/NA]:")
        cur.execute("SELECT * FROM food_item WHERE type = ? AND price >= ? AND price <= ?", (food_type, price_min, price_max))
    
    items = cur.fetchall()
    
    if items:
        print("Food Items:")
        for item in items:
            print(formatItem(item))
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


def updateItem():
    item_id = int(input("\nEnter Item ID: "))

    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))

    item = cur.fetchone()
    if item:
        print(formatItem(item))
        new_name  = input("Updated Name: ")
        new_price  = int(input("Updated Price: "))
        new_type = input("Updated Type: ")
    
        cur.execute("UPDATE food_item SET food_name = ?, price = ?, type = ? WHERE item_id = ?", (new_name, new_price, new_type, item_id))
    else:
        print("Food item not found.")
    

def deleteItem():
    cur.execute("SELECT * FROM food_item")

    item_id = int(input("Enter Item ID: "))

    cur.execute("DELETE FROM food_item WHERE item_id = ?", (item_id,))


def searchItem(item_id):
    cur.execute("SELECT * FROM food_item WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    if item:
        print(formatItem(item))
    else:
        print("Food item not found.")

########################################################

global cur

def item_menu(main_cur):
  global cur
  cur = main_cur
  while True:
      print("\n========= Food Items =========\n")
      print("[1] View all food items from a food establishment")
      print("[2] Search item from any establishment")
      print("[3] Add a food item")
      print("[4] Update a food item")
      print("[5] Delete a food item")
      print("[6] Search a food item")
      print("[0] Back to Menu")
      print("\n==============================")
      choice = input("\nEnter your choice: ")

      if choice == '1':
          viewItems()

      elif choice == '2':
          searchItemEstablishment()

      elif choice == '3':
          addItem()

      elif choice == '4':   
          updateItem()

      elif choice == '5':
          
          deleteItem()

      elif choice == '6':
          item_id = int(input("Enter Item ID: "))
          searchItem(item_id)

      elif choice == '0':

          break