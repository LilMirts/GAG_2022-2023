from datetime import datetime

class Client:
    def __init__(self, name, balance, is_gold_client=False):
        self.name = name
        self.balance = balance
        self.is_gold_client = is_gold_client

        self.cart = ShoppingCart()
        self.history = {}

    def checkout(self):
        if self.cart.total_cost > self.balance:
            raise NotEnoughMoneyException()

        self.history[datetime.now()] = self.cart.items  # items = {"milk": 3}
        self.cart.clear()

    def get_history(self):
        history_str = ""
        for time in sorted(self.history.keys(), reverse=True):
            history_str += time.strftime("%m.%d.%Y") + "\n"
            items = self.history[time]
            for item in items:
                history_str += f"{item} x{items[item]}\n"
            history_str += "\n"


class NotEnoughMoneyException(Exception):
    pass

