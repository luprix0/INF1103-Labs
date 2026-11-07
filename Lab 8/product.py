from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier    

    # ---------- read-only access (getters) ----------
    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    # ---------- behaviour shared by all products ----------
    def update_stock(self, quantity: int) -> bool:
        """Change stock by +/- quantity. Negative = sale, positive = restock.
        Returns True if updated. Returns False (and changes nothing) if the
        stock would go below zero. Every subclass keeps this meaning (LSP)."""
        if self.__stock + quantity < 0:
            return False
        self.__stock += quantity
        return True

    def display_information(self) -> None:
        """Print the common product details. Subclasses add their own details."""
        print(f"{self.__product_id:<6} {self.__name:<15} ${self.__price:<8.2f} Qty: {self.__stock}")

    def to_dict(self) -> dict:
        """Common fields for saving to JSON. Subclasses add their own."""
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }

    # ---------- behaviour every subclass MUST provide ----------
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message about how this product is delivered."""
        pass
