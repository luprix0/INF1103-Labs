import gc
import weakref

from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


print("=== Predict first 1 (section 2.2): del supplier ===")
supplier = Supplier("S001", "TechSource", "sales@techsource.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
ebook = DigitalProduct("P002", "Python Ebook", 19.90, 100, supplier, 12.5)
alive = weakref.ref(supplier)
del supplier
gc.collect()
print("Supplier object still alive?", alive() is not None)
laptop.supplier.display_information()
ebook.supplier.display_information()

print("\n=== Predict first 2 (section 3.2): remove product from Inventory A ===")
inventory_a, inventory_b = Inventory(), Inventory()
inventory_a.add_product(laptop)
removed = inventory_a.remove_product("P001")
print("Removed from A:", removed.name, "| A now holds:", [p.name for p in inventory_a.products])
print("Product still works? update_stock(-1) ->", laptop.update_stock(-1), "| stock:", laptop.stock)
inventory_b.add_product(laptop)
print("Same object in B?", inventory_b.find_product("P001") is laptop)

print("\n=== Predict first 3 (section 4.3): same product in two orders ===")
order_1, order_2 = Order("O001"), Order("O002")
order_1.add_order_line(laptop, 1)
order_2.add_order_line(laptop, 2)
line_1, line_2 = order_1.order_lines[0], order_2.order_lines[0]
print("Same OrderLine object?  ", line_1 is line_2, "(so 2 OrderLine objects)")
print("Same Product object?    ", line_1.product is line_2.product, "(so 1 Product object)")
print("id(line_1) =", id(line_1), "| id(line_2) =", id(line_2))
print("id(product in line_1) =", id(line_1.product), "| id(product in line_2) =", id(line_2.product))
order_1.add_order_line(ebook, 3)
order_1.display_information()
order_2.display_information()

print("\n=== Predict first 4 (section 7.2): polymorphism ===")
inventory_b.add_product(ebook)
for product in inventory_b.products:           
    product.display_information()
    print("  ->", product.get_fulfilment_info())

print("\n=== LSP (section 6.2): show_product_details works for both ===")
show_product_details(laptop)
show_product_details(ebook)
