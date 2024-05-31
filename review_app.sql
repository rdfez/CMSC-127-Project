DROP DATABASE IF EXISTS `review_app`;
CREATE DATABASE IF NOT EXISTS `review_app`;
USE `review_app`;

-- User Table
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` INT (50) NOT NULL,
    `email` VARCHAR (50) NOT NULL,
    `username` VARCHAR (50) NOT NULL,
    `login_credentials` VARCHAR (50) NOT NULL,
    `is_customer` BOOLEAN,
    `is_manager` BOOLEAN,
    PRIMARY KEY (`user_id`)
);

-- Food Establishment Table
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

-- Food Item Table
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

-- Food Review Table
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

---- INSERT ----
-- User
INSERT INTO `user` (`user_id`, `email`, `username`, `login_credentials`, `is_customer`, `is_manager`) 
VALUES
  (1, 'john.doe@example.com', 'johndoe', 'password123', 0, 1),
  (2, 'jane.smith@example.com', 'janesmith', 'securepass456', 0, 1),
  (3, 'admin.user@example.com', 'adminuser', 'adminpass789', 0, 1),
  (4, 'manager.bob@example.com', 'managerbob', 'managerpass101', 0, 1),
  (5, 'customer.alice@example.com', 'customeralice', 'customerpass202', 1, 0),
  (6, 'charlie.brown@example.com', 'charliebrown', 'charliepass303', 1, 0),
  (7, 'lucy.vanpelt@example.com', 'lucyvanpelt', 'lucypass404', 1, 0),
  (8, 'peppermint.patty@example.com', 'peppermintpatty', 'pattypass505', 1, 0),
  (9, 'snoopy.dog@example.com', 'snoopydog', 'snoopypass606', 1, 0),
  (10, 'woodstock.bird@example.com', 'woodstockbird', 'woodstockpass707', 1, 0);

-- Food Establishment
INSERT INTO `food_establishment` (`establishment_id`, `establishment_name`, `establishment_rating`, `location`, `manager_id`) 
VALUES 
  (1, 'Tasty Bites', 4, '123 Main Street', 1),
  (2, 'Crispy Crunch', 3, '456 Elm Street', 4),
  (3, 'Spice Palace', 5, '789 Oak Street', 4),
  (4, 'Fresh Delight', NULL, '101 Pine Street', 2),
  (5, 'Savory Eats', 4, '202 Maple Street', 3),
  (6, 'Sushi House', NULL, '304 Narra Street', 2);

-- Food Item
INSERT INTO `food_item` (`item_id`, `food_name`, `price`, `type`, `establishment_id`, `manager_id`) 
VALUES 
  (1, 'BOLOGNESE', 350, 'PASTA', 1, 1),
  (2, 'CHICKEN', 200, 'MEAT', 2, 4),
  (3, 'GARLIC SHRIMP', 250, 'FISH', 3, 2),
  (4, 'BUKO SHAKE', 180, 'BEVERAGE', 4, 2),
  (5, 'LEMON SQUARES', 120, 'DESSERT', 5, 4),
  (6, 'CHEESEBURGER', 140, 'MEAT', 3, 2),
  (7, 'CAESAR SALAD', 80, 'VEG', 3, 3),
  (8, 'SASHIMI', 210, 'MEAT', 2, 2),
  (9, 'MARGHERITA PIZZA', 300, 'VEG', 2, 2);

-- Food Review 
INSERT INTO `food_review` VALUES
  (1, 4, "2024-05-10", 1, 1, 5),
  (2, 5, "2024-03-10", 2, NULL, 10),
  (3, 1, "2024-05-09", 4, 4, 9),
  (4, 3, "2024-04-29", 5, 5, 7),
  (5, 2, "2024-05-01", 3, NULL, 7),
  (6, 2, "2024-05-09", 3, 7, 8),
  (7, 2, "2024-04-27", 3, 6, 6);