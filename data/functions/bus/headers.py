"""
This file contains headres used by the bus data functions
"""


# global variables
headers = [
"Timestamp", # 0: Timestamp micro since 1970 01 01 00:00:00 GMT
"LineID", # 1: Line ID
"Direction", # 2: Direction
"JourneyPatternID", # 3: Journey Pattern ID
"TimeFrame", # 4: Time Frame (The start date of the production time table - in Dublin the production time table starts at 6am and ends at 3am)
"VehicleJourneyID", # 5: Vehicle Journey ID (A given run on the journey pattern)
"Operator", # 6: Operator (Bus operator, not the driver)
"Congestion", # : Congestion [0=no,1=yes]
"Longitude", # 8: Lon WGS84
"Latitude", # 9: Lat WGS84
"BusDelay", # 10: Delay (seconds, negative if bus is ahead of schedule)
"BlockID", # 11: Block ID (a section ID of the journey pattern)
"VehicleID", # 12: Vehicle ID
"StopID", # 13: Stop ID
"AtStop", # 14: At Stop [0=no,1=yes]
]


headers_length = len(headers)


headers_clean = [
"Year",
"Month",
"Day",
"Hours",
"Minute",
"Second",
"WeekDay",
"YearDay",
] + headers