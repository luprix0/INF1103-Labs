import re

from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []    
        self.__transactions: list[dict] = [] 

    @property
    def products(self) -> list[Product]:
        """A copy of the product list (add/remove only through the methods below)."""
        return list(self.__products)

    # ---------- products ----------
    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the name or ID already exists."""
        if self.find_product(product.product_id) or self.search_product(product.name):
            return False
        self.__products.append(product)
        self.__record_transaction(product, "initial stock", product.stock)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the product's reference from this inventory and return it.
        The Product itself is NOT destroyed. Returns None if it was not found."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Find a product by its ID (not case-sensitive)."""
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def search_product(self, keyword: str) -> Product | None:
        """Find a product by name or product ID (not case-sensitive)."""
        for product in self.__products:
            if keyword.lower() in (product.name.lower(), product.product_id.lower()):
                return product
        return None

    def update_stock(self, keyword: str, change: int) -> str:
        """Change stock of one product. Returns "ok", "not found" or "not enough stock"."""
        product = self.search_product(keyword)
        if product is None:
            return "not found"
        if not product.update_stock(change):
            return "not enough stock"
        kind = "sale" if change < 0 else "restock"
        self.__record_transaction(product, kind, abs(change))
        return "ok"

    def next_product_id(self) -> str:
        """Make the next free ID, e.g. P001, P002 ... (safe even after removals)."""
        numbers = [int(m.group(1)) for p in self.__products
                   if (m := re.fullmatch(r"P(\d+)", p.product_id))]
        return f"P{max(numbers, default=0) + 1:03d}"

    def display_all(self) -> None:
        """Print all products and the transaction history."""
        print("\n--- INVENTORY ---")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()       

        print("\n--- TRANSACTION HISTORY ---")
        if not self.__transactions:
            print("No transactions yet.")
        for t in self.__transactions:
            print(f"{t['type']:<14} {t['product']:<15} x{t['quantity']:<4} ${t['amount']:.2f}")
        total_sales = sum(t["amount"] for t in self.__transactions if t["type"] == "sale")
        print(f"\nTotal sales so far: ${total_sales:.2f}")

    # ---------- data for the file handler ----------
    def to_dict(self) -> dict:
        return {
            "products": [p.to_dict() for p in self.__products],
            "transactions": list(self.__transactions),
        }

    def load_transactions(self, transactions: list[dict]) -> None:
        """Used when loading from file: restore the saved history."""
        self.__transactions = list(transactions)

    # ---------- helper ----------
    def __record_transaction(self, product: Product, kind: str, quantity: int) -> None:
        self.__transactions.append({
            "product": product.name,
            "type": kind,       
            "quantity": quantity,
            "amount": round(quantity * product.price, 2),
        })
