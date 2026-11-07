import gc
import os
import tempfile
import weakref

os.environ["DATA_DIR"] = tempfile.mkdtemp()     

import main
from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSource", "sales@techsource.com")


def make_products(supplier: Supplier) -> tuple[PhysicalProduct, DigitalProduct]:
    return (PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5),
            DigitalProduct("P002", "Python Ebook", 19.90, 100, supplier, 12.5))


# ---------- association: Supplier and Product ----------
def test_product_stores_reference_to_supplier():
    supplier = make_supplier()
    laptop, ebook = make_products(supplier)
    assert laptop.supplier is supplier and ebook.supplier is supplier      


def test_products_still_have_supplier_after_del_supplier():
    supplier = make_supplier()
    laptop, ebook = make_products(supplier)
    alive = weakref.ref(supplier)
    del supplier                                  
    gc.collect()
    assert alive() is not None                     
    assert laptop.supplier.name == "TechSource" and ebook.supplier.name == "TechSource"


def test_supplier_exists_without_products():
    supplier = make_supplier()
    assert supplier.name == "TechSource"          


# ---------- aggregation: Inventory and Product ----------
def test_product_survives_removal_and_moves_between_inventories():
    laptop, _ = make_products(make_supplier())   
    inv_a, inv_b = Inventory(), Inventory()
    assert inv_a.add_product(laptop)
    removed = inv_a.remove_product("P001")
    assert removed is laptop and inv_a.find_product("P001") is None
    assert laptop.update_stock(-1) and laptop.stock == 14    
    assert inv_b.add_product(laptop)
    assert inv_b.find_product("p001") is laptop             


def test_empty_inventory_does_not_destroy_products():
    laptop, ebook = make_products(make_supplier())
    inv = Inventory()
    inv.add_product(laptop); inv.add_product(ebook)
    inv.remove_product("P001"); inv.remove_product("P002")
    assert inv.products == [] and laptop.name == "Laptop" and ebook.name == "Python Ebook"


def test_find_and_remove_missing_product_give_none():
    inv = Inventory()
    assert inv.find_product("P999") is None and inv.remove_product("P999") is None


def test_next_product_id_is_safe_after_removal():
    s = make_supplier()
    inv = Inventory()
    inv.add_product(PhysicalProduct("P001", "A", 1, 1, s, 1))
    inv.add_product(PhysicalProduct("P002", "B", 1, 1, s, 1))
    inv.add_product(PhysicalProduct("P003", "C", 1, 1, s, 1))
    inv.remove_product("P002")
    assert inv.next_product_id() == "P004"


# ---------- composition: Order and OrderLine ----------
def test_order_creates_its_own_order_lines_and_totals():
    laptop, ebook = make_products(make_supplier())
    order = Order("O001")
    order.add_order_line(laptop, 2)
    order.add_order_line(ebook, 3)
    assert all(isinstance(line, OrderLine) for line in order.order_lines)
    assert order.order_lines[0].calculate_subtotal() == 2400.00
    assert order.calculate_total() == 2400.00 + 59.70


def test_same_product_in_two_orders_gives_two_lines_one_product():
    laptop, _ = make_products(make_supplier())
    order_1, order_2 = Order("O001"), Order("O002")
    order_1.add_order_line(laptop, 1)
    order_2.add_order_line(laptop, 1)
    line_1, line_2 = order_1.order_lines[0], order_2.order_lines[0]
    assert line_1 is not line_2                   
    assert line_1.product is line_2.product is laptop    


def test_removing_order_line_does_not_destroy_product():
    laptop, _ = make_products(make_supplier())
    order = Order("O001")
    order.add_order_line(laptop, 1)
    assert order.remove_order_line("P001") is True and order.order_lines == []
    assert laptop.name == "Laptop"               
    assert order.remove_order_line("P001") is False


def test_deleting_order_does_not_destroy_product():
    laptop, _ = make_products(make_supplier())
    order = Order("O001")
    order.add_order_line(laptop, 1)
    line_ref = weakref.ref(order.order_lines[0])
    del order
    gc.collect()
    assert line_ref() is None                      
    assert laptop.stock == 15                      


def test_order_rejects_zero_quantity():
    laptop, _ = make_products(make_supplier())
    try:
        Order("O001").add_order_line(laptop, 0)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


# ---------- LSP and polymorphism ----------
def show_product_details(product: Product) -> str:
    """Works for ANY Product, so it never checks the subclass."""
    return product.get_fulfilment_info()


def test_substitutability_and_polymorphism():
    laptop, ebook = make_products(make_supplier())
    assert "shipped" in show_product_details(laptop)
    assert "download" in show_product_details(ebook)
    inv = Inventory()
    inv.add_product(laptop); inv.add_product(ebook)
    infos = [p.get_fulfilment_info() for p in inv.products]     
    assert infos == ["Physical product: needs to be packed and shipped.",
                     "Digital product: delivered as an online download."]


def test_both_subclasses_keep_update_stock_contract():
    for product in make_products(make_supplier()):
        start = product.stock
        assert product.update_stock(-1) is True and product.stock == start - 1
        assert product.update_stock(-10_000) is False and product.stock == start - 1  
        assert product.update_stock(5) is True and product.stock == start + 4


def test_product_is_abstract_and_digital_is_not_shippable():
    try:
        Product("P9", "Nope", 1, 1, make_supplier())
    except TypeError:
        pass
    else:
        raise AssertionError("Product() should not be creatable")
    laptop, ebook = make_products(make_supplier())
    assert isinstance(laptop, CanBeShipped) and not isinstance(ebook, CanBeShipped)
    assert laptop.calculate_shipping_cost() == 10.00


# ---------- JSON ----------
def test_json_round_trip_keeps_types_and_shared_supplier():
    supplier = make_supplier()
    laptop, ebook = make_products(supplier)
    inv = Inventory()
    inv.add_product(laptop); inv.add_product(ebook)
    main.save_inventory(inv)
    back = main.load_inventory()
    laptop_back, ebook_back = back.find_product("P001"), back.find_product("P002")
    assert type(laptop_back) is PhysicalProduct and laptop_back.weight == 2.5
    assert type(ebook_back) is DigitalProduct and ebook_back.download_size == 12.5
    assert laptop_back.supplier.name == "TechSource"
    assert laptop_back.supplier is ebook_back.supplier      


def test_old_lab7_file_without_supplier_still_loads():
    import json
    with open(main.FILENAME, "w") as f:
        json.dump({"products": [{"product_id": "P001", "name": "Pen", "price": 2, "stock": 5,
                                 "type": "physical", "weight": 0.1}], "transactions": []}, f)
    back = main.load_inventory()
    assert back.find_product("P001").supplier.name == "Unknown"


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print("PASS ", name)
        except Exception as error:
            failed += 1
            print("FAIL ", name, "->", repr(error))
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
