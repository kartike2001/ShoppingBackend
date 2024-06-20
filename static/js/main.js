document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const addToCartForm = document.getElementById('add-to-cart-form');
    const checkoutButton = document.getElementById('checkout-button');
    const cartItemsDiv = document.getElementById('cart-items');
    const logoutButton = document.getElementById('logout-button');
    const profileForm = document.getElementById('profile-form');
    const orderHistoryDiv = document.getElementById('order-history');
    const cartTotal = document.getElementById('cart-total');

    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            fetch('/createUser', {
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

            fetch('/verifyUser', {
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

            fetch('/addToCart', {
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

            fetch('/checkoutCart', {
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
            fetch('/logout', {
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

        fetch('/viewCart', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': `authToken=${authToken}`
            }
        })
            .then(response => response.json())
            .then(data => {
                cartItemsDiv.innerHTML = '';
                let total = 0;
                data.forEach(item => {
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

                        fetch('/removeFromCart', {
                            method: 'POST',
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

                        fetch('/updateCartQuantity', {
                            method: 'POST',
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

    if (profileForm) {
        profileForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const name = document.getElementById('profile-name').value;
            const email = document.getElementById('profile-email').value;
            const authToken = document.cookie.split('=')[1];

            fetch('/updateUserProfile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Cookie': `authToken=${authToken}`
                },
                body: JSON.stringify({ name, email })
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                });
        });

        loadUserProfile();
    }

    function loadUserProfile() {
        const authToken = document.cookie.split('=')[1];

        fetch('/userProfile', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': `authToken=${authToken}`
            }
        })
            .then(response => response.json())
            .then(data => {
                document.getElementById('profile-name').value = data.name;
                document.getElementById('profile-email').value = data.email;
            });
    }

    if (orderHistoryDiv) {
        loadOrderHistory();
    }

    function loadOrderHistory() {
        const authToken = document.cookie.split('=')[1];

        fetch('/orderHistory', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Cookie': `authToken=${authToken}`
            }
        })
            .then(response => response.json())
            .then(data => {
                orderHistoryDiv.innerHTML = '';
                Object.keys(data).forEach(session_id => {
                    const session = data[session_id];
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
