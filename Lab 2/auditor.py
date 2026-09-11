inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or 'quit' to exit): ")

    # Exit condition
    if stock.lower() == "quit":
        break

    # Check if the input is a valid integer
    if not stock.isdigit():
        print("Error: Invalid input. Please enter a number.")
        failed_entries += 1
        continue

    # Convert the input to an integer
    stock = int(stock)

    # Check for negative numbers
    if stock < 0:
        print("Error: Negative stock values are not allowed.")
        failed_entries += 1
        continue

    # Add valid stock to inventory
    inventory += stock
    print("Stock accepted. Current inventory:", inventory)

    # Overstock check / Will trigger alert if stock more than 500
    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break

# Final report
print("\n--- Final Report ---")
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)