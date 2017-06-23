import json

with open("stops_on_routes.json") as file:
    stops_on_routes=json.load(file)

print(stops_on_routes)