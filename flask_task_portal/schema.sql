CREATE DATABASE IF NOT EXISTS library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'flask_user'@'localhost' IDENTIFIED BY 'flask_password';
CREATE USER IF NOT EXISTS 'flask_user'@'127.0.0.1' IDENTIFIED BY 'flask_password';
GRANT ALL PRIVILEGES ON library_db.* TO 'flask_user'@'localhost';
GRANT ALL PRIVILEGES ON library_db.* TO 'flask_user'@'127.0.0.1';
FLUSH PRIVILEGES;

USE library_db;

-- Module 1: Books. Three main fields: title, author, published_year.
CREATE TABLE IF NOT EXISTS books (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100) NOT NULL,
    published_year INT NOT NULL
);

-- Module 2: Members. Three main fields: name, email, phone.
CREATE TABLE IF NOT EXISTS members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30) NOT NULL
);

-- Module 3: Reservations. Three main fields: book_id, member_id, reservation_date.
CREATE TABLE IF NOT EXISTS reservations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
);

INSERT INTO books (title, author, published_year)
SELECT 'The Little Prince', 'Antoine de Saint-Exupery', 1943
WHERE NOT EXISTS (SELECT 1 FROM books WHERE title = 'The Little Prince');

INSERT INTO members (name, email, phone)
SELECT 'Demo Member', 'demo@example.com', '555-0100'
WHERE NOT EXISTS (SELECT 1 FROM members WHERE email = 'demo@example.com');
