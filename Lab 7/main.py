# main.py
# Main program: shows the menu, gets user input, calls Inventory methods.
# Also holds the file handling (load/save) for now.

import json
import os

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct

# Folder where inventory.json lives: the Docker volume if DATA_DIR is set,
# otherwise the same folder as this main.py.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", SCRIPT_DIR)
FILENAME = os.path.join(DATA_DIR, "inventory.json")


# ---------- File Handling ----------
def product_from_dict(item, number):
    """Build the right Product subclass from a saved dictionary, using its "type"."""
    product_id = item.get("product_id", f"P{number:03d}")
    stock = item.get("stock", item.get("quantity", 0))     # also accepts the Week 5 key
    kind = item.get("type", "physical")                    # older files had no type

    if kind == "digital":
        return DigitalProduct(product_id, item["name"], item["price"], stock,
                              item["download_size"])
    if kind == "physical":
        return PhysicalProduct(product_id, item["name"], item["price"], stock,
                               item.get("weight", 0.0))
    raise ValueError(f"unknown product type '{kind}'")


def load_inventory():
    """Load inventory.json into an Inventory object; otherwise start empty."""
    inventory = Inventory()
    if not os.path.exists(FILENAME):
        print(f"No saved inventory found at {os.path.abspath(FILENAME)}. Starting with empty inventory.")
        return inventory

    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)

        loaded = Inventory()
        for number, item in enumerate(data["products"], start=1):
            loaded.add_product(product_from_dict(item, number))
        loaded.load_transactions(data.get("transactions", []))   # replaces the auto-made history
        print(f"Loaded inventory from {FILENAME}.")
        return loaded
    except (json.JSONDecodeError, OSError, KeyError, TypeError, AttributeError, ValueError) as error:
        print(f"Could not read {os.path.abspath(FILENAME)} ({type(error).__name__}: {error}). Starting with empty inventory.")
        return inventory


def save_inventory(inventory):
    """Write products + transaction history to inventory.json."""
    try:
        with open(FILENAME, "w") as file:
            json.dump(inventory.to_dict(), file, indent=4)
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


def ask_new_product(inventory):
    """Ask the user for a product's details and build the right subclass."""
    name = input("Product name: ").strip()

    kind = ""
    while kind not in ("1", "2"):
        kind = input("Product type (1 = Physical, 2 = Digital): ").strip()
        if kind not in ("1", "2"):
            print("Please enter 1 or 2.")

    price = get_number("Price: ", float)
    quantity = get_number("Quantity: ", int)
    product_id = inventory.next_product_id()

    if kind == "1":
        weight = get_number("Weight (kg): ", float)
        return PhysicalProduct(product_id, name, price, quantity, weight)
    size = get_number("Download size (MB): ", float)
    return DigitalProduct(product_id, name, price, quantity, size)


def main():
    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            product = ask_new_product(inventory)
            if inventory.add_product(product):
                print(f"Added '{product.name}' ({product.product_id}).")
            else:
                print(f"'{product.name}' already exists. Use update stock instead.")

        elif choice == "3":
            name = input("Product name or ID: ").strip()
            change = get_number("Change in stock (negative for sale, positive for restock): ", int)
            result = inventory.update_stock(name, change)
            if result == "ok":
                print(f"Updated '{name}'. New quantity: {inventory.search_product(name).stock}")
            elif result == "not found":
                print(f"'{name}' not found.")
            else:
                print(f"Not enough stock. Only {inventory.search_product(name).stock} left.")

        elif choice == "4":
            name = input("Product name or ID to search: ").strip()
            product = inventory.search_product(name)
            if product:
                print("Found:")
                product.display_information()
                print(f"       {product.get_fulfilment_info()}")
                if isinstance(product, CanBeShipped):      # only shippable products have a cost
                    print(f"       Shipping cost: ${product.calculate_shipping_cost():.2f}")
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
