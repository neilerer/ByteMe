import pickle as pkl

with open("route_list", "rb") as route_file: # loading pickle file with routes
    routes=pkl.load(route_file)
