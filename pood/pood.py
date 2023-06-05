from datetime import datetime


class Client:
    
    def __init__(self, id, balance, is_gold_client=False):
        """Initialize the Client class, given the id, balance and type of the client."""
        self.id = id
        self.balance = balance
        self.is_gold_client = is_gold_client

        self.cart = ShoppingCart()
        self.history = {}

    def checkout(self):
        """Make a purchase, removing the total cost of the cart from client's balance and clearing the cart."""
        total_cost = self.cart.get_total_cost()
        if self.is_gold_client:
            total_cost = round(total_cost * 0.9, 2)

        if total_cost > self.balance:
            raise NotEnoughMoneyException()
        self.balance = round(self.balance - total_cost, 2)

        for item in self.cart.items:
            item.buy(self.cart.items[item])
        self.history[datetime.now()] = self.cart.items  # items = {milk: 3}
        self.cart.clear()

    def get_history(self):
        """Return the history of the client's purchases as a string."""
        history_str = ""
        for time in sorted(self.history.keys(), reverse=True):
            history_str += time.strftime("%m.%d.%Y") + "\n"
            items = self.history[time]
            for item in items:
                history_str += f"  {item} x{items[item]}\n"
            history_str += "\n"
        return history_str[:-2]


class NotEnoughMoneyException(Exception):
    pass


class Item:

    def __init__(self, name, price, qty):
        """Initialize the Item class, given the name, price and stock quantity of the item."""
        self.name = name
        self.price = price
        self.stock_qty = qty

    def __repr__(self):
        """Represent the item as a string."""
        return self.name

    def buy(self, qty):
        """Remove given quantity of the item from stock, if possible."""
        if qty > self.stock_qty:
            raise NotEnoughItemsInStockException
        self.stock_qty -= qty


class ShoppingCart:

    def __init__(self):
        """Initialize the ShoppingCart class without any items in it."""
        self.items = {}  # {milk: 3}

    def get_total_cost(self):
        """Return the total cost of items in the shopping cart."""
        total = 0
        for item in self.items:
            total += self.items[item] * item.price
        return total

    def add_items(self, item, qty):
        """Add the given quantity of given item to the cart."""
        if item in self.items:
            if item.stock_qty - self.items[item] < qty:
                raise NotEnoughItemsInStockException
            else:
                self.items[item] += qty
        else:
            if item.stock_qty < qty:
                raise NotEnoughItemsInStockException
            else:
                self.items[item] = qty

    def remove_items(self, item, qty):
        """Remove the given quantity of given item from the cart."""
        if item not in self.items:
            raise RemovableItemNotInCartException()
        if self.items[item] < qty:
            raise NotEnoughItemsInCartException()
        self.items[item] -= qty
        if self.items[item] == 0:
            del self.items[item]

    def clear(self):
        """Empty the cart."""
        self.items = {}


class NotEnoughItemsInStockException(Exception):
    pass


class RemovableItemNotInCartException(Exception):
    pass


class NotEnoughItemsInCartException(Exception):
    pass


class Store:

    def __init__(self):
        """Initialize the Store class."""
        self.stock = []
        self.clients = []

    def register_client(self, id, balance, is_gold_client=False):
        """Add a client to the store."""
        for client in self.clients:
            if client.id == id:
                raise ClientIdAlreadyTakenException()
        self.clients.append(Client(id, balance, is_gold_client))

    def add_to_stock(self, name, price, qty):
        """Add an item to stock or increase the quantity of an item in stock."""
        for item in self.stock:
            if item.name == name:
                if item.price == price:
                    item.stock_qty += qty
                    return
                else:
                    raise SameNameDifferentPriceException()
        self.stock.append(Item(name, price, qty))

    def get_history(self):
        """Return the history of purchases in the store as a dictionary."""
        history = {}
        for client in self.clients:
            history.update(client.history)
        return history


class SameNameDifferentPriceException(Exception):
    pass


class ClientIdAlreadyTakenException(Exception):
    pass
