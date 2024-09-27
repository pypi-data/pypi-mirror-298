from .models import CartItem, Cart, FirebaseConfig
from .database import FirebaseDB
from decimal import Decimal

class CartHandler:
    TAX_RATE = Decimal("0.05")  # 5% tax rate
    SHIPPING_COST = Decimal("2500.00")  # Flat shipping cost

    def __init__(self, config: FirebaseConfig):
        self.db = FirebaseDB(config)

    def _create_context(self):
        return {
            "user_agent": 'CustomUserAgent/1.0'
        }

    def create_cart(self, cart_id: str, customer_id: str = "", email: str = ""):
        cart_ref = self.db.get_cart_ref(cart_id)

        # Create context automatically
        context = self._create_context()

        current_items = []

        cart_ref.set({"items": current_items, "context": context, "customer_id": customer_id, "email": email})
        return {"message": "Cart created successfully", "cart_id": cart_id}


    def add_to_cart(self, cart_id: str, item: CartItem, customer_id: str = "", email: str = ""):
        cart_ref = self.db.get_cart_ref(cart_id)
        cart = cart_ref.get()

        # Create context automatically
        context = self._create_context()

        if cart.exists:
            current_items = cart.to_dict().get("items", [])
            for i, existing_item in enumerate(current_items):
                if existing_item["item_id"] == item.item_id:
                    current_items[i]["quantity"] += item.quantity
                    break
            else:
                current_items.append(item.model_dump())
        else:
            current_items = [item.model_dump()]

        cart_ref.set({"items": current_items, "context": context, "customer_id": customer_id, "email": email})
        return {"message": "Item added to cart"}

    def get_cart(self, cart_id: str):
        cart = self.db.get_cart_ref(cart_id).get()
        if not cart.exists:
            return None
        cart_details = cart.to_dict()

        # Calculate subtotal
        items = [CartItem(**item) for item in cart_details.get("items", [])]
        subtotal = sum(item.price * item.quantity for item in items)

        # Calculate tax and shipping
        tax_total = subtotal * self.TAX_RATE
        delivery_fee = self.SHIPPING_COST
        total = subtotal + tax_total + delivery_fee

        return Cart(
            cart_id=cart_id,
            customer_id=cart_details.get("customer_id", ""),
            email=cart_details.get("email", ""),
            items=[CartItem(**item) for item in cart_details.get("items", [])],
            shipping_method=cart_details.get("shipping_method", {}),
            shipping_address=cart_details.get("shipping_address", {}),
            billing_address=cart_details.get("billing_address", {}),
            subtotal=subtotal,
            tax_total=tax_total,
            delivery_fee=delivery_fee,
            total=total,
            payment_session=cart_details.get("payment_session", {})
        )

    def update_cart(self, cart: Cart):
        cart_ref = self.db.get_cart_ref(cart.cart_id)
        cart_ref.set(cart.model_dump())
        return {"message": "Cart updated successfully"}

    def update_cart_quantity(self, cart_id: str, product_id: str, quantity: int):
        """
        Update the quantity of a specific item in the cart based on product_id.
        """
        if quantity <= 0:
            return {"error": "Quantity must be greater than zero"}

        cart_ref = self.db.get_cart_ref(cart_id)
        cart = cart_ref.get()

        if not cart.exists:
            return {"error": "Cart does not exist"}

        current_items = cart.to_dict().get("items", [])

        # Find the item and update the quantity
        for i, item in enumerate(current_items):
            if item["product_id"] == product_id:
                current_items[i]["quantity"] = quantity
                break
        else:
            return {"error": "Item not found in cart"}

        # Update the cart with the new quantity
        cart_data = cart.to_dict()
        cart_data["items"] = current_items
        cart_ref.set(cart_data)

        return {"message": "Item quantity updated"}


    def update_cart_details(self, cart_id: str, cart_data: dict):
        """
        Update cart details dynamically with any fields provided in cart_data.
        """
        cart_ref = self.db.get_cart_ref(cart_id)
        cart = cart_ref.get()

        if not cart.exists:
            return {"error": "Cart does not exist"}

        # Get existing cart data
        existing_cart_data = cart.to_dict()

        # Update the cart with dynamic fields from cart_data
        existing_cart_data.update(cart_data)

        # Save the updated cart back to Firebase
        cart_ref.set(existing_cart_data)

        return {"message": "Cart details updated successfully"}

    def clear_cart(self, cart_id: str):
        self.db.get_cart_ref(cart_id).delete()
        return {"message": "Cart cleared successfully"}

    def remove_from_cart(self, cart_id: str, item_id: str):
        """
        Remove a specific item from the cart based on item_id.
        """
        cart_ref = self.db.get_cart_ref(cart_id)
        cart = cart_ref.get()

        if not cart.exists:
            return {"error": "Cart does not exist"}

        current_items = cart.to_dict().get("items", [])

        # Filter out the item to be removed by item_id
        updated_items = [item for item in current_items if item.get("item_id") != item_id]

        if len(updated_items) == len(current_items):
            return {"error": "Item not found in cart"}

        # Update the cart in Firebase with the remaining items
        cart_data = cart.to_dict()
        cart_data["items"] = updated_items
        cart_ref.set(cart_data)

        return {"message": "Item removed from cart"}

