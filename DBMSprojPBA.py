import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# ---------------- Connect to MySQL ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Replace with your MySQL password
    database="movie_booking"
)
cursor = conn.cursor()

# ---------------- Utility Functions ----------------
def fetch_movies():
    cursor.execute("SELECT * FROM movies")
    return cursor.fetchall()

def fetch_shows(movie_id):
    cursor.execute("SELECT * FROM shows WHERE movie_id=%s", (movie_id,))
    return cursor.fetchall()

def fetch_user_bookings(user_id):
    cursor.execute("""
        SELECT b.booking_id, m.title, s.show_time, b.seats_booked
        FROM bookings b
        JOIN shows s ON b.show_id = s.show_id
        JOIN movies m ON s.movie_id = m.movie_id
        WHERE b.user_id=%s
    """, (user_id,))
    return cursor.fetchall()

# ---------------- User Functions ----------------
def register_user():
    name = simpledialog.askstring("Register", "Enter your name:")
    email = simpledialog.askstring("Register", "Enter your email:")
    phone = simpledialog.askstring("Register", "Enter phone number:")
    if not name or not email or not phone:
        messagebox.showerror("Error", "All fields are required!")
        return None
    try:
        cursor.execute("INSERT INTO users (name, email, phone) VALUES (%s,%s,%s)", (name,email,phone))
        conn.commit()
        cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
        user_id = cursor.fetchone()[0]
        messagebox.showinfo("Success", f"Registration successful! Your User ID is: {user_id}")
        return user_id
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error: {e}")
        return None

def get_user_id():
    while True:
        user_id = simpledialog.askinteger("User Login/Register", "Enter User ID (0 to register):")
        if user_id == 0:
            return register_user()
        cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
        if cursor.fetchone():
            return user_id
        else:
            messagebox.showerror("Error", "User ID not found. Try again or 0 to register.")

# ---------------- GUI Windows ----------------
def view_movies_window():
    movies = fetch_movies()
    if not movies:
        messagebox.showinfo("Movies", "No movies available.")
        return

    win = tk.Toplevel(root)
    win.title("Movies List")
    win.geometry("500x300")

    tree = ttk.Treeview(win, columns=("ID","Title","Duration","Language"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Duration", text="Duration")
    tree.heading("Language", text="Language")

    for movie in movies:
        tree.insert("", tk.END, values=movie)
    tree.pack(expand=True, fill=tk.BOTH)

def view_shows_window():
    movies = fetch_movies()
    if not movies:
        messagebox.showinfo("Shows", "No movies available.")
        return

    movie_selection = simpledialog.askinteger("Select Movie", "Enter Movie ID to view shows:")
    shows = fetch_shows(movie_selection)
    if not shows:
        messagebox.showinfo("Shows", "No shows for this movie.")
        return

    win = tk.Toplevel(root)
    win.title("Shows List")
    win.geometry("600x300")

    tree = ttk.Treeview(win, columns=("ShowID","MovieID","Time","Seats"), show='headings')
    tree.heading("ShowID", text="Show ID")
    tree.heading("MovieID", text="Movie ID")
    tree.heading("Time", text="Show Time")
    tree.heading("Seats", text="Seats Left")

    for show in shows:
        tree.insert("", tk.END, values=(show[0], show[1], show[2].strftime("%d-%b-%Y %H:%M"), show[3]))
    tree.pack(expand=True, fill=tk.BOTH)

def book_ticket_window():
    user_id = get_user_id()
    movies = fetch_movies()
    if not movies:
        messagebox.showinfo("Booking", "No movies available.")
        return

    movie_id = simpledialog.askinteger("Select Movie", "Enter Movie ID:")
    shows = fetch_shows(movie_id)
    if not shows:
        messagebox.showinfo("Booking", "No shows for this movie.")
        return

    show_id = simpledialog.askinteger("Select Show", "Enter Show ID:")
    cursor.execute("SELECT seats_available FROM shows WHERE show_id=%s", (show_id,))
    available = cursor.fetchone()[0]

    seats = simpledialog.askinteger("Seats", f"Enter number of seats (Available: {available}):")
    if seats <= 0 or seats > available:
        messagebox.showerror("Error", "Invalid number of seats.")
        return

    confirm = messagebox.askyesno("Confirm", f"Confirm booking {seats} seats for Show ID {show_id}?")
    if confirm:
        cursor.execute("""
            INSERT INTO bookings (user_id, show_id, seats_booked, booking_time)
            VALUES (%s,%s,%s,%s)
        """, (user_id, show_id, seats, datetime.now()))
        cursor.execute("UPDATE shows SET seats_available=seats_available-%s WHERE show_id=%s", (seats, show_id))
        conn.commit()
        messagebox.showinfo("Success", f"Booking confirmed! Seats remaining: {available - seats}")

def view_bookings_window():
    user_id = get_user_id()
    bookings = fetch_user_bookings(user_id)
    if not bookings:
        messagebox.showinfo("Bookings", "No bookings found.")
        return

    win = tk.Toplevel(root)
    win.title("My Bookings")
    win.geometry("600x300")

    tree = ttk.Treeview(win, columns=("BookingID","Movie","Time","Seats"), show='headings')
    tree.heading("BookingID", text="Booking ID")
    tree.heading("Movie", text="Movie")
    tree.heading("Time", text="Show Time")
    tree.heading("Seats", text="Seats Booked")

    for b in bookings:
        tree.insert("", tk.END, values=(b[0], b[1], b[2].strftime("%d-%b-%Y %H:%M"), b[3]))
    tree.pack(expand=True, fill=tk.BOTH)

# ---------------- Main GUI ----------------
root = tk.Tk()
root.title("CineBook GUI")
root.geometry("600x400")

tk.Label(root, text="🎬 Welcome to CineBook!", font=("Helvetica", 20)).pack(pady=20)
tk.Button(root, text="View Movies", width=25, command=view_movies_window).pack(pady=5)
tk.Button(root, text="View Shows", width=25, command=view_shows_window).pack(pady=5)
tk.Button(root, text="Book Ticket", width=25, command=book_ticket_window).pack(pady=5)
tk.Button(root, text="View My Bookings", width=25, command=view_bookings_window).pack(pady=5)
tk.Button(root, text="Register New User", width=25, command=register_user).pack(pady=5)
tk.Button(root, text="Exit", width=25, command=root.destroy).pack(pady=20)

root.mainloop()

# Close DB connection when done
cursor.close()
conn.close()
