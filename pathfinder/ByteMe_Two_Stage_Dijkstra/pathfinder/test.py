import itertools

route_list = ["a", "b", "c"]


print(list(itertools.combinations(route_list, 2)))

# print([itertools.combinations(route_list, r) for r in range(1, len(route_list))][0])