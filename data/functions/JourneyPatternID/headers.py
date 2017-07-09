"""
This file holds the headers used in the JourneyPatternID activities
"""

headers = ["Year","Month","Day","Hours","Minute","Second","WeekDay","YearDay","Timestamp","LineID","Direction","JourneyPatternID","TimeFrame","VehicleJourneyID","Operator","Congestion","Longitude","Latitude","BusDelay","BlockID","VehicleID","StopID","AtStop","Temperature (C)","Dew Point (C)","Humidity (%)","Pressure (hPa)","Visibility (km)","Wind Direction","Wind Speed (km/h)","Gust Speed (km/h)","Precipitation","Events","Conditions"]

headers_reduced = ["Year","Month","Day","Hours","Minute","Second","WeekDay", "Timestamp", "JourneyPatternID", "VehicleJourneyID", "Longitude","Latitude", "VehicleID", "StopID","AtStop","Temperature (C)", "Visibility (km)", "Wind Speed (km/h)"]

headers_unique_identifiers = ["VehicleJourneyID", "VehicleID"]

headers_timestamp_dict_and_list = ["VehicleJourneyID", "VehicleID", "StopID", "Timestamp", "AtStop"]