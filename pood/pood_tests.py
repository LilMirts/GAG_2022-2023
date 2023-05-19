import pytest
from pood import *

store = Store()


def test_add_to_stock():
    store.add_to_stock("milk", 3.53, 5)
    assert len(store.stock) == 1
    assert store.stock[0].name == "milk"
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
