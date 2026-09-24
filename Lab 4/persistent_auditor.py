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
    Loads the previously saved inventory total and transaction history.

    Input:  filename (str) - path to the inventory file.
    Output: (int, list[int]) - (inventory total, transaction history).
            Returns (0, []) if the file does not exist or is corrupt,
            without raising an error.
    """
    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        if not lines:
            return 0, []

        total = int(lines[0].strip())

        history = []
        if len(lines) > 1 and lines[1].strip():
            history = [int(x) for x in lines[1].strip().split(",")]

        return total, history

    except FileNotFoundError:
        print("No existing inventory file found. Starting fresh.")
        return 0, []
    except (ValueError, IndexError):
        print("Warning: inventory file is corrupted. Starting fresh.")
        return 0, []


def save_inventory(total, history, filename="inventory.txt"):
    """
    Saves the current inventory total and transaction history to disk.

    Input:  total (int) - the current inventory total.
            history (list[int]) - all valid transaction amounts.
            filename (str) - path to write to.
    Output: None
    """
    with open(filename, "w") as f:
        f.write(str(total) + "\n")
        f.write(",".join(str(x) for x in history) + "\n")


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory, transaction_history = load_inventory()
failed_entries = 0
deliveries_processed = 0

print(f"Starting inventory: {inventory}")
if transaction_history:
    print(f"Loaded transaction history: {transaction_history}")

while True:
    stock = get_valid_input()

    if stock == "quit":
        break

    if stock is None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)
    transaction_history.append(stock)

    tax = calculate_tax(stock)

    deliveries_processed += 1

    print("Stock accepted. Current inventory:", inventory)
    print("Tax for this delivery:", tax)

save_inventory(inventory, transaction_history)
print("Inventory successfully saved to inventory.txt")

generate_report(deliveries_processed, failed_entries)