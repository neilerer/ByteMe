"""
This file contains the headers used in the weather files
"""

raw = [
'Time (GMT)', 
'Temp.', 
'Dew Point', 
'Humidity', 
'Pressure', 
'Visibility', 
'Wind Dir', 
'Wind Speed', 
'Gust Speed', 
'Precip', 
'Events', 
'Conditions',
]

clean = [
"Hour",
"Minute",
"Temperature (C)", # celcius
"Dew Point (C)", # celcius
"Humidity (%)", # %
"Pressure (hPa)", # hPa
"Visibility (km)", # km
"Wind Direction",
"Wind Speed (km/h)", # km/h
"Gust Speed (km/h)", # km/h
"Precipitation", 
"Events",
"Conditions",
]

final = [
"Year", 
"Month", 
"Day", 
"Hours", 
"Minute", 
"Second", 
"Day of the Week (Monday == 0)", 
"Day of the Year (0 to 366)",
] + clean[2::1]