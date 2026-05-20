import json

with open("productsList.json", "r") as file:
    json_data = json.load(file)
    for key, value in json_data.items():
        for tag, value in value.items():
            print(tag, value)
