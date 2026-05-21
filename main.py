import json, sys
PRODUCTS_LIST_FILE = "productsList.json"
SELECTED_ITEMS_LIST = "clientCart.json"


#-------------------------------------------------------------------------------------------------------------
def initialize_files():
    DEFAULT_LIST = {
  "1": {
    "price": 1000,
    "name": "Laptop",
    "stock": 100
  },
  "2": {
    "price": 1000,
    "name": "Desktop",
    "stock": 100
  },
  "3": {
    "price": 1000,
    "name": "Phone",
    "stock": 100
  },
  "4": {
    "price": 1000,
    "name": "TV",
    "stock": 100
  },
  "5": {
    "price": 1000,
    "name": "Fridge",
    "stock": 100
  },
  "6": {
    "price": 1000,
    "name": "Headset",
    "stock": 100
  },
  "7": {
    "price": 1000,
    "name": "webcam",
    "stock": 100
  }
}

    try:
        with open(PRODUCTS_LIST_FILE, "r") as products_list:
            test_list = products_list.read()

    except FileNotFoundError:
        with open(PRODUCTS_LIST_FILE, "w") as products_list:
            json.dump(DEFAULT_LIST, products_list, indent=4)
    try:
        with open(SELECTED_ITEMS_LIST, "r") as cart:
            test_cart = cart.read()
    except FileNotFoundError:
        with open(SELECTED_ITEMS_LIST, "w") as cart:
            json.dump({}, cart, indent=4)
        


def isAdmin():
    choice = input("Do you want to enter as ADMIN? (choose no to log in as CLIENT)\n y(es) / n(o)")
    if choice == "y":
        return True
    return False


def create():
    cart = {}
    return cart


def read(FILE):
    with open(FILE, 'r') as file:
        jsonData = json.load(file)
    return jsonData


def write(FILE, data, isConfirmed):
    if isConfirmed:
        with open(FILE, 'w') as file:
            json.dump(data, file, indent=4)


def cart_show(cart, products):
    total = 0
    print("Your current selection is: ")
    if len(cart) == 0:
        print("Your cart is empty.")
    else:
        for id, qty in cart.items():
            if id in products:
                product = products[id]
                sub_total = product["price"] * qty
                print(f"Product: {product['name']} \n Quantity: {qty}\n Subtotal: {sub_total}")
                total += sub_total
            else:
                print(f"Uknown product ID: {id} quantity: {qty}")
        print(f"Total: {total}")
    show_products(products)


def show_products(products):
    for id in products:
        print(f"Product: {products[id]['name']}, id: {id}, price: {products[id]['price']}")


def admin_show(new_products, old_products):
    print("Current list: ")
    if len(old_products) == 0:
        print("The current list is empty")
        if len(new_products) == 0:
            return
    else:
        for key ,value in old_products.items():
            for tag, content in value.items():
                print(f"name: {key}:\n{tag}: {content}")

    if len(new_products) == 0:
        print("The new list is empty.")

    else:
        for key ,value in new_products.items():
            for tag, content in value.items():
                print(f"name: {key}:\n{tag}: {content}")


def client_update(cart, products):
    while True:
        id = input("Enter a product id: ")
        amount = input("Enter the amount you want: ")
        if amount.isnumeric() and id in products:
            cart[id] = int(amount)
            break
        else:
            print("Enter a valid product/amount.")
    return cart


def admin_update(new_products):
    while True:
        try:
            print("enter id to change/add, or press ctrl + c to exit: ")
            id = input("Enter the product's id: ")
            if id not in new_products:
                new_products[id] = {}
            key = input("Enter the value to change/add: ")
            value = input("Enter the new value: ")
            new_products[id][key] = int(value) if value.isnumeric() else value 
        except KeyboardInterrupt:
            return new_products

    

def confirm():
    while True:
        validation = input("are you sure you want to confirm your modifications? y(es) / n(o) ")
        if validation == 'y':
            return True
        elif validation == 'n':
            return False


def delete(data):
    while True:
        try:
            choice = input("Do you want to remove a product or remove the whole list?\n p(roduct) / s(election): ")
            if choice == "p":
                product = input("Enter the item id to remove: ")
                if product in data:
                    del data[product]
                    return data
            elif choice == "s":
                return {}
            else:
                print("Enter a valid Value, or enter ctrl+c to go back to the menu.")

        except KeyError:
            print("Invalid key. Please enter a valid key to delete.")
        except KeyboardInterrupt:
            break


def checkOut(cart, products):
    if len(cart) == 0:
        print("Your cart is empty. select products before checkout.")
        return cart

    for id, qty in cart.items():
        if id in products and qty > products[id]["stock"]:
            print(f"Insufficient stock for '{products[id]['name']}'. Available: {products[id]['stock']}.")
            return cart
    
    cart_show(cart, products)


    if confirm():
        for id, qty in cart.items():
            if id in products:
                products[id]["stock"] -= qty
        write(PRODUCTS_LIST_FILE, products, True)
        write(SELECTED_ITEMS_LIST, {}, True)
        print("Order confirmed, enjoy.")
        return {}
    print("Order cancelled")
    return cart



def menu(admin):
    while True:
        if admin:
            options = "oerws"
            print("o(verwrite current products list) \ne(dit products list) \nr(emove item/list) \nw(rite/confirm) \ns(how current products list) \nexit: ")
        else:
            options = "cerso" 
            print("o(verwrite cart) \ne(dit cart) \nr(emove item from cart or remove cart) \ns(how current products list and cart)\n c(checkout, confirms order) \nexit: ")
        choice = input()
        if choice in options or choice == "exit":
            return choice

        # print("Choose what to do: ")

    #
#------------------------------------------------------------------------------------------------------------


def main():

    try:
        initialize_files()
        admin = isAdmin() 
        if admin:
            while True:
                choice = input("Do you want to read overwrite the file? enter yes to overwrite, enter no to append: \n")
                if choice == "no" or 'n':
                    new_products = read(PRODUCTS_LIST_FILE)
                    break
                elif choice == "yes" or 'y':
                    new_products = create()
                    break
                else:
                    print("Enter yes or no")
            writing_file = PRODUCTS_LIST_FILE
            old_products = read(PRODUCTS_LIST_FILE)
            while True:
                action = menu(admin)
                if action == "o":
                    new_products = create()
                elif action == 'e':
                    new_products = admin_update(new_products)
                elif action == "r":
                    new_products = delete(new_products)
                elif action == "w":
                    write(writing_file, new_products, confirm())
                elif action == "s":
                    admin_show(new_products, old_products)
                elif action == "exit":
                    sys.exit()



        else:
            cart = read(SELECTED_ITEMS_LIST)
            products = read(PRODUCTS_LIST_FILE)
            writing_file = SELECTED_ITEMS_LIST

            while True:
                action = menu(admin)
                if action == 'c':
                    cart = checkOut(cart, products)
                    write(writing_file, cart, True)
                elif action == 'e':
                    cart = client_update(cart, products)
                    write(writing_file, cart, True)
                elif action == "r":
                    cart = delete(cart)
                    write(writing_file, cart, True)
                elif action == "o":
                    cart = create()
                elif action == "s":
                    cart_show(cart, products)
                elif action == "exit":
                    sys.exit()
    except KeyboardInterrupt:
        sys.exit()

    


main()
