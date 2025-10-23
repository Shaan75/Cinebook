import mysql.connector
from datetime import datetime
from tabulate import tabulate
import time, os, random

# Try importing colorama for colorful text
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except:
    os.system('pip install colorama')
    from colorama import Fore, Style, init
    init(autoreset=True)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Your MySQL password here
    database="movie_booking"
)
cursor = conn.cursor()

# ---------------- Utility Functions ----------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def loading(msg="Loading"):
    for i in range(3):
        print(f"{msg}{'.' * (i+1)}", end='\r')
        time.sleep(0.5)
    print(" " * 30, end='\r')

def random_greeting():
    greetings = [
        "🎬 Welcome to CineBook – Where Every Seat Tells a Story!",
        "🍿 Popcorn ready? Let’s find your next movie!",
        "🎥 Lights, Camera, Action! Welcome to CineBook!",
        "⭐ The best place to book your favorite movie tickets!"
    ]
    print(Fore.CYAN + random.choice(greetings) + Style.RESET_ALL)

# ---------------- Database Functions ----------------
def view_movies():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    if not movies:
        print(Fore.RED + "No movies found 🎞️")
        return
    print(Fore.YELLOW + "\n📽️  Now Showing:\n")
    print(Fore.GREEN + tabulate(
        [(m[0], m[1], m[2], m[3], f"₹{m[4]:.2f}") for m in movies],
        headers=["ID", "Title", "Duration", "Language", "Price"],
        tablefmt="fancy_grid"
    ))

def view_shows(movie_id):
    cursor.execute("SELECT * FROM shows WHERE movie_id=%s", (movie_id,))
    shows = cursor.fetchall()
    if not shows:
        print(Fore.RED + "No shows available for this movie 😢")
        return False
    shows_display = []
    for show in shows:
        show_id, mid, show_time, seats_left, total_seats = show
        shows_display.append([show_id, mid, show_time.strftime("%d-%b-%Y %H:%M"), seats_left, total_seats])
    print(Fore.LIGHTMAGENTA_EX + "\n🎞️  Available Shows:\n")
    print(Fore.GREEN + tabulate(shows_display, headers=["Show ID", "Movie ID", "Seats Left", "Total Seats"], tablefmt="fancy_grid"))
    return True

def book_ticket(user_id, show_id, seats):
    cursor.execute("SELECT seats_available, movie_id FROM shows WHERE show_id=%s", (show_id,))
    result = cursor.fetchone()
    if not result:
        print(Fore.RED + "❌ Invalid show ID.")
        return

    available, movie_id = result
    if seats <= 0:
        print(Fore.RED + "❌ Invalid seat count.")
        return
    if seats > available:
        print(Fore.YELLOW + f"⚠️ Only {available} seats left! Try again.")
        return

    # Get movie price
    cursor.execute("SELECT price FROM movies WHERE movie_id=%s", (movie_id,))
    price = cursor.fetchone()[0]
    total_cost = seats * price

    cursor.execute("""
        INSERT INTO bookings (user_id, show_id, seats_booked, booking_time)
        VALUES (%s,%s,%s,%s)
    """, (user_id, show_id, seats, datetime.now()))
    cursor.execute("UPDATE shows SET seats_available=seats_available-%s WHERE show_id=%s", (seats, show_id))
    conn.commit()
    print(Fore.GREEN + f"✅ Booking successful! {seats} seats reserved 🎉")
    print(Fore.LIGHTYELLOW_EX + f"💰 Total cost: ₹{total_cost:.2f}")
    cursor.execute("SELECT seats_available FROM shows WHERE show_id=%s", (show_id,))
    remaining = cursor.fetchone()[0]
    print(Fore.LIGHTCYAN_EX + f"Seats remaining for this show: {remaining}")

def view_user_bookings(user_id):
    cursor.execute("""
        SELECT b.booking_id, m.title, s.show_time, b.seats_booked, m.price
        FROM bookings b
        JOIN shows s ON b.show_id = s.show_id
        JOIN movies m ON s.movie_id = m.movie_id
        WHERE b.user_id=%s
    """, (user_id,))
    bookings = cursor.fetchall()
    if not bookings:
        print(Fore.RED + "No bookings found 🪑")
        return
    bookings_display = []
    for booking in bookings:
        bid, title, show_time, seats, price = booking
        total = seats * price
        bookings_display.append([bid, title, show_time.strftime("%d-%b-%Y %H:%M"), seats, f"₹{total:.2f}"])
    print(Fore.LIGHTYELLOW_EX + "\n🎫 Your Bookings:\n")
    print(Fore.GREEN + tabulate(bookings_display, headers=["Booking ID", "Movie", "Show Time", "Seats", "Total Cost"], tablefmt="fancy_grid"))

def register_user():
    print(Fore.LIGHTBLUE_EX + "\n📝 Register New User:")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter phone number: ")
    try:
        cursor.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        cursor.execute("SELECT user_id FROM users WHERE email=%s", (email,))
        user_id = cursor.fetchone()[0]
        print(Fore.GREEN + f"✅ Registration successful! Your User ID is: {user_id}")
        return user_id
    except mysql.connector.Error as e:
        print(Fore.RED + f"❌ Error: {e}")
        return None

def get_user_id():
    while True:
        try:
            user_id = int(input("Enter your User ID (or 0 to register new user): "))
            if user_id == 0:
                return register_user()
            cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
            if cursor.fetchone():
                return user_id
            else:
                print(Fore.RED + "❌ User ID not found. Try again or enter 0 to register.")
        except ValueError:
            print(Fore.RED + "❌ Enter a valid number!")

def view_movie_income():
    cursor.execute("""
        SELECT m.title, m.price, 
               IFNULL(SUM(b.seats_booked),0) AS total_seats_sold,
               IFNULL(SUM(b.seats_booked)*m.price,0) AS total_income
        FROM movies m
        LEFT JOIN shows s ON m.movie_id = s.movie_id
        LEFT JOIN bookings b ON s.show_id = b.show_id
        GROUP BY m.movie_id
    """)
    results = cursor.fetchall()
    print(Fore.LIGHTGREEN_EX + "\n💰 Movie-wise Income Report:\n")
    print(Fore.GREEN + tabulate(results, headers=["Movie", "Price", "Seats Sold", "Total Income"], tablefmt="fancy_grid"))

# ---------------- Main Menu ----------------
def main():
    clear_screen()
    random_greeting()
    time.sleep(1)

    while True:
        print(Fore.CYAN + "\n🎬 --- CINEBOOK MAIN MENU --- 🎬")
        print(Fore.LIGHTWHITE_EX + """
1️⃣  View Movies
2️⃣  View Shows
3️⃣  Book Ticket
4️⃣  View My Bookings
5️⃣  Register New User
6️⃣  Movie Income Report
7️⃣  Exit
""")
        choice = input(Fore.LIGHTYELLOW_EX + "Enter choice: " + Style.RESET_ALL)

        if choice == '1':
            clear_screen()
            view_movies()
        elif choice == '2':
            view_movies()
            try:
                movie_id = int(input("Enter Movie ID to view shows: "))
                clear_screen()
                view_shows(movie_id)
            except ValueError:
                print(Fore.RED + "❌ Invalid Movie ID")
        elif choice == '3':
            user_id = get_user_id()
            view_movies()
            try:
                movie_id = int(input("Enter Movie ID: "))
                if view_shows(movie_id):
                    show_id = int(input("Enter Show ID: "))
                    seats = int(input("Enter Number of Seats: "))
                    confirm = input(Fore.LIGHTYELLOW_EX + f"Confirm booking {seats} seats? (y/n): ")
                    if confirm.lower() == 'y':
                        loading("Booking your seats")
                        book_ticket(user_id, show_id, seats)
                    else:
                        print(Fore.RED + "Booking cancelled.")
            except ValueError:
                print(Fore.RED + "❌ Invalid input")
        elif choice == '4':
            user_id = get_user_id()
            clear_screen()
            view_user_bookings(user_id)
        elif choice == '5':
            clear_screen()
            register_user()
        elif choice == '6':
            clear_screen()
            view_movie_income()
        elif choice == '7':
            slow_print(Fore.LIGHTMAGENTA_EX + "\nThanks for using CineBook! 🎥 Have a great day! 🍿")
            break
        else:
            print(Fore.RED + "Invalid choice ❌ Try again!")

        input(Fore.LIGHTBLACK_EX + "\nPress Enter to return to menu...")
        clear_screen()

    cursor.close()
    conn.close()

# ---------------- Run Program ----------------
if __name__ == "__main__":
    main()
