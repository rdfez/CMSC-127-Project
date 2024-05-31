from misc import count, get_id, get_input, validate_id
from datetime import datetime
import os

import mariadb

# Add a review
# - Parameters:
#   1. cursor (cursor): mariaDB cursor
def add_review (cur):
  # Get total number of establishments
  establishment_total = count(cur, "establishment", False)
  # Get total number of items
  item_total = count(cur, "item", False)

  # Halt if there are no entities (both establishment and item)
  if(not(establishment_total > 0) and not(item_total > 0)):
    print("There are no food establishments or food items!")
    return

  # Add menu
  print('''\nPlease select one you would like to create a review for:
          [1] Food Establishment
          [2] Food Item
          [0] Cancel
          ''')
  
  type_input = get_input("Enter your choice: ", "int", 0, 2, None, None)
  # Declare type based on user input
  if (type_input == 1):
    if (not(establishment_total > 0)):
      print("There are no food establishments!")
      return
    else:
      type = "establishment"
  elif (type_input == 2):
    if (not(item_total > 0)):
      print("There are no food items!")
      return
    else:
      type = "item" 
  elif (type_input == 0):
    return

  # Get total number of reviews
  review_total = count(cur, "review", False) + 1

  # Get id of new review by looping through review ids
  for i in range(1, review_total+1):
    # Check if id is being used
    if validate_id(cur, "review", i) == 1:
      continue
    else:
      # Assign id of new review
      new_review_id = i
      break

  # Entity id
  if (type == "establishment"):
    # TODO: view all establishments
    establishment_id = get_id("\nEnter the establishment ID: ", "establishment", None, None, cur)
    item_id = None
  elif (type == "item"):
    item_id = get_id("\nEnter the food item ID: ", "item", None, None, cur)
    cur.execute("SELECT establishment_id FROM food_item WHERE item_id = ?;", (item_id,))
    establishment_id = cur.fetchone()[0]

  # Rating
  rating = get_input("\nEnter rating (from 1 to 5): ", "int", 1, 5, None, None)

  # User id
  user_id = get_id("\nEnter the user ID: ", "user", None, None, cur)

  # Date
  date = get_input("\nEnter review date (YYYY-MM-DD): ", "date", None, None, "\nUse date today for review date? (y/n) ", True)
  # Assign date today to date variable
  if (date == None):
    date = datetime.today().strftime('%Y-%m-%d')
  
  # Insert new review
  cur.execute("INSERT INTO food_review VALUES (?, ?, ?, ?, ?, ?);", (new_review_id, rating, date, establishment_id, item_id, user_id))
    
  # Update establishment ratings
  cur.execute("UPDATE food_establishment e SET establishment_rating = (SELECT TRUNCATE(SUM(rating)/COUNT(rating),1) FROM food_review r WHERE r.establishment_id = e.establishment_id and item_id IS NULL);")

  print("\nNew Review: ")
  view_a_review(cur, new_review_id)

  print("\nReview added successfully!")

# Update a review
# - Parameters:
#   1. cursor (cursor): mariaDB cursor
def update_review (cur):
    # Get total number of reviews
    review_total = count(cur, "review", False)
    # Display all reviews
    view_all_reviews(cur)

    # Return if there are no reviews
    if (not(review_total > 0)):
      return
    
    review_id = get_id("\nEnter the ID of review to be updated: ", "review", None, None, cur)

    print(f"\nReview Info:")
    view_a_review(cur, review_id)

    # Update menu
    print("\nUpdate: ")
    print("\t[1] Rating")
    print("\t[2] Food Establishment")
    print("\t[3] Food Item")
    print("\t[0] Cancel")
    choice = get_input("\nEnter choice: ", "int", 0, 3, None, None)

    # Rating 
    if choice == 1:
        attribute = "rating"
        value = get_input("\nEnter new rating (from 1 to 5): ", "int", 1, 5, None, None)

    # Establishment
    elif choice == 2:
        attribute = "establishment_id"
        value = get_id("Enter new establishment ID: ", "establishment", None, None, cur)
    
    # Food
    elif choice == 3:
        attribute = "item_id"
        value = get_id("Enter new food item ID: ", "item", "\nJust remove food item? (y/n) ", True, cur)

    elif choice == 0:
        return

    else:
        print("Invalid choice!\n")
    
    # Update chosen field
    cur.execute(f"UPDATE food_review SET {attribute} = ? WHERE review_id = ?;", (value, review_id))
    
    # Update establishment ratings
    cur.execute("UPDATE food_establishment e SET establishment_rating = (SELECT TRUNCATE(SUM(rating)/COUNT(rating),1) FROM food_review r WHERE r.establishment_id = e.establishment_id and item_id IS NULL);")
  
    print(f"\nUpdated Review Info:")
    view_a_review(cur, review_id)

    print(f"\nReview's {attribute} was successfully updated!")

    return
            
# Delete a review
# - Parameters:
#   1. cursor (cursor): mariaDB cursor
def delete_review (cur):
    # Get total number of reviews
    review_total = count(cur, "review", False)
    # Display all reviews
    view_all_reviews(cur)

    # Return if there are no reviews
    if (not(review_total > 0)):
      return
    
    # Get review id from user input
    review_id = get_id("\nEnter the ID of the review to be deleted: ", "review", None, None, cur)
    
    # Update establishment ratings
    cur.execute("UPDATE food_establishment e SET establishment_rating = (SELECT TRUNCATE(SUM(rating)/COUNT(rating),1) FROM food_review r WHERE r.establishment_id = e.establishment_id AND item_id IS NULL);")
    # Delete review
    cur.execute("DELETE FROM food_review WHERE review_id = ?", (review_id,))
    
    print("\nReview deleted.")

    return

# View all reviews (regardless of food/establishment)
# - Parameters:
#   1. cursor (cursor): mariaDB cursor  
def view_all_reviews (cur):
  cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review") 

  # Fetch all results
  reviews = cur.fetchall()
  
  # Prompt for no review
  if (len(reviews) == 0):
      # os.system('cls||clear')
      print(f"\nThere are no reviews!")
  # Print all reviews
  else:
    # os.system('cls||clear')
    print("\n==============================")
    # Loop through results
    for (review_id, rating, date, establishment_id, item_id, user_id) in reviews:
      # User name
      cur.execute("SELECT username FROM user WHERE user_id = ?", (user_id,))
      username = cur.fetchone()[0]

      # Establishment name
      cur.execute("SELECT establishment_name FROM food_establishment WHERE establishment_id = ?", (establishment_id,))
      establishment_name = cur.fetchone()[0]

      if (item_id):
        #Food name
        cur.execute("SELECT food_name FROM food_item WHERE item_id = ?", (item_id,))
        food_name = cur.fetchone()[0]
        # Print w/ food
        print(f"\n[Review ID: {review_id}]")
        print(f"User: {username}")
        print(f"Rating: {rating}/5 \tDate: {date}")
        print(f"Establishment: \t\"{establishment_name}\"")
        print(f"Food Name: \t\"{food_name}\"")
        print("\n==============================")
        
      else:
        # Print w/o food
        print(f"\n[Review ID: {review_id}]")
        print(f"User: {username}")
        print(f"Rating: {rating}/5 \t Date: {date}")
        print(f"Establishment: \t\"{establishment_name}\"")
        print("\n======================================")

  return

# View all reviews for a food item or establishment
# - Parameters:
#   1. cursor (cursor): mariaDB cursor  
def view_reviews (cur): 
  # Get total number of establishments
  establishment_total = count(cur, "establishment", False)
  # Get total number of items
  item_total = count(cur, "item", False)

  # Halt if there are no entities (both establishment and item)
  if(not(establishment_total > 0) and not(item_total > 0)):
    print("There are no food establishments or food items!")
    return

  # Add menu
  print('''\nPlease select one you would like to view the reviews for:
          [1] Food Establishment
          [2] Food Item
          [0] Cancel
          ''')
  
  type_input = get_input("Enter your choice: ", "int", 0, 2, None, None)
  # Declare type based on user input
  if (type_input == 1):
    if (not(establishment_total > 0)):
      print("There are no food establishments!")
      return
    else:
      type = "establishment"
  elif (type_input == 2):
    if (not(item_total > 0)):
      print("There are no food items!")
      return
    else:
      type = "item" 
  elif (type_input == 0):
    return

  # Get user input for bool for recent reviews 
  is_recent = get_input("\nView only recent reviews? (y/n): ", "bool", None, None, None, None)
  # Get entity id
  id = get_id(f"\nEnter the {type} ID: ", type, None, None, cur)

  # Get all reviews for chosen type and id
  if (is_recent):
    cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review WHERE {type}_id = ? AND DATEDIFF(NOW(), date) <= 30", (id,)) 
  else:
    cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review WHERE {type}_id = ?", (id,)) 

  # Fetch all results
  reviews = cur.fetchall()
  
  # Prompt for no review
  if (len(reviews) == 0):
      # os.system('cls||clear')
      if (is_recent):
        print(f"\nThere are no recent reviews for that food {type}!")
      else:
        print(f"\nThere are no reviews for that food {type}!")
  # Print all reviews
  else:
    # os.system('cls||clear')
    print("\n==============================")
    # Loop through results
    for (review_id, rating, date, establishment_id, item_id, user_id) in reviews:
      # User name
      cur.execute("SELECT username FROM user WHERE user_id = ?", (user_id,))
      username = cur.fetchone()[0]

      # Establishment name
      cur.execute("SELECT establishment_name FROM food_establishment WHERE establishment_id = ?", (establishment_id,))
      establishment_name = cur.fetchone()[0]

      if (type == "item"):
        #Food name
        cur.execute("SELECT food_name FROM food_item WHERE item_id = ?", (item_id,))
        food_name = cur.fetchone()[0]
        # Print w/ food
        print(f"\n[Review ID: {review_id}]")
        print(f"User: {username}")
        print(f"Rating: {rating}/5 \tDate: {date}")
        print(f"Establishment: \t\"{establishment_name}\"")
        print(f"Food Name: \t\"{food_name}\"")
        print("\n==============================")
        
      else:
        # Print w/o food
        print(f"\n[Review ID: {review_id}]")
        print(f"User: {username}")
        print(f"Rating: {rating}/5 \t Date: {date}")
        print(f"Establishment: \t\"{establishment_name}\"")
        print("\n==============================")

  return

# View a specific review
# - Parameters:
#   1. cursor (cursor): mariaDB cursor  
#   1. id (int): review ID
def view_a_review (cur, id):
  cur.execute(f"SELECT review_id, rating, date, establishment_id, item_id, user_id FROM food_review WHERE review_id = ?", (id,)) 

  # Fetch all results
  review = cur

  # Print the review
  print("\n==============================")
  for (review_id, rating, date, establishment_id, item_id, user_id) in review:
    # User name
    cur.execute("SELECT username FROM user WHERE user_id = ?", (user_id,))
    username = cur.fetchone()[0]

    # Establishment name
    cur.execute("SELECT establishment_name FROM food_establishment WHERE establishment_id = ?", (establishment_id,))
    establishment_name = cur.fetchone()[0]

    if (item_id):
      #Food name
      cur.execute("SELECT food_name FROM food_item WHERE item_id = ?", (item_id,))
      food_name = cur.fetchone()[0]
      # Print w/ food
      print(f"\n[Review ID: {review_id}]")
      print(f"User: {username}")
      print(f"Rating: {rating}/5 \tDate: {date}")
      print(f"Establishment: \t\"{establishment_name}\"")
      print(f"Food Name: \t\"{food_name}\"")
      print("\n==============================")
      
    else:
      # Print w/o food
      print(f"\n[Review ID: {review_id}]")
      print(f"User: {username}")
      print(f"Rating: {rating}/5 \t Date: {date}")
      print(f"Establishment: \t\"{establishment_name}\"")
      print("\n==============================")

    
  return

# Menu for reviews
def review_menu(cur): 

  while True:
    print("\n========== Reviews ==========\n")
    print("[1] View Reviews for a Food Establishment or Item")
    print("[2] Add a Review")
    print("[3] Edit a Review")
    print("[4] Delete a Review")
    print("[0] Back to Menu")
    print("\n==============================")
    choice = get_input("\nEnter your choice: ", "int", 0, 4, None, None)

    if choice == 1:
        print("\n-> Viewing reviews for a food establishment or item")
        view_reviews(cur)
    elif choice == 2:
        print("\n-> Adding a review")
        add_review(cur)
    elif choice == 3:
        print("\n-> Editing a review")
        update_review(cur)
    elif choice == 4:
        print("\n-> Deleting a review")
        delete_review(cur)
    elif choice == 0: break

  return

#################################

