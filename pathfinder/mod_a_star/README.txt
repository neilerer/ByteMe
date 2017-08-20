data_json/

	.gitignore is self-explanatory

	data.json is the output of all our models

	json_to_pickle.py creates a pickle file of the json data

	merge_sort.py is used 



data_json_review/

	.gitignore is self-explanatory

	data_review.py gives you a feel for what's in data.p, which is stored in data_json/



possible_paths/

	route_connections.py generates a dictionary that allows us to see what routes are connected to other routes

	shortest_path.py generates the route-to-route path with minimal route transfers for each pair of routes



possible_paths_review/

	.gitignore is self-explanatory

	route_connections_review.py generates a text file that contains, for each route, all other routes it is connected to (for every weekday and time unit)