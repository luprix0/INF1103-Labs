from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier

SHIPPING_BASE_FEE: float = 5.00  
SHIPPING_PER_KG: float = 2.00       


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight          

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information() 
        print(f"       Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "Physical product: needs to be packed and shipped."

    def calculate_shipping_cost(self) -> float:
        """Base fee plus a charge per kilogram."""
        return round(SHIPPING_BASE_FEE + SHIPPING_PER_KG * self.__weight, 2)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
