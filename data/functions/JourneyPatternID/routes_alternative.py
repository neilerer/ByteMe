# imports
import os
import routes


def weekday_runs(file_name, weekday):
	data = routes.weekday_stops(file_name)[0]
	return [data[item] for item in data]


def find_unique_values(wd_runs):
	unique_values = []
	for data_list in wd_runs:
		for d in data_list:
			if d not in unique_values:
				unique_values.append(d)
	return unique_values + ["left", "right"]

def total_occurances(wd_runs, unique_values):
	occurances = [0 for x in unique_values]
	for data_list in wd_runs:
		for d in data_list:
			index = unique_values.index(d)
			occurances[index] += 1
			occurances[-2] += 1
			occurances[-1] += 1
	return occurances

def neighbour_count(wd_runs, unique_values, value, side):
	neighbours = [0 for x in unique_values]
	for data_list in wd_runs:
		d_count = 0
		d_limit = len(data_list)
		if d_limit == 1:
			pass
		else:
			for d in data_list:
				if d == value:
					if side == "right":
						try:
							if d_count == d_limit - 1:
								neighbours[-1] += 1
							else:
								neighbour = data_list[d_count + 1]
								neighbours[unique_values.index(neighbour)] += 1
						except:
							pass
					else:
						try:
							if d_count == 0:
								neighbours[-2] += 1
							else:
								neighbour = data_list[d_count - 1]
								neighbours[unique_values.index(neighbour)] += 1
						except:
							pass
				d_count += 1
	return neighbours


def neighbour_fraction(wd_runs, unique_values, value, side):
	# data
	neighbours = neighbour_count(wd_runs, unique_values, value, side)
	n_sum = sum(neighbours)
	neighbour_fraction = []
	# 
	count = 0
	count_bound = len(neighbours)
	# 
	while count < count_bound:
		neighbour_fraction.append(neighbours[count] / n_sum)
		count += 1
	return neighbour_fraction


def neighbourhood_data(file_name, weekday):
	wd_runs = weekday_runs(file_name, weekday)
	unique_values = find_unique_values(wd_runs)
	return [wd_runs, unique_values]

def neighbourhod_numbers(file_name, weekday, value, side):
	# data
	data = neighbourhood_data(file_name, weekday)
	wd_runs = data[0]
	unique_values = data[1]
	# return
	return [value, side, unique_values, neighbour_count(wd_runs, unique_values, value, side), neighbour_fraction(wd_runs, unique_values, value, side)]


file_name = "00010001.csv"
for item in neighbourhod_numbers(file_name, 0, '226', 'left'):
	print(item)