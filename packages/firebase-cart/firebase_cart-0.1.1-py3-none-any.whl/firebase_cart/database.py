import firebase_admin
from firebase_admin import credentials, firestore
from .models import FirebaseConfig
from .logging import logger

class FirebaseDB:
    def __init__(self, config: FirebaseConfig):
        # cred = credentials.Certificate(config.credentials)
        # if config.database_url:
        #     firebase_admin.initialize_app(cred, {'databaseURL': config.database_url})
        # else:
        #     firebase_admin.initialize_app(cred)
        # self.db = firestore.client()
        try:
            if not firebase_admin._apps:  # Check if the app is not already initialized
                cred = credentials.Certificate(config.credentials)
                firebase_admin.initialize_app(cred, {'databaseURL': config.database_url, "storageBucket": config.bucket})
            self.db = firestore.client()
        except Exception as e:
            logger.error(f"storage init error, {e}")
            raise
        finally:
            logger.debug("storage closed")


    def get_cart_ref(self, cart_id: str):
        """
        Retrieves a reference to a specific order by its ID.
        Useful for getting or modifying a specific cart.

        Parameters:
        - cart_id: The ID of the cart document.

        Returns:
        - A Firestore document reference to the specific cart.
        """
        return self.db.collection("carts").document(cart_id)
    
    def get_order_ref(self, order_id: str):
        """
        Retrieves a reference to a specific order by its ID.
        Useful for getting or modifying a specific order.

        Parameters:
        - order_id: The ID of the order document.

        Returns:
        - A Firestore document reference to the specific order.
        """
        return self.db.collection("orders").document(order_id)
    
    def get_all_orders_ref(self):
        """
        Retrieves a reference to the Firestore collection that contains all orders.
        This method is used for admin users who can access all orders.
        """
        return self.db.collection("orders")

    def get_user_orders_ref(self, user_id: str):
        """
        Retrieves a query that references only the orders for a specific user.
        This method is used for non-admin users who can only access their own orders.

        Parameters:
        - user_id: The ID of the user whose orders need to be retrieved.

        Returns:
        - A Firestore query that can be used to fetch orders for a specific user.
        """
        return self.db.collection("orders").where("user_id", "==", user_id)

    