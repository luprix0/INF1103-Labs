import json
import os
import re

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
DATA_DIR: str = os.environ.get("DATA_DIR", SCRIPT_DIR)
FILENAME: str = os.path.join(DATA_DIR, "inventory.json")


# ---------- File Handling ----------
def supplier_from_dict(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    """Reuse the Supplier object with this ID, or create it the first time we see it.
    Products from the same supplier therefore share ONE Supplier object (association)."""
    supplier_id = data.get("supplier_id", "S000")
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data.get("name", "Unknown"),
                                          data.get("contact_email", "n/a"))
    return suppliers[supplier_id]


def product_from_dict(item: dict, number: int, suppliers: dict[str, Supplier]) -> Product:
    """Build the right Product subclass from a saved dictionary, using its "type"."""
    product_id = item.get("product_id", f"P{number:03d}")
    stock = item.get("stock", item.get("quantity", 0))   
    kind = item.get("type", "physical")                   
    supplier = supplier_from_dict(item.get("supplier", {}), suppliers)  

    if kind == "digital":
        return DigitalProduct(product_id, item["name"], item["price"], stock,
                              supplier, item["download_size"])
    if kind == "physical":
        return PhysicalProduct(product_id, item["name"], item["price"], stock,
                               supplier, item.get("weight", 0.0))
    raise ValueError(f"unknown product type '{kind}'")


def load_inventory() -> Inventory:
    """Load inventory.json into an Inventory object; otherwise start empty."""
    inventory = Inventory()
    if not os.path.exists(FILENAME):
        print(f"No saved inventory found at {os.path.abspath(FILENAME)}. Starting with empty inventory.")
        return inventory

    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)

        loaded = Inventory()
        suppliers: dict[str, Supplier] = {}
        for number, item in enumerate(data["products"], start=1):
            loaded.add_product(product_from_dict(item, number, suppliers))
        loaded.load_transactions(data.get("transactions", []))   
        print(f"Loaded inventory from {FILENAME}.")
        return loaded
    except (json.JSONDecodeError, OSError, KeyError, TypeError, AttributeError, ValueError) as error:
        print(f"Could not read {os.path.abspath(FILENAME)} ({type(error).__name__}: {error}). Starting with empty inventory.")
        return inventory


def save_inventory(inventory: Inventory) -> None:
    """Write products (with their suppliers) + transaction history to inventory.json."""
    try:
        with open(FILENAME, "w") as file:
            json.dump(inventory.to_dict(), file, indent=4)
        print(f"Inventory saved to {FILENAME}.")
    except OSError as error:
        print(f"Error saving inventory: {error}")


# ---------- Menu System ----------
def get_number(prompt: str, number_type=float):
    """Keep asking until the user enters a valid number."""
    while True:
        try:
            return number_type(input(prompt))
        except ValueError:
            print("Invalid number, try again.")


def show_menu() -> None:
    print("\n===== INVENTORY MENU =====")
    print("1. Display")
    print("2. Add")
    print("3. Update")
    print("4. Search")
    print("5. Save")
    print("6. Create order")
    print("7. Remove product")
    print("8. Exit")


def known_suppliers(inventory: Inventory) -> dict[str, Supplier]:
    """The suppliers already used by products in the inventory, by ID."""
    return {p.supplier.supplier_id: p.supplier for p in inventory.products}


def ask_supplier(inventory: Inventory) -> Supplier:
    """Reuse a supplier with the same name, or create a new Supplier object."""
    suppliers = known_suppliers(inventory)
    name = input("Supplier name: ").strip()
    for supplier in suppliers.values():
        if supplier.name.lower() == name.lower():
            print(f"Using existing supplier {supplier.supplier_id}.")
            return supplier

    email = input("Supplier contact email: ").strip()
    numbers = [int(m.group(1)) for sid in suppliers if (m := re.fullmatch(r"S(\d+)", sid))]
    return Supplier(f"S{max(numbers, default=0) + 1:03d}", name, email)


def ask_new_product(inventory: Inventory) -> Product:
    """Ask the user for a product's details and build the right subclass."""
    name = input("Product name: ").strip()

    kind = ""
    while kind not in ("1", "2"):
        kind = input("Product type (1 = Physical, 2 = Digital): ").strip()
        if kind not in ("1", "2"):
            print("Please enter 1 or 2.")

    price = get_number("Price: ", float)
    quantity = get_number("Quantity: ", int)
    supplier = ask_supplier(inventory)
    product_id = inventory.next_product_id()

    if kind == "1":
        weight = get_number("Weight (kg): ", float)
        return PhysicalProduct(product_id, name, price, quantity, supplier, weight)
    size = get_number("Download size (MB): ", float)
    return DigitalProduct(product_id, name, price, quantity, supplier, size)


def create_order(inventory: Inventory, orders: list[Order]) -> None:
    """Build an Order from products in the inventory. The Order creates its own lines."""
    order = Order(f"O{len(orders) + 1:03d}")
    print(f"Creating order {order.order_id}. Leave the product blank to finish.")

    while True:
        keyword = input("Product name or ID: ").strip()
        if not keyword:
            break
        product = inventory.search_product(keyword)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_number("Quantity: ", int)
        if quantity <= 0:
            print("Quantity must be at least 1.")
        elif quantity > product.stock:
            print(f"Not enough stock. Only {product.stock} left.")
        else:
            order.add_order_line(product, quantity)

    if not order.order_lines:
        print("Order cancelled: no items.")
        return

    order.display_information()
    if input("Confirm order and reduce stock? (y/n): ").strip().lower() == "y":
        for line in order.order_lines:
            result = inventory.update_stock(line.product.product_id, -line.quantity)
            if result != "ok":
                print(f"Could not reduce stock for {line.product.name}: {result}.")
        orders.append(order)
        print(f"Order {order.order_id} confirmed.")
    else:
        print("Order discarded.")


def main() -> None:
    inventory = load_inventory()
    orders: list[Order] = []

    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()

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
                if isinstance(product, CanBeShipped):     
                    print(f"       Shipping cost: ${product.calculate_shipping_cost():.2f}")
                print("       ", end="")
                product.supplier.display_information()
            else:
                print("Product not found.")

        elif choice == "5":
            save_inventory(inventory)

        elif choice == "6":
            create_order(inventory, orders)

        elif choice == "7":
            name = input("Product ID to remove: ").strip()
            removed = inventory.remove_product(name)
            if removed:
                print(f"Removed '{removed.name}' from the inventory (the product itself still exists).")
            else:
                print("Product not found.")

        elif choice == "8":
            save_choice = input("Save before exiting? (y/n): ").strip().lower()
            if save_choice == "y":
                save_inventory(inventory)
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-8.")


if __name__ == "__main__":
    main()
