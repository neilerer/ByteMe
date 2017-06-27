import csv
import glob,os
import datetime
import time
import json

""" README
When running the below functions care should be taken when changing between directories.
The functions below use the file structure on my local machince and hence should be changed accordingly for wherever they are being run
"""

def unique_bus_stops():
    """Function which returns a dictionary containing the bus stop numbers and locations
    key=bus stop number, value=array of (lat,long) values for bus stop entries
    resulting location is the most frequent location found for each stop
    """
    stops_and_coordinates = {}
    os.chdir("../Data")
    for file in glob.glob("*.csv"):
        reader=csv.reader(open(file))
        for line in reader:
            try: #try/except block for empty at_stop values error handling (problem converting empty cell to int)
                if int(line[14])==1:
                    if line[13] in stops_and_coordinates: #if stop ID exists
                        coords=[line[9],line[8]] #line[9],line[8] is lat,long
                        if coords not in stops_and_coordinates[line[13]]: #if new GPS coordinate
                            stops_and_coordinates[line[13]].append([line[9],line[8]]) #add to list of GPS coords
                            stops_and_coordinates[line[13]].append(1) #intialises GPS count to 1
                        else: # if current GPS for stop ID had been found already
                            stops_and_coordinates[line[13]][stops_and_coordinates[line[13]].index([line[9],line[8]])+1]+=1 #increment count
                    else:
                        stops_and_coordinates[line[13]]=[[line[9],line[8]],1] #creating a key/value pair for a new stop ID
            except:
                continue
        result={}
        for stop in stops_and_coordinates: #looping through the recorded GPS coords for each stop
            max_count_index=1
            for i in range(3,len(stops_and_coordinates[stop]),2):
                if stops_and_coordinates[stop][i]>stops_and_coordinates[stop][max_count_index]:
                    max_count_index=i #finding the most frequently recorded GPS location for the stop
            result[stop]=stops_and_coordinates[stop][max_count_index-1] #adding result to result dictionary
    return result


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

### BELOW CODE USED TO TEST/RUN ABOVE FUNCTIONS AND OBTAIN DATA ###

# a=route_validity_checker()
# for key in a:
#     print(key, a[key])

# print(len(['15', '46A', '14', '41B', '39A', '65', '40D', '11', '31', '27', '67', '79', '42', '66A', '33B', '140', '44', '83A', '27B', '38', '16C', '747', '41C', '39', '25', '239', '43', '70', '13', '150', '145', '77A', '184', '84', '61', '83', '40', '66', '15A', '123', '17A', '16', '14C', '9', '4', '37', '32', '33', '49', '56A', '151', '25A', '45A', '54A', '47', '18', '7', '17', '102', '120', '65B', '41', '122', '29A', '76', '68', '59', '25B', '69', '27A', '66B', '38B', '7D', '75', '15B', '84A', '63', '84X', '33X', '68A', '1', '76A', '7B', '270', '236', '130', '238', '220', '44B', '40B', '26', '32B', '8', '41A', '53', '67X', '104', '32A', '79A', '114', '185', '66X', '31B', '32X', '51X', '51D', '41X', '142', '111', '69X', '27X', '116', '46E', '161', '118', '25X', '38A', '33A', 'PP07', '53B', '31A', 'OL84']
# )) #num routes is 122, including the 3 which should be excluded


# print(datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d %H:%M:%S'))

# a=unique_bus_stops()
# os.chdir("../Dublin Bus")
# with open("stop_coordinates.json","w",newline="") as file:
#     json.dump(a,file)

# print(len(a))
# for stop in a:
#     print(stop,a[stop])

# print(unique_bus_stops())
# a=unique_colD()
# print(a)
# print(len(a))
# print(unique_routes())

# stopped_bus_data()
# a=bus_routes()
# print(len(a))
# print(a)

# a=stops_on_routes()
# for route in a:
#     print("ROUTE", route)
# print("ROUTE 16")
# for i in range(0,len(a['16']),2):
#     print("stop:", a['16'][i], "count:", a['16'][i+1])
# print(a)
# with open("route16_stop_count.json","w",newline="") as file:
#     json.dump(a,file)
# route_data("16C")

# a=[7347, 289903, 2977, 1462, 1497, 173, 1666, 10, 6064, 38, 409, 76, 1335, 912, 230, 363, 672, 643, 103, 25, 49, 5852, 141, 34, 50, 1546, 1481, 307, 1408, 154, 62, 21, 3277, 183, 73, 8, 1341, 3724, 1441, 37, 264, 98, 1344, 2696, 1432, 266, 296, 347, 5181, 76, 1349, 1183, 356, 60, 2986, 9, 1349, 1, 1350, 2718, 416, 182, 227, 206, 696, 44, 4614, 42, 262, 11046, 3027, 16, 1308, 184, 2994, 14, 2949, 91, 2997, 4, 4456, 4580, 1716, 14, 1284, 3415, 1412, 1519, 1346, 322, 1414, 95, 4433, 35, 1367, 55, 1329, 3550, 456, 15, 4838, 192, 63, 34, 280, 43, 1291, 2707, 1422, 289, 1367, 373, 68, 33, 1346, 17, 5663, 47, 3038, 594, 119, 1428, 116, 2325, 1429, 595, 1310, 63, 86, 16, 1330, 1591, 468, 136, 216, 1236, 1407, 148, 3011, 20, 218, 2985, 7399, 6, 1288, 1445, 1531, 241, 3027, 17, 219, 1628, 1455, 336, 11175, 79, 1310, 206, 35, 7, 1348, 3899, 64, 15, 1354, 4000, 248, 195, 50, 6, 1322, 1362, 1569, 6538, 1463, 936, 56, 146, 1631, 942, 1381, 33, 1626, 1682, 1734, 92, 1370, 118, 1307, 49, 1309, 69, 1305, 1379, 325, 156, 1348, 31, 1303, 1203, 1506, 82, 5173, 443, 212, 52, 1844, 389, 1368, 160, 214, 582, 423, 26, 3007, 430, 1316, 200, 2972, 17, 212, 2, 320, 9753, 1328, 833, 1591, 27, 212, 1, 2975, 141365, 1638, 849, 1420, 537, 3000, 250, 273, 39, 1640, 2210, 286, 2046, 1769, 77, 1308, 25, 1323, 1164, 380, 185, 1305, 36, 1303, 15, 242, 41, 236, 1696, 5459, 196, 1338, 1339, 405, 64, 1331, 3136, 331, 55, 1344, 381, 220, 1275, 1660, 107, 1376, 132, 1640, 126, 48, 2528, 3070, 46, 3916, 62, 1631, 211, 1387, 714, 3055, 22, 2970, 1053, 3034, 67, 243, 296, 269, 13, 1343, 1663, 1713, 199, 1627, 566, 3106, 42, 1638, 12, 3044, 106, 58, 21, 278, 20691, 1344, 64, 1634, 221, 1432, 14, 1292, 1382, 3726, 18, 3396, 37, 1336, 1384, 108, 42, 51, 2123, 1359, 1889, 5113, 111, 1372, 893, 137, 43, 1295, 2149, 1339, 1135, 7374, 23, 213, 3739, 148, 64, 263, 61, 50, 11, 1279, 7574, 7091, 12, 1634, 7, 1629, 207, 1535, 283, 246, 115, 1328, 246, 1328, 134, 1360, 665, 3004, 19, 1582, 47, 1637, 2341, 1348, 55, 317, 32, 1298, 2446, 290, 56, 4432, 1566, 316, 140, 5171, 29506, 2982, 30, 1627, 166, 1331, 50, 1635, 115, 1644, 388, 440, 1118, 1643, 13, 226, 2257, 1347, 2208, 1678, 36, 1285, 5062, 353, 308, 209, 33, 211, 12, 220, 57, 1328, 87, 1349, 58, 7293, 282, 216, 136, 2977, 163, 2977, 15, 215, 3527, 1318, 566, 256, 75, 1297, 895, 1353, 1117, 1287, 4297, 247, 3, 1337, 1160, 217, 1107, 1371, 44, 2969, 979, 1668, 63, 1304, 1203, 245, 51, 1326, 1262, 274, 36, 1289, 2303, 1326, 361, 1340, 2011, 239, 531, 1341, 50, 51, 67, 2969, 18, 2981, 604, 1368, 262, 1644, 133, 2971, 1572, 3008, 111, 132, 93, 7074, 294, 2991, 1469, 318, 477, 229, 133, 3069, 350, 235, 326, 297, 23, 1641, 343, 1778, 256, 1637, 12, 233, 2188, 3705, 30, 1347, 807, 248, 266, 1297, 93, 1304, 373, 1296, 1454, 262, 198, 1356, 460, 1333, 550, 228, 244, 8180, 3, 47, 892, 2993, 30, 214, 92, 1320, 2076, 5095, 20, 1334, 872, 3001, 52, 2220, 11, 2976, 1110, 1337, 178, 2968, 623, 259, 534, 1295, 264, 2972, 31, 7349, 598, 310, 3029, 45, 1226, 5055, 170, 1302, 1067, 1306, 295, 1343, 121, 1339, 1107, 1632, 69, 235, 120, 1391, 630, 1325, 1602, 3686, 76, 1633, 190, 114, 710, 1672, 212, 7071, 54, 2967, 754, 286, 272, 3003, 172, 119, 223, 203, 1375, 298, 169, 1327, 1293, 1390, 75, 205, 2789, 1332, 789, 5051, 2915, 1360, 178, 1628, 109, 220, 8, 1296, 90, 1301, 715, 1323, 183, 336, 265, 1356, 97, 1630, 288, 1363, 390, 247, 698, 231, 1400, 1369, 619, 1645, 34, 1639, 1730, 3011, 173, 1287, 1217, 1293, 1720, 5074, 186, 234, 1454, 1407, 1108, 2966, 721, 1353, 995, 241, 140, 1324, 847, 1311, 382, 1308, 269, 1626, 54, 3669, 248, 242, 554, 1624, 1665, 7090, 96, 210, 21, 1623, 995, 1643, 64, 230, 11, 270, 10783, 2978, 1379, 1309, 790, 5052, 400, 233, 474, 1354, 281, 2980, 633, 1625, 337, 1338, 631, 1624, 362, 1357, 2549, 1295, 918, 1353, 379, 204, 618, 1301, 2, 1299, 969, 1642, 373, 5053, 2, 1294, 887, 1352, 2398, 7073, 143, 2979, 435, 1362, 459, 1342, 798, 1285, 946, 85, 777, 1625, 133, 1355, 1555, 233, 509, 208, 202, 1345, 1086, 1282, 2316, 1622, 408, 1321, 224, 221, 75, 1290, 547, 1636, 133, 7068, 102, 2992, 49, 237, 186, 232, 117, 1300, 5]
# stops_on_16=[]
# for i in range(0,len(a),2):
#     stops_on_16.append(a[i])
# print(stops_on_16)
# print(len(stops_on_16))

# print(stops_on_16route())

# a=stops_on_routes()
# with open("routes_and_stops.json","w",newline="") as file:
#     json.dump(a,file)

# a=bus_routes_direction()
# a.sort()
# print(a)

print(stops_on_routes_with_direction())