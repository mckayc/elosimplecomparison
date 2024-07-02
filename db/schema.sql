CREATE DATABASE IF NOT EXISTS elocompare;

USE elocompare;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS comparisons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item1_id INT,
    item2_id INT,
    winner_id INT,
    FOREIGN KEY (item1_id) REFERENCES items(id),
    FOREIGN KEY (item2_id) REFERENCES items(id),
    FOREIGN KEY (winner_id) REFERENCES items(id)
);
