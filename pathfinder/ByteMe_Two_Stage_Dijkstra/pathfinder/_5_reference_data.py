import _0_data as data
import _1_route_mapping as rm
import _2_route_dijkstra as rs
import _3_stop_dijkstra as sd
import time
import datetime



def remove_first_entry_of_dict(d):
	# return d.pop(next(iter(d)))
	key = next(iter(d))
	value = d[key]
	d.pop(next(iter(d)))
	return [key, value]



def stops_by_weekday_and_time_unit():
	output_dict = dict()
	stop_dict = data.get_pickle_file("stop_dict.p")
	for weekday in stop_dict:
		output_dict[weekday] = dict()
		for time_unit in stop_dict[weekday]:
			output_dict[weekday][time_unit] = list()
			for stop in stop_dict[weekday][time_unit]:
				output_dict[weekday][time_unit].append(stop)
	return output_dict



def check_stop(stops, stop_id):
	for weekday in stops:
		print("Checking {}".format(weekday))
		for time_unit in stops[weekday]:
			print("Checking hour {}".format(time_unit))
			if stop_id in stops[weekday][time_unit]:
				print("Found: {} is in {} at {}".format(stop_id, weekday, time_unit))
			else:
				print("Not Found: {} is not in {} at {}".format(stop_id, weekday, time_unit))
		print("")




def test_the_shortest_path(stop_dict, r_dict):
	# input message for the log
	print("")
	user = input("Identify yourself: ")
	print("")
	message = input("Explain the purpose of this test: ")
	print("")
	weekday = int(input("Enter the weekday: "))
	print("")
	time_unit = int(input("Enter the time_unit: "))
	print("")
	start = int(input("Enter the staring stop id: "))
	print("")
	end = int(input("Enter the ending stop id: "))
	print("")
	# find the shortest path candidates
	start_time = time.time()
	sp = sd.the_shortest_path(stop_dict, r_dict, weekday, time_unit, start, end)
	end_time = time.time()
	# log ID
	destination = open("_4_log_file.txt", "a")
	destination.write("Date: {}\n".format(datetime.datetime.now()))
	destination.write("User: {}\n".format(user))
	destination.write("Comment: {}\n\n".format(message))
	# performance
	destination.write("Performance\n")
	destination.write("Time in Seconds: {}\n\n".format(end_time - start_time))
	# output
	key = sp[0]
	value = sp[1]
	destination.write("The Shortest Path\n")
	destination.write("Routes Used: {}\n".format(key))
	destination.write("Journey Time: {}\n".format(value[0]))
	destination.write("Path Taken:\n")
	for quadruple in value[1]:
		destination.write(str(quadruple) + "\n")
	destination.write("\n\n\n\n")



if __name__ == "__main__":
	# data
	print("Loading stop_dict . . .")
	stop_dict = data.get_pickle_file("stop_dict.p")
	print("Loading route_dict . . .")
	r_dict = rm.routes_dict(stop_dict)
	print("Loading stops . . .")
	stops = stops_by_weekday_and_time_unit()

	while True:
		test_the_shortest_path(stop_dict, r_dict)