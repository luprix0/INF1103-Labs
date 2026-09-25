def load_orders(filename="inventory2.txt"):
    """
    Loads existing orders from disk.

    Input:  filename (str) - path to the orders file.
    Output: list[tuple] - list of (order_id, product_name, quantity) tuples.
            Returns an empty list if the file doesn't exist or a line is
            corrupt (never raises an error).
    """
    orders = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    continue
                order_id_str, product_name, quantity_str = parts
                try:
                    orders.append((int(order_id_str), product_name, int(quantity_str)))
                except ValueError:
                    continue  # skip corrupt line, keep loading the rest
    except FileNotFoundError:
        pass  # no file yet -> start with an empty order list
    return orders


def display_orders(orders):
    """
    Prints all current orders.

    Input:  orders (list[tuple]) - (order_id, product_name, quantity) tuples.
    Output: None
    """
    print("Current Orders:\n")
    for order_id, product_name, quantity in orders:
        print(f"{order_id}, {product_name}, {quantity}")


def get_valid_input(orders):
    """
    Collects the 3 pieces of data that make up one order record:
    - order_id: auto-generated (next number after the highest existing ID)
    - product_name: typed by the user
    - quantity: typed by the user, validated as a positive whole number

    Input:  orders (list[tuple]) - existing orders, used to work out the
            next order_id.
    Output: (int, str, int) or None - (order_id, product_name, quantity)
            if the input was valid, otherwise None.
    """
    product_name = input("Enter Product Name: ").strip()
    if not product_name:
        print("Error: Product name cannot be empty.")
        return None

    quantity_input = input("Enter Quantity: ").strip()
    if not quantity_input.isdigit():
        print("Error: Quantity must be a positive whole number.")
        return None

    quantity = int(quantity_input)
    if quantity <= 0:
        print("Error: Quantity must be greater than zero.")
        return None

    next_id = max((order_id for order_id, _, _ in orders), default=1000) + 1

    return next_id, product_name, quantity


def save_orders(orders, filename="inventory2.txt"):
    """
    Saves all orders to disk, one per line.

    Input:  orders (list[tuple]) - (order_id, product_name, quantity) tuples.
            filename (str) - path to write to.
    Output: None
    """
    with open(filename, "w") as f:
        for order_id, product_name, quantity in orders:
            f.write(f"{order_id}, {product_name}, {quantity}\n")


def main():
    orders = load_orders()
    display_orders(orders)

    print()
    new_order = get_valid_input(orders)

    if new_order is not None:
        orders.append(new_order)
        order_id, product_name, quantity = new_order
        print(f"\nNew Order Added:\n{order_id},{product_name},{quantity}")

        save_orders(orders)
        print("\nOrder successfully saved to inventory2.txt")
    else:
        print("\nOrder was not added due to invalid input.")


if __name__ == "__main__":
    main()