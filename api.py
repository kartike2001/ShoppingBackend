import logging
from flask import Flask, request, jsonify, make_response, render_template, send_from_directory
from flask_cors import CORS
import bcrypt
from dbmethods import dbmethods
import helpers 
import hashlib

# Create the Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/orderHistoryPage')
def order_history_page():
    return render_template('order_history.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Create a new user endpoint
@app.route('/createUser', methods=['POST'])
def create_user():
    try:
        userInformation = request.json
        name = helpers.escape_html(helpers.escape_sql(userInformation["name"]))
        email = helpers.escape_html(helpers.escape_sql(userInformation["email"]))
        plainTextPassword = helpers.escape_html(helpers.escape_sql(userInformation["password"]))
        username = email.split("@")[0]
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(plainTextPassword.encode('utf-8'), salt)
        authToken = helpers.generate_token()
        db = dbmethods()
        db.create_user(helpers.escape_sql(name), helpers.escape_sql(email), helpers.escape_sql(username),
                       helpers.escape_sql(hashedPassword.decode()),
                       hashlib.sha256(authToken.encode("utf-8")).hexdigest())
        db.closeConnection()
        content = {"message": "User created successfully"}
        response = make_response(jsonify(content))
        response.set_cookie(key="authToken", value=authToken, httponly=True, max_age=3600)
        return response, 201
    except Exception as e:
        logger.error("Error creating user: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Verify user endpoint
@app.route('/verifyUser', methods=['POST'])
def verify_user():
    try:
        userInformation = request.json
        email = helpers.escape_html(helpers.escape_sql(userInformation['email']))
        plainTextPassword = helpers.escape_html(helpers.escape_sql(userInformation['password']))
        db = dbmethods()
        user = db.verifyLogin(helpers.escape_sql(email))
        if user and bcrypt.checkpw(plainTextPassword.encode('utf-8'), user[0][4].encode('utf-8')):
            authToken = helpers.generate_token()
            db.update_authToken(user[0][3], hashlib.sha256(authToken.encode("utf-8")).hexdigest())
            db.closeConnection()
            content = {"message": "User verified successfully", "name": user[0][1], "username": user[0][3],
                       "email": user[0][2], "authToken": authToken}
            response = make_response(jsonify(content))
            response.set_cookie(key="authToken", value=authToken, httponly=True, max_age=3600)
            return response, 200
        else:
            db.closeConnection()
            return jsonify({"message": "User verification failed"}), 401
    except Exception as e:
        logger.error("Error verifying user: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Add Item to cart endpoint
@app.route('/addToCart', methods=['POST'])
def add_to_cart():
    try:
        authToken = request.cookies.get('authToken')
        logger.debug("Received authToken: %s", authToken)
        if authToken:
            db = dbmethods()
            user = db.verifyAuth(hashlib.sha256(authToken.encode("utf-8")).hexdigest())
            if user:
                cartInformation = request.json
                itemName = helpers.escape_html(helpers.escape_sql(cartInformation["itemName"]))
                itemPrice = helpers.escape_html(helpers.escape_sql(cartInformation["itemPrice"]))
                itemQuantity = helpers.escape_html(helpers.escape_sql(cartInformation["itemQuantity"]))
                db.add_to_cart(user[0][3], itemName, itemPrice, itemQuantity)
                db.closeConnection()
                return jsonify({"message": f"Added {itemName} to the cart!"}), 200
            else:
                db.closeConnection()
                return jsonify({"message": "User verification failed"}), 401
        else:
            return jsonify({"message": "Authentication required"}), 401
    except Exception as e:
        logger.error("Error adding to cart: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


# View Cart endpoint
@app.route('/viewCart', methods=['GET'])
def view_cart():
    try:
        authToken = request.cookies.get('authToken')
        if authToken:
            db = dbmethods()
            user = db.verifyAuth(hashlib.sha256(authToken.encode("utf-8")).hexdigest())
            if user:
                cart = db.view_cart(user[0][3])
                db.closeConnection()
                return jsonify(cart), 200
            else:
                db.closeConnection()
                return jsonify({"message": "User verification failed"}), 401
        else:
            return jsonify({"message": "Authentication required"}), 401
    except Exception as e:
        logger.error("Error viewing cart: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Logout endpoint
@app.route('/logout', methods=['POST'])
def logout():
    try:
        response = make_response(jsonify({"message": "User logged out successfully"}))
        response.set_cookie(key='authToken', value='', expires=0)
        return response, 200
    except Exception as e:
        logger.error("Error logging out: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Remove cart endpoint
@app.route('/removeFromCart', methods=['POST'])
def remove_from_cart():
    try:
        authToken = request.cookies.get('authToken')
        if authToken:
            db = dbmethods()
            user = db.verifyAuth(hashlib.sha256(authToken.encode("utf-8")).hexdigest())
            if user:
                cart_id = request.json['cart_id']
                db.remove_from_cart(cart_id)
                db.closeConnection()
                return jsonify({"message": "Item removed from cart"}), 200
            else:
                db.closeConnection()
                return jsonify({"message": "User verification failed"}), 401
        else:
            return jsonify({"message": "Authentication required"}), 401
    except Exception as e:
        logger.error("Error removing from cart: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Update cart quantity endpoint
@app.route('/updateCartQuantity', methods=['POST'])
def update_cart_quantity():
    try:
        authToken = request.cookies.get('authToken')
        if authToken:
            db = dbmethods()
            user = db.verifyAuth(hashlib.sha256(authToken.encode("utf-8")).hexdigest())
            if user:
                cart_id = request.json['cart_id']
                itemQuantity = request.json['itemQuantity']
                db.update_cart_quantity(cart_id, itemQuantity)
                db.closeConnection()
                return jsonify({"message": "Cart item quantity updated"}), 200
            else:
                db.closeConnection()
                return jsonify({"message": "User verification failed"}), 401
        else:
            return jsonify({"message": "Authentication required"}), 401
    except Exception as e:
        logger.error("Error updating cart quantity: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Checkout cart endpoint
@app.route('/checkoutCart', methods=['POST'])
def checkout_cart():
    try:
        authToken = request.cookies.get('authToken')
        if authToken:
            db = dbmethods()
            user = db.verifyAuth(hashlib.sha256(authToken.encode("utf-8")).hexdigest())
            if user:
                db.checkout_entire_cart(user[0][3])
                db.closeConnection()
                return jsonify({"message": "Cart checked out successfully"}), 200
            else:
                db.closeConnection()
                return jsonify({"message": "User verification failed"}), 401
        else:
            return jsonify({"message": "Authentication required"}), 401
    except Exception as e:
        logger.error("Error checking out cart: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


# Get user order history endpoint
@app.route('/orderHistory', methods=['GET'])
def order_history():
    try:
        authToken = request.cookies.get('authToken')
        if authToken:
            db = dbmethods()
            user = db.verifyAuth(hashlib.sha256(authToken.encode("utf-8")).hexdigest())
            if user:
                history = db.get_order_history(user[0][3])
                db.closeConnection()
                return jsonify(history), 200
            else:
                db.closeConnection()
                return jsonify({"message": "User verification failed"}), 401
        else:
            return jsonify({"message": "Authentication required"}), 401
    except Exception as e:
        logger.error("Error retrieving order history: %s", e)
        return jsonify({"message": "Internal Server Error"}), 500


if __name__ == '__main__':
    app.run(debug=True)
