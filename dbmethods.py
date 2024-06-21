import psycopg2
import helpers

# This class contains all the methods that interact with the database
class dbmethods:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="shopping_cart", user="root", password="password", host="db", port="5432")
        self.cur = self.connection.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                username VARCHAR(255),
                password VARCHAR(255),
                authToken VARCHAR(255)
            )
        ''')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255),
                itemName VARCHAR(255),
                itemPrice NUMERIC(10, 2),
                itemQuantity INTEGER,
                bought BOOLEAN
            )
        ''')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS order_sessions (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255),
                orderDate TIMESTAMP
            )
        ''')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS order_history (
                id SERIAL PRIMARY KEY,
                session_id INTEGER REFERENCES order_sessions(id),
                itemName VARCHAR(255),
                itemPrice NUMERIC(10, 2),
                itemQuantity INTEGER
            )
        ''')
        self.connection.commit()

    # Create a new user
    def create_user(self, name, email, username, hashedPass, authToken):
        self.cur.execute(
            "INSERT INTO users (name, email, username, password, authToken) VALUES (%s, %s, %s, %s, %s)",
            (name, email, username, hashedPass, authToken))
        self.connection.commit()

    # Verify login
    def verifyLogin(self, email):
        self.cur.execute(
            "SELECT * FROM users WHERE email = %s", (email,))
        return self.cur.fetchall()

    # Verify auth token
    def verifyAuth(self, authToken):
        self.cur.execute(
            "SELECT * FROM users WHERE authToken = %s", (authToken,))
        return self.cur.fetchall()

    # Update auth token
    def update_authToken(self, username, authToken):
        self.cur.execute(
            "UPDATE users SET authToken = %s WHERE username = %s", (authToken, username,))
        self.connection.commit()

    # Add item to cart
    def add_to_cart(self, username, itemName, itemPrice, itemQuantity):
        self.cur.execute(
            "INSERT INTO cart (username, itemName, itemPrice, itemQuantity, bought) VALUES (%s, %s, %s, %s, %s)",
            (username, itemName, itemPrice, itemQuantity, False))
        self.connection.commit()

    # Get an single Item
    def get_cart_item(self, username, itemName, itemPrice):
        self.cur.execute(
            "SELECT * FROM cart WHERE username = %s AND itemName = %s AND itemPrice = %s AND bought = False",
            (username, itemName, itemPrice))
        return self.cur.fetchall()

    # View cart
    def view_cart(self, username):
        self.cur.execute(
            "SELECT name FROM users WHERE username = %s", (username,))
        user = self.cur.fetchone()
        self.cur.execute(
            "SELECT * FROM cart WHERE username = %s AND bought = False", (username,))
        items = [{"id": item[0], "itemName": item[2], "itemPrice": float(item[3]), "itemQuantity": item[4]} for item in self.cur.fetchall()]
        return {"userName": user[0], "items": items}

    # Remove from cart
    def remove_from_cart(self, cart_id):
        self.cur.execute(
            "DELETE FROM cart WHERE id = %s", (cart_id,))
        self.connection.commit()

    # Update cart quantity
    def update_cart_quantity(self, cart_id, itemQuantity):
        self.cur.execute(
            "UPDATE cart SET itemQuantity = %s WHERE id = %s",
            (itemQuantity, cart_id)
        )
        self.connection.commit()

    # Checkout entire cart
    def checkout_entire_cart(self, username):
        self.cur.execute(
            "SELECT * FROM cart WHERE username = %s AND bought = False", (username,))
        items = self.cur.fetchall()
        self.cur.execute(
            "INSERT INTO order_sessions (username, orderDate) VALUES (%s, NOW()) RETURNING id", (username,))
        session_id = self.cur.fetchone()[0]
        for item in items:
            self.cur.execute(
                "INSERT INTO order_history (session_id, itemName, itemPrice, itemQuantity) VALUES (%s, %s, %s, %s)",
                (session_id, item[2], item[3], item[4]))
        self.cur.execute(
            "UPDATE cart SET bought = True WHERE username = %s AND bought = False", (username,))
        self.connection.commit()

    # Get order history
    def get_order_history(self, username):
        self.cur.execute(
            "SELECT name FROM users WHERE username = %s", (username,))
        user = self.cur.fetchone()
        self.cur.execute(
            "SELECT os.id, os.orderDate, oh.itemName, oh.itemPrice, oh.itemQuantity FROM order_sessions os JOIN order_history oh ON os.id = oh.session_id WHERE os.username = %s ORDER BY os.orderDate DESC", (username,))
        history = self.cur.fetchall()
        sessions = {}
        for record in history:
            session_id = record[0]
            if session_id not in sessions:
                sessions[session_id] = {
                    "orderDate": record[1].strftime('%Y-%m-%d %H:%M:%S'),
                    "items": []
                }
            sessions[session_id]["items"].append({
                "itemName": record[2],
                "itemPrice": float(record[3]),
                "itemQuantity": record[4]
            })
        return {"userName": user[0], "sessions": sessions}

    # Get user profile
    def get_user_profile(self, username):
        self.cur.execute(
            "SELECT name, email FROM users WHERE username = %s", (username,))
        user = self.cur.fetchone()
        return {"name": user[0], "email": user[1]} if user else None

    # Update user profile
    def update_user_profile(self, username, name, email):
        self.cur.execute(
            "UPDATE users SET name = %s, email = %s WHERE username = %s", (name, email, username))
        self.connection.commit()

    def closeConnection(self):
        self.connection.close()