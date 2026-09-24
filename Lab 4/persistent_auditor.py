def get_valid_input():
    while True:
        stock = input("Enter stock quantity (or 'quit' to exit): ")

        if stock.lower() == "quit":
            return "quit"

        if not stock.isdigit():
            print("Error: Invalid input. Please enter a number.")
            return None

        stock = int(stock)

        if stock < 0:
            print("Error: Negative stock values are not allowed.")
            return None

        return stock


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def load_inventory(filename="inventory.txt"):
    """
    Loads the previously saved inventory total from disk.

    Input:  filename (str) - path to the inventory file.
    Output: int - the saved inventory total, or 0 if the file does not
            exist or its contents can't be read.
    """
    try:
        with open(filename, "r") as f:
            first_line = f.readline().strip()
            return int(first_line)
    except FileNotFoundError:
        print("No existing inventory file found. Starting with inventory = 0.")
        return 0
    except ValueError:
        print("Warning: inventory file contents were invalid. Starting with inventory = 0.")
        return 0


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory = load_inventory()
failed_entries = 0
deliveries_processed = 0

print(f"Starting inventory: {inventory}")

while True:
    stock = get_valid_input()

    if stock == "quit":
        break

    if stock is None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)

    tax = calculate_tax(stock)

    deliveries_processed += 1

    print("Stock accepted. Current inventory:", inventory)
    print("Tax for this delivery:", tax)

generate_report(deliveries_processed, failed_entries)