# product.py
# Product: represents ONE product and manages its own state (SRP).
# It does not load/save files, show menus or ask the user for input.


class Product:
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

    # ---------- behaviour ----------
    def update_stock(self, quantity):
        """Change stock by +/- quantity. Negative = sale, positive = restock.
        Returns True if updated, False if there is not enough stock."""
        if self.__stock + quantity < 0:
            return False
        self.__stock += quantity
        return True

    def display_information(self):
        """Print this product's details."""
        print(f"{self.__product_id:<6} {self.__name:<15} ${self.__price:<8.2f} Qty: {self.__stock}")

    def to_dict(self):
        """Plain dictionary of this product, used when saving to JSON."""
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }
