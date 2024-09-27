# Firebase Cart

A Firebase-based cart package for Python applications.

## Installation

```
pip install firebase_cart
```

## Usage

```python
from firebase_cart import CartHandler, CartItem, FirebaseConfig

# Initialize with your Firebase credentials
firebase_config = FirebaseConfig(
    credentials={
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "your-private-key",
        # ... other credential fields ...
    },
    database_url="https://your-project-id.firebaseio.com"  # Optional
)

cart_handler = CartHandler(firebase_config)

# Add item to cart
item = CartItem(product_id="123", quantity=2)
cart_handler.add_to_cart("user123", item)

# Get cart
cart = cart_handler.get_cart("user123")

# Update cart
cart.items.append(CartItem(product_id="456", quantity=1))
cart_handler.update_cart(cart)

# Clear cart
cart_handler.clear_cart("user123")
```

## API Reference

### CartHandler

* `__init__(config: FirebaseConfig)`: Initialize the CartHandler with Firebase configuration.
* `add_to_cart(user_id: str, item: CartItem, context: Optional[CartContext] = None)`: Add an item to the cart.
* `get_cart(user_id: str) -> Optional[Cart]`: Retrieve a user's cart.
* `update_cart(cart: Cart)`: Update an entire cart.
* `clear_cart(user_id: str)`: Clear a user's cart.

### CartItem

* `product_id: str`: The ID of the product.
* `quantity: int`: The quantity of the product.


### CartContext

* `ip: Optional[str]`: The IP address of the user.
* `user_agent: Optional[str]`: The user agent of the client.
* `additional_info: Optional[Dict[str, Any]]`: Any additional context information.

## Error Handling

The package raises `FirebaseError` for any Firebase-related errors. Handle these appropriately in your application.

## Logging

The package logs important events and errors. Configure logging in your application to capture these logs.