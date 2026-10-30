# product.py
# Product: ABSTRACT base class for every product (SRP: represent and manage ONE product).
# It cannot be created directly. Every product must be physical or digital.
# It does not load/save files, show menus or ask the user for input.

from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        # Double underscore = "private" by convention (encapsulation).
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---------- read-only access (getters) ----------
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    # ---------- behaviour shared by all products ----------
    def update_stock(self, quantity):
        """Change stock by +/- quantity. Negative = sale, positive = restock.
        Returns True if updated, False if there is not enough stock."""
        if self.__stock + quantity < 0:
            return False
        self.__stock += quantity
        return True

    def display_information(self):
        """Print the common product details. Subclasses add their own details."""
        print(f"{self.__product_id:<6} {self.__name:<15} ${self.__price:<8.2f} Qty: {self.__stock}")

    def to_dict(self):
        """Common fields for saving to JSON. Subclasses add their own."""
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    # ---------- behaviour every subclass MUST provide ----------
    @abstractmethod
    def get_fulfilment_info(self):
        """Return a message about how this product is delivered."""
        pass
