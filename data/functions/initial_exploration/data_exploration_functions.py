def stopped_bus_data():
    """Function which puts data entries with at_stop=1 into a new csv file"""
    os.chdir("../Data")
    with open("Sorted Data/stopped_bus_data.csv", "w", newline="") as result_file:
        wr = csv.writer(result_file, dialect='excel')
        for file in glob.glob("*.csv"):
            print(file)
            reader = csv.reader(open(file))
            for line in reader:
                try:
                    if int(line[14]) == 1:
                        wr.writerow(line)
                except:
                    continue

def extract_bus_route(code):
    """Returns a bus route of a given journey id code (column D in the provided data)"""
    try:
        if int(code[-4:]): #testing if pattern ends in 4 digits, error here results in "" being returned
            return code[:-4].lstrip('0') #eliminates leading 0s (for routes containing letters eg 046A) and the trailing 4 digit mystery code
    except:
        return "" #error handling picked in bus_routes() function, this will catch null values and journey ids in the incorrect format

def bus_routes():
    """Returns a list of unique bus routes using extract_bus_routes function"""
    route_list = []
    os.chdir("../Data")
    for file in glob.glob("*.csv"):
        print(file)
        reader = csv.reader(open(file))
        for line in reader:
            route=extract_bus_route(line[3]) #Journey ID field
            if route not in route_list and route!="": #error handling for extract_bus_routes function
                route_list.append(route)
    return route_list

def route_validity_checker(): #below route list was rerturned from bus_routes function above, copy and pasted to eliminate need to re-run
    """
    Function created to test the validity of the routes returned by bus_routes function
    Idea is to count the number of occurrences of these routes in the 56 files to see if all the routes seem credible
    """
    route_list=['15', '46A', '14', '41B', '39A', '65', '40D', '11', '31', '27', '67', '79', '42', '66A', '33B', '140', '44', '83A', '27B', '38', '16C', '747', '41C', '39', '25', '239', '43', '70', '13', '150', '145', '77A', '184', '84', '61', '83', '40', '66', '15A', '123', '17A', '16', '14C', '9', '4', '37', '32', '33', '49', '56A', '151', '25A', '45A', '54A', '47', '18', '7', '17', '102', '120', '65B', '41', '122', '29A', '76', '68', '59', '25B', '69', '27A', '66B', '38B', '7D', '75', '15B', '84A', '63', '84X', '33X', '68A', '1', '76A', '7B', '270', '236', '130', '238', '220', '44B', '40B', '26', '32B', '8', '41A', '53', '67X', '104', '32A', '79A', '114', '185', '66X', '31B', '32X', '51X', '51D', '41X', '142', '111', '69X', '27X', '116', '46E', '161', '118', '25X', '38A', '33A', 'PP07', '53B', '31A', 'OL84']
    count_dict={}
    for route in route_list: #dictionary with key for every route in the list
        count_dict[route]=0 #used to count number of occurrences in files
    os.chdir("../Data")
    for file in glob.glob("*.csv"): #for every file
        print(file)
        reader=csv.reader(open(file))
        for line in reader:
            route=extract_bus_route(line[3])
            if route!="":
                count_dict[extract_bus_route(line[3])]+=1 #incremenent the counter of the route with the associated journey id code
    return count_dict #result is that 3 routes are likely due to strange circumstances or errors in data

def route_data(route):
    """
    Function which takes a route number and creates a csv file containing all data relating to the route number
    This function takes a bus route as a string as a parameter
    """
    os.chdir("../Data/test") #change to whatever directory your data files are stored in
    with open("../Sorted Data/"+str(route)+"_data.csv","w",newline="") as result_file: #storing resulting data in csv file in different directory
        wr=csv.writer(result_file, dialect='excel') #setting up csv writer
        for file in glob.glob("*.csv"): #looping through raw data files
            reader=csv.reader(open(file))
            for line in reader:
                if extract_bus_route(line[3])==route: #extract_bus_route returns the bus route from journey pattern id (col D)
                    wr.writerow(line)

def stops_on_routes():
    """
    For every route, each stop it serves is added to an array
    """
    routes = ['15', '46A', '14', '41B', '39A', '65', '40D', '11', '31', '27', '67', '79', '42', '66A', '33B', '140', '44', '83A', '27B', '38', '16C', '747', '41C', '39', '25', '239', '43', '70', '13', '150', '145', '77A', '184', '84', '61', '83', '40', '66', '15A', '123', '17A', '16', '14C', '9', '4', '37', '32', '33', '49', '56A', '151', '25A', '45A', '54A', '47', '18', '7', '17', '102', '120', '65B', '41', '122', '29A', '76', '68', '59', '25B', '69', '27A', '66B', '38B', '7D', '75', '15B', '84A', '63', '84X', '33X', '68A', '1', '76A', '7B', '270', '236', '130', '238', '220', '44B', '40B', '26', '32B', '8', '41A', '53', '67X', '104', '32A', '79A', '114', '185', '66X', '31B', '32X', '51X', '51D', '41X', '142', '111', '69X', '27X', '116', '46E', '161', '118', '25X', '38A', '33A', '31A']
    routes_and_stops={}
    for route in routes:
        routes_and_stops[route]=[] #new array value for each route key
    reader = csv.reader(open("../Data/Sorted Data/stopped_bus_data.csv"))
    for line in reader:
        try:
            current_route=extract_bus_route(line[3])
            if int(line[13]) not in routes_and_stops[current_route]:
                routes_and_stops[current_route].append(int(line[13]))
        except:
            continue
    return routes_and_stops

def extract_route_and_direction(code):
    """Returns a bus route and direction ('<' or '>') from a given journey id code (column D in the provided data)"""
    try:
        if int(code[-4:]):  # testing if pattern ends in 4 digits, error here results in "" being returned
            if code[-4] == '1':
                return (code[:-4] + "y").lstrip(
                    '0')  # eliminates leading 0s (for routes containing letters eg 046A) and the trailing 3-digit code
            elif code[-4] == '0':
                return (code[:-4] + "z").lstrip('0')
    except:
        return ""  # error handling picked in bus_routes() function, this will catch null values and journey ids in the incorrect format

def bus_routes_direction():
    """Returns a list of unique bus routes with direction indicator ('<' or '>') using extract_bus_route_and_direction function"""
    route_list = []
    os.chdir("../Data")
    for file in glob.glob("*.csv"):
        print(file) #useful for monitoring progress of function
        reader = csv.reader(open(file))
        for line in reader:
            route = extract_route_and_direction(line[3])  # Journey ID field
            if route not in route_list and route != "":  # error handling for extract_bus_routes function
                route_list.append(route)
    return route_list

def stops_on_routes_with_direction():
    """
    For every route, each stop it serves is added to an array
    """
    routes_and_stops = {}
    routes = ['102y', '102z', '104y', '104z', '111y', '111z', '114y', '114z', '116y', '116z', '118y', '11y', '11z', '120y', '120z', '122y', '122z', '123y', '123z', '130y', '130z', '13y', '13z', '140y', '140z', '142y', '142z', '145y', '145z', '14Cy', '14Cz', '14y', '14z', '150y', '150z', '151y', '151z', '15Ay', '15Az', '15By', '15Bz', '15y', '15z', '161y', '161z', '16Cy', '16Cz', '16y', '16z', '17Ay', '17Az', '17y', '17z', '184y', '184z', '185y', '185z', '18y', '18z', '1y', '1z', '220y', '220z', '236y', '236z', '238y', '238z', '239y', '239z', '25Ay', '25Az', '25By', '25Bz', '25Xy', '25Xz', '25y', '25z', '26y', '26z', '270y', '270z', '27Ay', '27Az', '27By', '27Bz', '27Xy', '27Xz', '27y', '27z', '29Ay', '29Az', '31Ay', '31Az', '31By', '31Bz', '31y', '31z', '32Ay', '32Az', '32By', '32Bz', '32Xy', '32Xz', '32y', '32z', '33Ay', '33Az', '33By', '33Bz', '33Xy', '33Xz', '33y', '33z', '37y', '37z', '38Ay', '38Az', '38By', '38Bz', '38y', '38z', '39Ay', '39Az', '39y', '39z', '40By', '40Bz', '40Dy', '40Dz', '40y', '40z', '41Ay', '41By', '41Bz', '41Cy', '41Cz', '41Xy', '41Xz', '41y', '41z', '42y', '42z', '43y', '43z', '44By', '44Bz', '44y', '44z', '45Ay', '45Az', '46Ay', '46Az', '46Ey', '47y', '47z', '49y', '49z', '4y', '4z', '51Dy', '51Dz', '51Xy', '53By', '53Bz', '53y', '53z', '54Ay', '54Az', '56Ay', '56Az', '59y', '59z', '61y', '61z', '63y', '63z', '65By', '65Bz', '65y', '65z', '66Ay', '66Az', '66By', '66Bz', '66Xy', '66Xz', '66y', '66z', '67Xy', '67Xz', '67y', '67z', '68Ay', '68Az', '68y', '68z', '69Xy', '69Xz', '69y', '69z', '70y', '70z', '747y', '747z', '75y', '75z', '76Ay', '76Az', '76y', '76z', '77Ay', '77Az', '79Ay', '79Az', '79y', '79z', '7By', '7Bz', '7Dy', '7Dz', '7y', '7z', '83Ay', '83Az', '83y', '83z', '84Ay', '84Az', '84Xy', '84Xz', '84y', '84z', '8y', '8z', '9y', '9z']
    for route in routes:
        routes_and_stops[route] = []  # new array value for each route key
    reader = csv.reader(open("../Data/Sorted Data/stopped_bus_data.csv"))
    for line in reader:
        try:
            current_route = extract_route_and_direction(line[3])
            if int(line[13]) not in routes_and_stops[current_route]:
                routes_and_stops[current_route].append(int(line[13]))
        except:
            continue
    return routes_and_stops
	
def concatenate_data():
	"""Function which concatenates all data files"""
    #os.chdir("../Data") # redirecting to directory where data files are saved
    with open("big_data_file.csv", "w", newline="") as result_file: # creating new master csv file
        wr = csv.writer(result_file, dialect='excel')
        for file in glob.glob("*.csv"):
            # print(file) # useful for monitoring progress of script
            reader = csv.reader(open(file))
            for line in reader:
				wr.writerow(line)