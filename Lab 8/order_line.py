from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        """Product price multiplied by the quantity ordered."""
        return round(self.__product.price * self.__quantity, 2)

    def display_information(self) -> None:
        print(f"   {self.__product.name:<15} x{self.__quantity:<4} ${self.calculate_subtotal():.2f}")
