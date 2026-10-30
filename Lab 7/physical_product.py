# physical_product.py
# PhysicalProduct: a product that is shipped. Adds weight (kg).
# Inherits from Product and signs the CanBeShipped contract.
# (One parent class plus one interface-style ABC, so no real multiple inheritance of data.)

from can_be_shipped import CanBeShipped
from product import Product

SHIPPING_BASE_FEE = 5.00     # flat fee for any parcel
SHIPPING_PER_KG = 2.00       # extra charge per kilogram


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight          # kilograms

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()   # common details come from Product
        print(f"       Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self):
        return "Physical product: needs to be packed and shipped."

    def calculate_shipping_cost(self):
        """Base fee plus a charge per kilogram."""
        return round(SHIPPING_BASE_FEE + SHIPPING_PER_KG * self.__weight, 2)

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data
