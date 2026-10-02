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


# ---------- Data Persistence ----------
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


def save_inventory(inv):
    """Write the inventory (products + transaction history) to inventory.json."""
    try:
        with open(FILENAME, "w") as file:
            json.dump(inv, file, indent=4)
        print(f"Inventory saved to {FILENAME}.")
    except OSError as error:
        print(f"Error saving inventory: {error}")


# ---------- Menu System ----------
def get_number(prompt, number_type=float):
    """Keep asking until the user enters a valid number."""
    while True:
        try:
            return number_type(input(prompt))
        except ValueError:
            print("Invalid number, try again.")


def show_menu():
    print("\n===== INVENTORY MENU =====")
    print("1. Display")
    print("2. Add")
    print("3. Update")
    print("4. Search")
    print("5. Save")
    print("6. Exit")


def main():
    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            display_all(inventory)

        elif choice == "2":
            name = input("Product name: ").strip()
            price = get_number("Price: ", float)
            quantity = get_number("Quantity: ", int)
            add_product(inventory, name, price, quantity)

        elif choice == "3":
            name = input("Product name: ").strip()
            change = get_number("Change in stock (negative for sale, positive for restock): ", int)
            update_stock(inventory, name, change)

        elif choice == "4":
            name = input("Product name to search: ").strip()
            product = search_product(inventory, name)
            if product:
                print(f"Found: {product['name']} | ${product['price']:.2f} | Qty: {product['quantity']}")
            else:
                print("Product not found.")

        elif choice == "5":
            save_inventory(inventory)

        elif choice == "6":
            save_choice = input("Save before exiting? (y/n): ").strip().lower()
            if save_choice == "y":
                save_inventory(inventory)
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()