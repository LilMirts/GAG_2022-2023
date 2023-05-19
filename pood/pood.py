from datetime import datetime


class Client:

    def __init__(self, id, balance, is_gold_client=False):
        self.id = id
        self.balance = balance
        self.is_gold_client = is_gold_client

        self.cart = ShoppingCart()
        self.history = {}

    def checkout(self):
        total_cost = self.cart.get_total_cost
        if self.is_gold_client:
            total_cost = total_cost * 0.9

        if total_cost > self.balance:
            raise NotEnoughMoneyException()

        for item in self.cart.items:
            item.buy(self.cart.items[item])
        self.history[datetime.now()] = self.cart.items  # items = {milk: 3}
        self.cart.clear()

    def get_history(self):
        history_str = ""
        for time in sorted(self.history.keys(), reverse=True):
            history_str += time.strftime("%m.%d.%Y") + "\n"
            items = self.history[time]
            for item in items:
                history_str += f"  {item} x{items[item]}\n"
            history_str += "\n"


class NotEnoughMoneyException(Exception):
    pass


class Item:

    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.stock_qty = qty

    def __repr__(self):
        return self.name

    def buy(self, qty):
        self.stock_qty -= qty


class ShoppingCart:

    def __init__(self):
        self.items = {}  # {milk: 3}

    def get_total_cost(self):
        total = 0
        for item in self.items:
            total += self.items[item] * item.price
        return total

    def add_items(self, item, qty):
        if item.stock_qty < qty:
            raise NotEnoughItemsInStockException
        else:
            if item in self.items:
                self.items[item] += qty
            else:
                self.items[item] = qty

    def remove_items(self, item, qty):
        if item not in self.items:
            raise RemovableItemNotInCartException()
        if self.items[item] < qty:
            raise NotEnoughItemsInCartException()
        self.items[item] -= qty
        if self.items[item] == 0:
            del self.items[item]

    def clear(self):
        self.items = {}


class NotEnoughItemsInStockException(Exception):
    pass


class RemovableItemNotInCartException(Exception):
    pass


class NotEnoughItemsInCartException(Exception):
    pass


class Store:

    def __init__(self):
        self.stock = []
        self.clients = []

    def register_client(self, id, balance, is_gold_client=False):
        for client in self.clients:
            if client.id == id:
                raise ClientIdAlreadyTakenException()
        self.clients.append(Client(id, balance, is_gold_client))

    def add_to_stock(self, name, price, qty):
        for item in self.stock:
            if item.name == name:
                if item.price == price:
                    item.stock_qty += qty
                    return
                else:
                    raise SameNameDifferentPriceException()
        self.stock.append(Item(name, price, qty))

    def get_history(self):
        history = {}
        for client in self.clients:
            history.update(client.history)
        return history


class SameNameDifferentPriceException(Exception):
    pass


class ClientIdAlreadyTakenException(Exception):
    pass
