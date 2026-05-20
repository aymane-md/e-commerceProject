import json
PRODUCTS_LIST_FILE = "procuctsList.json"
SELECTED_ITEMS_LIST = "clientCart.json"


#-------------------------------------------------------------------------------------------------------------
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


def show(current_data, new_data):
    print("Currently available products: ")
    for key ,value in current_data.values():
        for tag, value in value.items():
            print(f"name: {key}:\n{tag}: {value}")
    print("currently selected products: ")
    if len(new_data) > 0:
        for key ,value in new_data.values():
            for tag, value in value.items():
                print(f"name: {key}:\n{tag}: {value}")
    else:
        print("No currently selected products, make a selection first")

def update(read_object, write_object):
    while True:
        key = input("Enter a product id: ")
        value = input("Enter the amount you want: ")
        if value.isnumeric() and key in [read_object[i]["id"] for i in read_object.keys()]:
            write_object[key] = int(value)
            break
        else:
            print("Enter a valid product/amount.")
    return write_object


def confirm():
    while True:
        validation = input("are you sure you want to confirm your modifications? y(es) / n(o) ")
        if validation == 'y':
            return True
        elif validation == 'n':
            return False


def write(FILE, data, isConfirmed):
    if isConfirmed:
        with open(FILE, 'w') as file:
            json.dump(data, file, indent=4)


def delete(data):
    while True:
        try:
            choice = input("Do you want to remove a product from your cart or abort the whoe selection?\n p(roduct) / s(election): ")
            if choice == "p":
                product = input("Enter the key/value to delete: ")
                if product in data:
                    del data[product]
                    return data
            if choice == "s":
                data = {}
                return data
            else:
                print("Enter a valid Value, or enter ctrl+c to go back to exit.")

        except KeyError:
            print("Invalid key. Please enter a valid key to delete.")
        # return delete(data)

#------------------------------------------------------------------------------------------------------------


def main():
    admin = isAdmin()
    if admin:
        current_data = read(PRODUCTS_LIST_FILE)
        new_data = {}
        show(current_data, new_data)
        while True:
            choice = input("Do you want to read overwrite the file? enter yes to overwrite, enter no to append")
            if choice == "no":
                new_data = read(PRODUCTS_LIST_FILE)
                break
            elif choice == "yes":
                new_data = create()
                break
            else:
                print("Enter yes or no")
        new_data = update(current_data, new_data)
        update(current_data, new_data)
        writing_file = PRODUCTS_LIST_FILE

    else:
        choice = input("Do you want to load cart from a file? enter yes to load, enter no to start a new one: ")
        while True:
            if choice == "yes":
                new_data = read(PRODUCTS_LIST_FILE)
                break
            elif choice == "no":
                new_data = create()
                break
            else:
                print("Enter yes or no")
        writing_file = SELECTED_ITEMS_LIST

    write(writing_file, new_data, confirm())



    


