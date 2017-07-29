# # imports
# import copy
# import multiprocessing as mp
# import data_conversion_routes_to_stops as dcrts
# import shortest_path as sp



# def sd():
# 	return dcrts.get_bus_stop_data()

# def fsp(start_stop, end_stop, stop_dict):
# 	return sp.find_shortest_path(start_stop, end_stop, stop_dict)


from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support

def func(a, b):
    return a + b

def main():
    a_args = [1,2,3]
    second_arg = 1
    with Pool() as pool:
        L = pool.starmap(func, [(1, 1), (2, 1), (3, 1)])
        M = pool.starmap(func, zip(a_args, repeat(second_arg)))
        N = pool.map(partial(func, b=second_arg), a_args)
        assert L == M == N

if __name__=="__main__":
    freeze_support()
    main()