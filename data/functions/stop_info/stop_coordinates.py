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
