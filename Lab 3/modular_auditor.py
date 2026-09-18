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


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory = 0
failed_entries = 0
deliveries_processed = 0

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