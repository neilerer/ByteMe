# imports
import json
import merge_sort



def json_to_dict(file_name):
	with open(file_name) as json_data:
		return json.load(json_data)

def key_to_list(key):
	key_list = key.split("-")
	return key_list

def dict_display(file_name, jpi):
	data = json_to_dict(file_name)[jpi]
	for key in data:
		key_list = key_to_list(key)
		print("Key: {}".format(key_list))
		print("Stop Sequence: {}".format(key_list[0]))
		print("Stop ID: {}".format(key_list[1]))
		print("Weekday: {}".format(key_list[2]))
		print("Hour: {}".format(key_list[3]))
		print("CTT: {}".format(data[key]))
		print("")


def route(jpi_dict, jpi, weekday_input, hour_input):
	data = jpi_dict[jpi]
	output_dict = dict()
	for key in data:
		key_list = key_to_list(key)
		stop_sequence = key_list[0]
		stop_id = key_list[1]
		weekday = key_list[2]
		hour = key_list[3]
		ctt = data[key]

		if weekday == weekday_input and hour == hour_input:
			output_dict[stop_sequence] = (stop_id, ctt)

	output_dict = merge_sort.merge_sort_route(output_dict)

	return output_dict


jpi_dict = json_to_dict("046A0001.json")
# dict_display("046A0001.json", "046A0001")
my_data = route(jpi_dict, "046A0001", '3', '9')
for sequence in my_data:
	print(sequence)
	print(my_data[sequence])