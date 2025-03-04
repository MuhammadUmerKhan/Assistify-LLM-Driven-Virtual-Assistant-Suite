use foodbot;
CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),  -- Could be session ID or user identifier
    items TEXT NOT NULL,  -- Stores ordered items in JSON format ({"burger": 2, "pizza": 1})
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('Pending', 'In Process', 'Completed') DEFAULT 'Pending'
);

INSERT INTO menu (name, price) VALUES
('Cheese Burger', 5.99),
('Chicken Burger', 6.99),
('Veggie Burger', 5.49),
('Pepperoni Pizza', 12.99),
('Margherita Pizza', 11.49),
('BBQ Chicken Pizza', 13.99),
('Grilled Chicken Sandwich', 7.99),
('Club Sandwich', 6.99),
('Spaghetti Carbonara', 9.99),
('Fettuccine Alfredo', 10.49),
('Tandoori Chicken', 11.99),
('Butter Chicken', 12.49),
('Beef Steak', 15.99),
('Chicken Biryani', 8.99),
('Mutton Biryani', 10.99),
('Prawn Curry', 13.49),
('Fish and Chips', 9.49),
('French Fries', 3.99),
('Garlic Bread', 4.49),
('Chocolate Brownie', 5.49),
('Vanilla Ice Cream', 3.99),
('Strawberry Shake', 4.99),
('Mango Smoothie', 5.49),
('Coca-Cola', 2.49),
('Pepsi', 2.49),
('Fresh Orange Juice', 4.99);
 
INSERT INTO orders (user_id, items, total_price, status) VALUES
('user_001', '{"Cheese Burger": 2, "French Fries": 1, "Coca-Cola": 1}', 17.46, 'Pending'),
('user_002', '{"Pepperoni Pizza": 1, "Garlic Bread": 1, "Pepsi": 1}', 19.97, 'In Process'),
('user_003', '{"Chicken Biryani": 2, "Mango Smoothie": 1}', 23.47, 'Completed'),
('user_004', '{"Club Sandwich": 1, "Strawberry Shake": 1}', 11.98, 'Pending'),
('user_005', '{"Beef Steak": 1, "Fresh Orange Juice": 1}', 20.98, 'In Process');

alter table orders drop column user_id;
select * from menu where name="Pizza";
select * from orders;
select * from menu;