from .utils import generate_id
from .models import Order, FirebaseConfig, CartItem
from .database import FirebaseDB
from decimal import Decimal
import uuid
from datetime import datetime

class OrderHandler:
    TAX_RATE = Decimal("0.10")  # 10% tax rate
    SHIPPING_COST = Decimal("2500")  # Flat shipping cost

    def __init__(self, config: FirebaseConfig):
        self.db = FirebaseDB(config)

    def create_order(self, user_id: str, cart_id: str):
        """
        Create a new order based on the cart_id.
        """
        # Fetch the cart data using cart_id
        cart_ref = self.db.get_cart_ref(cart_id)
        cart = cart_ref.get()

        if not cart.exists:
            return {"error": "Cart does not exist"}

        cart_data = cart.to_dict()

        # Calculate subtotal
        items = [CartItem(**item) for item in cart_data.get("items", [])]
        subtotal = sum(item.price * item.quantity for item in items)

        # Calculate tax and shipping
        tax_total = subtotal * self.TAX_RATE
        delivery_fee = self.SHIPPING_COST
        total = subtotal + tax_total + delivery_fee

        # Convert Decimal values to float for Firestore
        subtotal_float = float(subtotal)
        tax_total_float = float(tax_total)
        delivery_fee_float = float(delivery_fee)
        total_float = float(total)

        # Create order details
        order_id = generate_id(prefix='order_')
        
        order_data = {
            "order_id": order_id,
            "user_id": user_id,
            "cart_id": cart_id,
            "fulfillment_status": "not_fulfilled",
            "line_items": [item.model_dump() for item in items],
            "subtotal": subtotal_float,
            "tax_total": tax_total_float,
            "delivery_fee": delivery_fee_float,
            "total": total_float,
            "status": "pending",  # Default order status
            "payment_status": "awaiting",
            "created_at": datetime.utcnow().isoformat(),
            "shipping_method":cart_data.get("shipping_method", {}),
            "shipping_address": cart_data.get("shipping_address"),
            "billing_address": cart_data.get("billing_address"),
            "email": cart_data.get("email"),
            "payment_session":cart_data.get("payment_session", {}),
            "fulfillments": []
        }

        # Save order to Firebase
        order_ref = self.db.get_order_ref(order_id)
        order_ref.set(order_data)

        # Optionally clear the cart after order creation
        # self.db.get_cart_ref(cart_id).delete()

        return {
            "message": "Order created successfully",
            "order_id": order_id,
            "total": total,
            "order": order_data
        }
    
    def get_orders(self, user_id: str, limit: int = 10):
        orders_ref = self.db.get_user_orders_ref(user_id)

        # Fetch orders with pagination
        query = orders_ref.order_by("created_at").limit(limit)
        orders_snapshot = query.get()

        orders = [order.to_dict() for order in orders_snapshot]
        return orders
    
    def get_paginated_orders(self, page: int = 1, limit: int = 10):
        """
        Paginate the retrieval of orders with total count and pages.
        
        Parameters:
        - user_id: The user making the request.
        - is_admin: If true, admin can retrieve all orders, otherwise only the user's orders.
        - page: The current page number.
        - limit: The number of orders to retrieve per page.

        Returns:
        - A dictionary containing orders, current page, limit, total count, and total pages.
        """
        # Step 1: Determine if it's admin or user-specific retrieval
        orders_ref = self.db.get_all_orders_ref()

        # Step 2: Get the total count of orders (this might be expensive on large collections)
        total_count = len(orders_ref.get())  # Fetch all to count them

        # Step 3: Calculate total number of pages
        total_pages = (total_count + limit - 1) // limit  # ceiling division

        # Step 4: Calculate offset based on current page
        offset = (page - 1) * limit

        # Step 5: Paginate and fetch only the required documents for the current page
        query = orders_ref.order_by("created_at").limit(limit).offset(offset)
        orders_snapshot = query.get()

        orders = []
        for order in orders_snapshot:
            orders.append(order.to_dict())

        return {
            "orders": orders,
            "page": page,
            "limit": limit,
            "total_count": total_count,
            "total_pages": total_pages
        }


    def get_order(self, user_id: str, order_id: str, is_admin: bool):
        """
        Get order details by order ID. 
        Non-admin users can only retrieve their own orders.
        """
        order_ref = self.db.get_order_ref(order_id)
        order = order_ref.get()

        if not order.exists:
            return {"error": "Order does not exist"}

        order_data = order.to_dict()

        # Restrict access for non-admin users
        if not is_admin and order_data.get("user_id") != user_id:
            return {"error": "Permission denied. You can only retrieve your own orders."}

        # return order_data
        return Order(**order.to_dict())

    def update_order(self, order_id: str, update_data: dict, is_admin: bool):
        """
        Update order details dynamically. 
        Only admins can update orders.
        """
        if not is_admin:
            return {"error": "Permission denied. Only admins can update orders."}

        order_ref = self.db.get_order_ref(order_id)
        order = order_ref.get()

        if not order.exists:
            return {"error": "Order does not exist"}

        order_data = order.to_dict()
        order_data.update(update_data)

        order_ref.set(order_data)

        return {"message": "Order updated successfully"}

    def list_orders_for_user(self, user_id: str, is_admin: bool):
        """
        List all orders for a specific user.
        Admins can view all orders, non-admins can view only their own.
        """
        if is_admin:
            orders_ref = self.db.get_all_orders_ref()
        else:
            orders_ref = self.db.get_user_orders_ref(user_id)

        orders = orders_ref.get()

        if not orders.exists:
            return {"message": "No orders found"}

        return [order.to_dict() for order in orders]
