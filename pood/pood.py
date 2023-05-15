from datetime import datetime


class Client:
    def __init__(self, name, balance, is_gold_client=False):
        self.name = name
        self.balance = balance
        self.is_gold_client = is_gold_client

        self.cart = ShoppingCart()
        self.history = {}

    def checkout(self):
        total_cost = self.cart.total_cost
        if self.is_gold_client:
            total_cost = total_cost * 0.9

        if total_cost > self.balance:
            raise NotEnoughMoneyException()

        for item in self.cart.items:
            item.buy(self.cart.items[qty])
        self.history[datetime.now()] = self.cart.items  # items = {"milk": 3}
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
        self.qty = qty

    def __repr__(self):
        return self.name

    def buy(self, qty):
        self.qty -= qty


class ShoppingCart:
    def __init__(self):
        self.items = {}  # {"milk": 3}

    def add_items(self, item, qty):
        if item.qty < qty:
            raise NotEnoughItemsException
        else:
            if item in self.items:
                self.items[item] += qty
            else:
                self.items[item] = qty

    def remove_items(self, item, qty):
        pass


class NotEnoughItemsException(Exception):
    pass
