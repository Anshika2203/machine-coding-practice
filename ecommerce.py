import uuid
import threading
import time

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.lock = threading.Lock()

class ECommerce:
    def __init__(self):
        self.products = {}
        self.carts = {}  # Stores cart items per user
        self.orders = {}  # Stores placed orders per user

    def add_product(self, product_id, name, price, stock):
        if product_id in self.products:
            raise ValueError("Product ID already exists.")
        self.products[product_id] = Product(product_id, name, price, stock)

    def get_inventory_count(self, product_id):
        if product_id not in self.products:
            raise ValueError("Product not found.")
        return self.products[product_id].stock

    def add_to_cart(self, user_id, product_id, count):
        if product_id not in self.products:
            raise ValueError("Product not found.")
        product = self.products[product_id]
        
        with product.lock:
            if product.stock < count:
                raise ValueError("Not enough stock available.")
            product.stock -= count

        self.carts.setdefault(user_id, {}).setdefault(product_id, 0)
        self.carts[user_id][product_id] += count
        
        # Revert stock if order not placed in 5 minutes
        threading.Timer(300, self.revert_cart, [user_id, product_id, count]).start()

    def revert_cart(self, user_id, product_id, count):
        if user_id in self.carts and product_id in self.carts[user_id]:
            with self.products[product_id].lock:
                self.products[product_id].stock += count
            del self.carts[user_id][product_id]

    def place_order(self, user_id):
        if user_id not in self.carts or not self.carts[user_id]:
            raise ValueError("Cart is empty.")
        
        total_amount = 0
        order_details = {}
        
        for product_id, count in self.carts[user_id].items():
            product = self.products[product_id]
            total_amount += product.price * count
            order_details[product_id] = count
        
        self.orders[user_id] = {"items": order_details, "total": total_amount, "confirmed": False}
        self.carts[user_id] = {}  # Empty cart after placing order
        return total_amount
    
    def confirm_order(self, user_id):
        if user_id not in self.orders:
            raise ValueError("No order found.")
        self.orders[user_id]["confirmed"] = True
        return "Order Confirmed!"

# Example Usage
if __name__ == "__main__":
    ecommerce = ECommerce()
    ecommerce.add_product("P1", "Laptop", 1000, 10)
    ecommerce.add_product("P2", "Phone", 500, 5)
    
    ecommerce.add_to_cart("user1", "P1", 2)
    print(ecommerce.get_inventory_count("P1"))  # Expected: 8
    
    total = ecommerce.place_order("user1")
    print("Total Amount:", total)
    print(ecommerce.confirm_order("user1"))