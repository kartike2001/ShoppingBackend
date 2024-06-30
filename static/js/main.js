document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const addToCartForm = document.getElementById('add-to-cart-form');
    const checkoutButton = document.getElementById('checkout-button');
    const cartItemsDiv = document.getElementById('cart-items');
    const logoutButton = document.getElementById('logout-button');
    const orderHistoryDiv = document.getElementById('order-history');
    const cartTotal = document.getElementById('cart-total');
    const userNameHeader = document.getElementById('user-name');

    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            fetch('/users/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, email, password })
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    if (data.message === "User created successfully") {
                        window.location.href = '/login';
                    }
                });
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            fetch('/users/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    if (data.message === "User verified successfully") {
                        document.cookie = `authToken=${data.authToken}; path=/`;
                        window.location.href = '/cart';
                    }
                });
        });
    }

    if (addToCartForm) {
        addToCartForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const itemName = document.getElementById('item-name').value;
            const itemPrice = document.getElementById('item-price').value;
            const itemQuantity = document.getElementById('item-quantity').value;
            const authToken = document.cookie.split('=')[1];

            fetch('/cart/items', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `authToken=${authToken}`
                },
                body: JSON.stringify({ itemName, itemPrice, itemQuantity })
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    loadCart();
                });
        });
    }

    if (checkoutButton) {
        checkoutButton.addEventListener('click', function () {
            const authToken = document.cookie.split('=')[1];

            fetch('/cart/checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `authToken=${authToken}`
                }
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    loadCart();
                });
        });

        loadCart();
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            fetch('/users/logout', {
                method: 'POST'
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    window.location.href = '/login';
                });
        });
    }

    function loadCart() {
        const authToken = document.cookie.split('=')[1];

        fetch('/cart/items', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': `authToken=${authToken}`
            }
        })
            .then(response => response.json())
            .then(data => {
                userNameHeader.textContent = `Hello, ${data.userName}`;
                cartItemsDiv.innerHTML = '';
                let total = 0;
                data.items.forEach(item => {
                    const itemDiv = document.createElement('div');
                    itemDiv.innerHTML = `Name: ${item.itemName}, Price: ${item.itemPrice}, Quantity: 
                    <input type="number" value="${item.itemQuantity}" data-id="${item.id}" class="update-quantity">
                    <button data-id="${item.id}" class="remove-item">Remove</button>`;
                    cartItemsDiv.appendChild(itemDiv);
                    total += item.itemPrice * item.itemQuantity;
                });

                cartTotal.textContent = total.toFixed(2);

                document.querySelectorAll('.remove-item').forEach(button => {
                    button.addEventListener('click', function () {
                        const cart_id = this.getAttribute('data-id');
                        const authToken = document.cookie.split('=')[1];

                        fetch('/cart/items', {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json',
                                'Cookie': `authToken=${authToken}`
                            },
                            body: JSON.stringify({ cart_id })
                        })
                            .then(response => response.json())
                            .then(data => {
                                alert(data.message);
                                loadCart();
                            });
                    });
                });

                document.querySelectorAll('.update-quantity').forEach(input => {
                    input.addEventListener('change', function () {
                        const cart_id = this.getAttribute('data-id');
                        const itemQuantity = this.value;
                        const authToken = document.cookie.split('=')[1];

                        fetch('/cart/items', {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                'Cookie': `authToken=${authToken}`
                            },
                            body: JSON.stringify({ cart_id, itemQuantity })
                        })
                            .then(response => response.json())
                            .then(data => {
                                alert(data.message);
                                loadCart();
                            });
                    });
                });
            });
    }

    if (orderHistoryDiv) {
        const authToken = document.cookie.split('=')[1];

        fetch('/orders/history', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': `authToken=${authToken}`
            }
        })
            .then(response => response.json())
            .then(data => {
                userNameHeader.textContent = `Hello, ${data.userName}`;
                orderHistoryDiv.innerHTML = '';
                Object.keys(data.sessions).forEach(session_id => {
                    const session = data.sessions[session_id];
                    const sessionDiv = document.createElement('div');
                    sessionDiv.innerHTML = `<h3>Order Date: ${session.orderDate}</h3>`;
                    session.items.forEach(item => {
                        const itemDiv = document.createElement('div');
                        itemDiv.textContent = `Name: ${item.itemName}, Price: ${item.itemPrice}, Quantity: ${item.itemQuantity}`;
                        sessionDiv.appendChild(itemDiv);
                    });
                    orderHistoryDiv.appendChild(sessionDiv);
                });
            });
    }
});