CREATE DATABASE movie_booking;
USE movie_booking;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    duration VARCHAR(20),
    language VARCHAR(50)
);

CREATE TABLE shows (
    show_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    show_time DATETIME,
    seats_available INT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    show_id INT,
    seats_booked INT,
    booking_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

INSERT INTO users (name, email, phone) VALUES
('Aarav Mehta', 'aarav@gmail.com', '9876543210'),
('Priya Sharma', 'priya@gmail.com', '9988776655'),
('Rahul Singh', 'rahul@gmail.com', '9123456789');

INSERT INTO movies (title, duration, language) VALUES
('Inception', '2h 28m', 'English'),
('Pathaan', '2h 26m', 'Hindi'),
('Avengers: Endgame', '3h 1m', 'English'),
('RRR', '3h 7m', 'Telugu'),
('KGF Chapter 2', '2h 48m', 'Kannada');

INSERT INTO shows (movie_id, show_time, seats_available) VALUES
(1, '2025-10-23 14:00:00', 50),
(1, '2025-10-23 19:00:00', 50),
(2, '2025-10-23 15:00:00', 60),
(3, '2025-10-23 18:00:00', 70),
(4, '2025-10-24 13:00:00', 80),
(5, '2025-10-24 21:00:00', 65);
