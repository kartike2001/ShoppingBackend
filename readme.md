# Shopping Cart Service

This is a simple Shopping Cart service implemented using Flask and PostgreSQL. The service allows users to:
- Register and log in.
- Add items to a shopping cart.
- View items in the cart.
- Remove items from the cart.
- Update the quantity of items in the cart.
- Checkout the cart.
- View order history.
- Logout.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Postman (for API testing)
- There is a frontend as well if you prefer it over using Postman - http://localhost:8080/

### Setting Up the Project

1. **Clone the repository:**

```sh
git clone https://github.com/kartike2001/ShoppingBackend.git
```

2. **CD into the repository directory**

3. **Start the Docker containers:**
Make sure that the docker app is running
```sh
docker-compose up --build
```

This command will build the Docker images and start the containers for the Flask web server and the PostgreSQL database.

### API Endpoints and Testing with Postman

#### 1. Register a New User 

- **URL:** `http://localhost:8080/users`
- **Method:** `POST`
- **Headers:** 
  - `Content-Type: application/json`
- **Body:**

To test on Postman select raw JSON

```json
{
    "name": "Kartike Chaurasia",
    "email": "kartike.chau@philips.com",
    "password": "password123"
}
```

#### 2. Log in as the User

- **URL:** `http://localhost:8080/users/verify`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**

To test on Postman select raw JSON

```json
{
    "email": "kartike.chau@philips.com",
    "password": "password123"
}
```

#### 3. Add Items to the Cart

- **URL:** `http://localhost:8080/cart/items`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Replace `<your_auth_token>` with the token received in the login response, once selected on Postman you can uncheck the header for a GET request or whenever not needed)
- **Body:**

Won't be able to enter a negative `itemPrice` or a zero/negative `itemQuantity`

To test on Postman select raw JSON

```json
{
    "itemName": "IntelliVue MX400",
    "itemPrice": 9999.99,
    "itemQuantity": 10
}
```
If the price and Item name are same it should update the quantity
```json
{
    "itemName": "IntelliVue MX400",
    "itemPrice": 9999.99,
    "itemQuantity": 3
}
```
```json
{
    "itemName": "IntelliVue MX850",
    "itemPrice": 19999.49,
    "itemQuantity": 3
}
```

#### 4. View Cart

- **URL:** `http://localhost:8080/cart`
- **Method:** `GET`
- **Headers:**
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

#### 5. Update Cart Quantity

- **URL:** `http://localhost:8080/cart/items`
- **Method:** `PUT`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

Replace with the actual cart item id you want to update

To test on Postman select raw JSON

```json
{
    "cart_id": 1,
    "itemQuantity": 5
}
```

#### 6. Remove Item from Cart

- **URL:** `http://localhost:8080/cart/items`
- **Method:** `DELETE`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)
- **Body:**

To test on Postman select raw JSON

```json
{
    "cart_id": 1
}
```

#### 7. Checkout Cart

- **URL:** `http://localhost:8080/cart/checkout`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

#### 8. View Order History

- **URL:** `http://localhost:8080/orders/history`
- **Method:** `GET`
- **Headers:**
  - `Cookie: authToken=<your_auth_token>` (Make sure header is checked)

#### 9. Logout

- **URL:** `http://localhost:8080/users/logout`
- **Method:** `POST`