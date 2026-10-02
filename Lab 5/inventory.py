import json
import os

FILENAME = "inventory.json"

# ---------- Data Representation ----------
# The inventory is a dictionary holding:
#   "products"     -> list of product dictionaries
#   "transactions" -> history of every transaction amount
inventory = {
    "products": [],
    "transactions": []
}


# ---------- Data Manipulation ----------
def record_transaction(inv, product_name, kind, quantity, amount):
    """Store one transaction in the history list."""
    inv["transactions"].append({
        "product": product_name,
        "type": kind,          # "initial stock", "sale" or "restock"
        "quantity": quantity,
        "amount": round(amount, 2)
    })


def search_product(inv, name):
    """Return the product dictionary matching name, or None."""
    for product in inv["products"]:
        if product["name"].lower() == name.lower():
            return product
    return None


def add_product(inv, name, price, quantity):
    """Add a new product and log the value of the initial stock."""
    if search_product(inv, name):
        print(f"'{name}' already exists. Use update stock instead.")
        return False
    inv["products"].append({"name": name, "price": price, "quantity": quantity})
    record_transaction(inv, name, "initial stock", quantity, price * quantity)
    print(f"Added '{name}'.")
    return True


def update_stock(inv, name, change):
    """Change stock by +/- amount. Negative = sale, positive = restock."""
    product = search_product(inv, name)
    if product is None:
        print(f"'{name}' not found.")
        return False
    if product["quantity"] + change < 0:
        print(f"Not enough stock. Only {product['quantity']} left.")
        return False
    product["quantity"] += change
    kind = "sale" if change < 0 else "restock"
    record_transaction(inv, name, kind, abs(change), abs(change) * product["price"])
    print(f"Updated '{name}'. New quantity: {product['quantity']}")
    return True


def display_all(inv):
    """Print all products and the transaction history."""
    print("\n--- INVENTORY ---")
    if not inv["products"]:
        print("No products in inventory.")
    for p in inv["products"]:
        print(f"{p['name']:<15} ${p['price']:<8.2f} Qty: {p['quantity']}")

    print("\n--- TRANSACTION HISTORY ---")
    if not inv["transactions"]:
        print("No transactions yet.")
    for t in inv["transactions"]:
        print(f"{t['type']:<14} {t['product']:<15} x{t['quantity']:<4} ${t['amount']:.2f}")
    total_sales = sum(t["amount"] for t in inv["transactions"] if t["type"] == "sale")
    print(f"\nTotal sales so far: ${total_sales:.2f}")


# ---------- Data Persistence: Load ----------
def load_inventory():
    """Load inventory.json if it exists; otherwise start empty."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
            print(f"Loaded inventory from {FILENAME}.")
            return data
        except (json.JSONDecodeError, OSError):
            print("Could not read inventory.json. Starting with empty inventory.")
    else:
        print("No saved inventory found. Starting with empty inventory.")
    return {"products": [], "transactions": []}


# ---------- Temporary test (Part 2) ----------
if __name__ == "__main__":
    inventory = load_inventory()

    # First run: file doesn't exist, so create sample data and write it manually
    # (temporary, because save_inventory() doesn't exist yet)
    if not inventory["products"]:
        add_product(inventory, "Notebook", 2.50, 100)
        add_product(inventory, "Pen", 1.20, 250)
        add_product(inventory, "Backpack", 35.00, 20)
        with open(FILENAME, "w") as f:
            json.dump(inventory, f, indent=4)
        print("Sample data written to inventory.json.")

    display_all(inventory)