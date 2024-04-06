from backend.db_manager import DBManager
import uuid

class Product:
    def __init__(self, item_id, item_name, price, description, category, pictures, seller_id, inventory):
        self.item_id = item_id
        self.item_name = item_name
        self.price = price
        self.description = description
        self.category = category
        self.pictures = pictures
        self.seller_id = seller_id
        self.inventory = inventory

def create_product(item_id, item_name, price, description, category, pictures, seller_id, inventory):
    product_data = {
        "item_id": item_id,
        "item_name": item_name,
        "price": price,
        "description": description,
        "category": category,
        "pictures": pictures,
        "seller_id": seller_id,
        "inventory": inventory
    }
    db_manager = DBManager()
    db_manager.insert_product(product_data)
    return (True, "Product created successfully")

def get_product(item_id):
    db_manager = DBManager()
    product_data = db_manager.get(item_id, f"products/{item_id}")
    if product_data:
        return (True, Product(**product_data))
    else:
        return (False, "Product not found")

def browse_products_by_category(category):
    db_manager = DBManager()
    products_data = db_manager.find_by_category(category)
    products = [Product(**data) for data in products_data]
    return (True, products)
    

def search_products(search_term):
    db_manager = DBManager()
    products_data = db_manager.search_products(search_term)
    products = [Product(**data) for data in products_data]
    return (True, products)