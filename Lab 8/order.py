from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        """A copy of the list, so outside code cannot add or remove lines directly."""
        return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine inside this order (the Order owns it)."""
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the first line for this product. Returns True if one was removed."""
        for line in self.__order_lines:
            if line.product.product_id.lower() == product_id.lower():
                self.__order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        """Ask every OrderLine for its subtotal and add them up."""
        return round(sum(line.calculate_subtotal() for line in self.__order_lines), 2)

    def display_information(self) -> None:
        print(f"\n--- ORDER {self.__order_id} ---")
        if not self.__order_lines:
            print("   (no items)")
        for line in self.__order_lines:
            line.display_information()
        print(f"   Total: ${self.calculate_total():.2f}")
