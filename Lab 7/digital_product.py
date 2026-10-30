# digital_product.py
# DigitalProduct: a product that is downloaded. Adds download_size (MB).
# It does NOT implement CanBeShipped, because nothing is shipped.

from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size    # megabytes

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()   # common details come from Product
        print(f"       Digital | Download size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self):
        return "Digital product: delivered as an online download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
