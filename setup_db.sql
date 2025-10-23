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

INSERT INTO movies (title, duration, language, price) VALUES
('Spider-Man: No Way Home', '2h 28m', 'English', 250.00),
('Doctor Strange 2', '2h 35m', 'English', 240.00),
('Jawan', '2h 45m', 'Hindi', 200.00),
('Mission Impossible 7', '2h 30m', 'English', 270.00),
('Avatar 2', '3h 12m', 'English', 300.00),
('Bahubali 3', '2h 50m', 'Telugu', 220.00),
('Dangal', '2h 41m', 'Hindi', 180.00),
('Kantara', '2h 20m', 'Kannada', 200.00);

INSERT INTO shows (movie_id, show_time, seats_available) VALUES
-- Inception
(1, '2025-10-25 10:00:00', 50),
(1, '2025-10-25 14:00:00', 50),
(1, '2025-10-26 19:00:00', 50),

-- Pathaan
(2, '2025-10-25 11:00:00', 50),
(2, '2025-10-25 17:00:00', 50),
(2, '2025-10-26 20:00:00', 50),

-- Avengers: Endgame
(3, '2025-10-25 10:30:00', 50),
(3, '2025-10-26 16:00:00', 50),
(3, '2025-10-27 20:30:00', 50),

-- RRR
(4, '2025-10-25 13:00:00', 50),
(4, '2025-10-26 18:30:00', 50),
(4, '2025-10-27 21:00:00', 50),

-- KGF Chapter 2
(5, '2025-10-25 09:30:00', 50),
(5, '2025-10-25 15:30:00', 50),
(5, '2025-10-26 19:30:00', 50),

-- Spider-Man: No Way Home
(6, '2025-10-25 12:00:00', 50),
(6, '2025-10-26 17:00:00', 50),
(6, '2025-10-27 20:00:00', 50),

-- Doctor Strange 2
(7, '2025-10-25 11:30:00', 50),
(7, '2025-10-26 14:30:00', 50),
(7, '2025-10-27 19:30:00', 50),

-- Jawan
(8, '2025-10-25 10:00:00', 50),
(8, '2025-10-25 19:00:00', 50),
(8, '2025-10-26 22:00:00', 50),

-- Mission Impossible 7
(9, '2025-10-25 09:00:00', 50),
(9, '2025-10-26 15:00:00', 50),
(9, '2025-10-27 21:00:00', 50),

-- Avatar 2
(10, '2025-10-25 12:30:00', 50),
(10, '2025-10-26 16:30:00', 50),
(10, '2025-10-27 20:30:00', 50),

-- Bahubali 3
(11, '2025-10-25 13:30:00', 50),
(11, '2025-10-26 18:30:00', 50),
(11, '2025-10-27 22:30:00', 50),

-- Dangal
(12, '2025-10-25 14:00:00', 50),
(12, '2025-10-26 19:00:00', 50),
(12, '2025-10-27 21:30:00', 50),

-- Kantara
(13, '2025-10-25 08:30:00', 50),
(13, '2025-10-26 13:30:00', 50),
(13, '2025-10-27 18:30:00', 50);


ALTER TABLE shows ADD COLUMN total_seats INT DEFAULT 50;
UPDATE shows SET total_seats = 50;

