# inventory.py
# Inventory: stores and manages a COLLECTION of Product objects (SRP).
# It does not read input, show the menu or touch files.

from product import Product


class Inventory:
    def __init__(self):
        self.__products = []        # list of Product objects
        self.__transactions = []    # history of every transaction

    # ---------- products ----------
    def add_product(self, product):
        """Store a Product. Returns False if the name or ID already exists."""
        if self.search_product(product.name) or self.search_product(product.product_id):
            return False
        self.__products.append(product)
        self.__record_transaction(product, "initial stock", product.stock)
        return True

    def search_product(self, keyword):
        """Find a product by name or product ID (not case-sensitive). Returns Product or None."""
        for product in self.__products:
            if keyword.lower() in (product.name.lower(), product.product_id.lower()):
                return product
        return None

    def update_stock(self, keyword, change):
        """Change stock of one product. Returns "ok", "not found" or "not enough stock"."""
        product = self.search_product(keyword)
        if product is None:
            return "not found"
        if not product.update_stock(change):
            return "not enough stock"
        kind = "sale" if change < 0 else "restock"
        self.__record_transaction(product, kind, abs(change))
        return "ok"

    def next_product_id(self):
        """Make the next free ID, e.g. P001, P002 ..."""
        return f"P{len(self.__products) + 1:03d}"

    def display_all(self):
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
    def to_dict(self):
        return {
            "products": [p.to_dict() for p in self.__products],
            "transactions": list(self.__transactions),
        }

    def load_transactions(self, transactions):
        """Used when loading from file: restore the saved history."""
        self.__transactions = list(transactions)

    # ---------- helper ----------
    def __record_transaction(self, product, kind, quantity):
        self.__transactions.append({
            "product": product.name,
            "type": kind,        # "initial stock", "sale" or "restock"
            "quantity": quantity,
            "amount": round(quantity * product.price, 2),
        })
