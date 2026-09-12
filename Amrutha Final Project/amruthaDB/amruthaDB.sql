create database amrutha;
use amrutha;
CREATE TABLE users (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(10),
    last_name VARCHAR(10),
    email_id VARCHAR(40),
    mobile_no VARCHAR(10),
    password VARCHAR(255),  
    address VARCHAR(50),
    usertype VARCHAR(10)
);

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100),
    description TEXT,
    price DECIMAL(10, 2),
    stock INT,
    image VARCHAR(100)
);

CREATE TABLE cart (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (user_id) REFERENCES users(userID) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(userID) ON DELETE CASCADE
);

create table contact(
	id INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(25),
    email varchar(25),
	message varchar(50)
);

select * from contact;




select *from users; 

SELECT * FROM users WHERE password = '112233';
