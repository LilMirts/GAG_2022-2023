import pytest
from pood import *

store = Store()


def test_add_to_stock():
    store.add_to_stock("milk", 3.53, 5)
    assert len(store.stock) == 1
    assert store.stock[0].name == "milk"
    store.add_to_stock("cheese", 2.34, 10)
    assert store.stock[1].stock_qty == 10
    store.add_to_stock("milk", 3.53, 2)
    assert store.stock[0].stock_qty == 7
    with pytest.raises(SameNameDifferentPriceException):
        store.add_to_stock("milk", 3.22, 3)


def test_register_client():
    store.register_client(32, 150.23)
    assert len(store.clients) == 1
    assert store.clients[0].is_gold_client is False
    with pytest.raises(ClientIdAlreadyTakenException):
        store.register_client(32, 132.22)


def test_cart_add_items():
    client = store.clients[0]
    client.cart.add_items(store.stock[0], 3)
    assert client.cart.items[store.stock[0]] == 3
    with pytest.raises(NotEnoughItemsInStockException):
        client.cart.add_items(store.stock[0], 6)
    with pytest.raises(NotEnoughItemsInStockException):
        client.cart.add_items(store.stock[1], 11)
    client.cart.add_items(store.stock[1], 10)
    assert len(client.cart.items) == 2


def test_cart_remove_items():
    client = store.clients[0]
    with pytest.raises(RemovableItemNotInCartException):
        client.cart.remove_items(Item("chips", 1.34, 15), 3)
    with pytest.raises(NotEnoughItemsInCartException):
        client.cart.remove_items(store.stock[0], 4)
    client.cart.remove_items(store.stock[1], 2)
    assert client.cart.items[store.stock[1]] == 8
    client.cart.remove_items(store.stock[1], 8)
    assert len(client.cart.items) == 1


def test_client_checkout():
    client = store.clients[0]
    client.cart.add_items(store.stock[1], 6)
    client.balance = 23.34
    with pytest.raises(NotEnoughMoneyException):
        client.checkout()
    client.is_gold_client = True
    client.checkout()
    assert client.balance == 1.17
    assert len(client.cart.items) == 0
    assert store.stock[0].stock_qty == 4
    assert store.stock[1].stock_qty == 4


def test_client_history():
    client = store.clients[0]
    client.cart.add_items(store.stock[1], 2)
    client.balance = 30.76
    client.checkout()
    date = datetime.now().strftime('%m.%d.%Y')
    assert client.get_history() == f"{date}\n" \
                                   "  cheese x2\n" \
                                   "\n" \
                                   f"{date}\n" \
                                   "  milk x3\n" \
                                   "  cheese x6"


def test_store_history():
    assert list(store.get_history().values()) == [{store.stock[0]: 3, store.stock[1]: 6}, {store.stock[1]: 2}]
