# Shopping Cart Service

This is a simple Shopping Cart service implemented using Flask and PostgreSQL. The service allows users to:
- Register and log in.
- Add items to a shopping cart.
- View items in the cart.
- Remove items from the cart.
- Update the quantity of items in the cart.
- Checkout the cart.
- View order history.
- View and update user profile.
- Logout.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Postman (for API testing)
- There is a frontend as well if you prefer it over using Postman - http://localhost:5000/

### Setting Up the Project

1. **Clone the repository:**

```sh
git clone 
```

2. **Start the Docker containers:**

```sh
docker-compose up --build
```

This command will build the Docker images and start the containers for the Flask web server and the PostgreSQL database.

### API Endpoints and Testing with Postman

#### 1. Register a New User 

- **URL:** `http://localhost:5000/createUser`
- **Method:** `POST`
- **Headers:** 
  - `Content-Type: application/json`
- **Body:**

```json
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "password123"
}
```

#### 2. Log in as the User

- **URL:** `http://localhost:5000/verifyUser`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**

```json
{
    "email": "john.doe@example.com",
    "password": "password123"
}
```

#### 3. Add Items to the Cart

- **URL:** `http://localhost:5000/addToCart`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Replace `<your_auth_token>` with the token received in the login response, once selected on Postman you can uncheck the header for a GET request or whenever not needed)
- **Body:**

```json
{
    "itemName": "Apple",
    "itemPrice": 0.99,
    "itemQuantity": 10
}
```
```json
{
    "itemName": "Banana",
    "itemPrice": 0.49,
    "itemQuantity": 3
}
```

#### 4. View Cart

- **URL:** `http://localhost:5000/viewCart`
- **Method:** `GET`
- **Headers:**
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

#### 5. Remove Item from Cart

- **URL:** `http://localhost:5000/removeFromCart`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)
- **Body:**

```json
{
    "cart_id": 1  // Replace with the actual cart item id you want to remove
}
```

#### 6. Update Cart Quantity

- **URL:** `http://localhost:5000/updateCartQuantity`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

```json
{
    "cart_id": 1,  // Replace with the actual cart item id you want to update
    "itemQuantity": 5
}
```

#### 7. Checkout Cart

- **URL:** `http://localhost:5000/checkoutCart`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

#### 8. View Order History

- **URL:** `http://localhost:5000/orderHistory`
- **Method:** `GET`
- **Headers:**
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

#### 9. View User Profile

- **URL:** `http://localhost:5000/userProfile`
- **Method:** `GET`
- **Headers:**
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

#### 10. Update User Profile

- **URL:** `http://localhost:5000/updateUserProfile`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)
- **Body:**

```json
{
    "name": "John Doe",
    "email": "john.doe@example.com"
}
```

#### 11. Logout

- **URL:** `http://localhost:5000/logout`
- **Method:** `POST`
