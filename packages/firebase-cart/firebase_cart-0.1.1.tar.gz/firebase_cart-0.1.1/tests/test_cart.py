import pytest
from firebase_cart import CartHandler, CartItem, Cart, FirebaseConfig, CartContext
from unittest.mock import MagicMock, patch

@pytest.fixture
def firebase_config():
    return FirebaseConfig(
        credentials={"type": "service_account", "project_id": "test-project"},
        database_url="https://test-project.firebaseio.com"
    )

@pytest.fixture
def cart_handler(firebase_config):
    with patch('firebase_cart.database.credentials.Certificate'), \
        patch('firebase_cart.database.firebase_admin.initialize_app'), \
        patch('firebase_cart.database.firestore.client'):
        return CartHandler(firebase_config)

def test_add_to_cart(cart_handler):
    cart_handler.db.get_cart_ref = MagicMock()
    cart_handler.db.get_cart_ref().get.return_value.exists = False

    item = CartItem(product_id="123", quantity=2)
    context = CartContext(ip="127.0.0.1", user_agent="test-agent")
    result = cart_handler.add_to_cart("user1", item, context)

    assert result == {"message": "Item added to cart"}
    cart_handler.db.get_cart_ref().set.assert_called_once()

def test_get_cart(cart_handler):
    mock_cart_data = {
        "items": [{"product_id": "123", "quantity": 2}],
        "context": {"ip": "127.0.0.1", "user_agent": "test-agent"}
    }
    cart_handler.db.get_cart_ref = MagicMock()
    cart_handler.db.get_cart_ref().get.return_value.exists = True
    cart_handler.db.get_cart_ref().get.return_value.to_dict.return_value = mock_cart_data

    cart = cart_handler.get_cart("user1")

    assert isinstance(cart, Cart)
    assert cart.user_id == "user1"
    assert len(cart.items) == 1
    assert cart.items[0].product_id == "123"
    assert cart.context.ip == "127.0.0.1"
