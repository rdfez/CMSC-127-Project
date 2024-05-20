# CMSC-127-Project
Table of Contents
- [References](#references)  
- [Schemas](#schemas)
- [Tasks](#tasks)

# References
- [How to connect Python programs to MariaDB](https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/)

# Schemas
1. User
    - `user_id` INT (50) NOT NULL,
    - `email` VARCHAR (50) NOT NULL,
    - `username` VARCHAR (50) NOT NULL,
    - `login_credentials` VARCHAR (50) NOT NULL,
    - `is_customer` BOOLEAN,
    - `is_manager` BOOLEAN,
3. Food Establishment
    - `establishment_id` INT (50) NOT NULL,
    - `establishment_name` VARCHAR (50) NOT NULL,
    - `establishment_rating` INT (50) DEFAULT NULL,
    - `location` VARCHAR (50),
    - `manager_id` INT (50) NOT NULL,
      - foreign key
5. Food Item
    - `item_id` INT (50) NOT NULL,
    - `food_name` VARCHAR (50) NOT NULL,
    - `price` INT (50) NOT NULL,
    - `type` VARCHAR (10) NOT NULL,
    - `establishment_id` INT (50) NOT NULL,
      - foreign key
    - `manager_id` INT (50) NOT NULL,
      - foreign key
7. Food Review
    - `review_id` INT (50) NOT NULL,
    - `rating` INT (1) NOT NULL,
    - `date` DATE NOT NULL,
    - `establishment_id` INT (50) NOT NULL,
      - foreign key
    - `item_id` INT (50),
      - foreign key
    - `user_id` INT (50) NOT NULL,
      - foreign key

# Tasks
Misc
1. UI (menu/prompts)

User 
1. View all users (?) [^1]
2. Add a user (?) [^1]
3. Update a user (?) [^1]
4. Delete a user (?) [^1]

Food Establishment 
1. View all food establishments
2. View all highly rated food establishments (rating >= 4)
3. Add a food establishment
4. Update a food establishment
5. Delete a food establishment
6. Search a food establishment

Food Item
1. View all food items from a food establishment
    - no filter/sort
    - filter by food type (no filter / meat / veg / etc.)
    - sort by price
2. Search item from any establishment
    - based on price range  
    - based on food type
    - based on price range and food type
3. Add a food item
4. Update a food item
5. Delete a food item
6. Search a food item (?) [^1]

Food Review
1. View all reviews
    - for a food establishment
    - for a food item
2. View all reviews not older than one month 
    - for a food establishment 
    - for a food item
3. Add a review
4. Update a review
5. Delete a review

[^1]: May not be needed/low priority
