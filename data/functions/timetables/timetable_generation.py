#timetable_generation.py
#generate json files containing timetables for each route divided into Monday to Friday, Saturday and Sunday schedules
#code review 16-08-17

#imports
import json
import pandas as pd
import os
import time


def convert_seconds_to_HHMMSS(seconds):
        """convert seconds to HHMMSS format"""
        #seconds
        minutes = seconds / 60
        remaining_seconds = int(seconds % 60) #less than 59
        if int(remaining_seconds) < 10:
                remaining_seconds = "0" + str(remaining_seconds)
        #minutes
        remaining_minutes = int(minutes % 60)
        if int(remaining_minutes) < 10:  # or len(str(minutes)) < 2:
                remaining_minutes = "0" + str(remaining_minutes)  # check this
        #hours
        hours = int((minutes // 60))
        if int(hours) < 10:
                hours = "0" + str(hours)
        HHMMSS_from_secs = str(hours) + str(remaining_minutes) + str(remaining_seconds)
        return HHMMSS_from_secs



def HHMMSS_to_seconds(time):
        """"Convert HHMMSS to number of seconds"""
        hours = str(time)[0:2]
        minutes = str(time)[2:4]
        seconds = str(time)[4:6]
        hours_to_seconds = int(hours) * 60 * 60
        minutes_to_seconds = int(minutes) * 60
        total_of_seconds = int(hours_to_seconds) + int(minutes_to_seconds) + int(seconds)
        return total_of_seconds



def concat_rowdata_to_HHMMSS(line):
        """returns HHMMSS from single row in input data file"""
        if int(line['Hours'])<10:
                hours='0'+str(line['Hours'])
        else:
                hours=str(line['Hours'])
        if int(line['Minute'])<10:
                minutes='0'+str(line['Minute'])
        else:
                minutes=str(line['Minute'])
        if int(line['Second'])<10:
                seconds='0'+str(line['Second'])
        else:
                seconds=str(line['Second'])
        HHMMSS_from_rowdata = hours + minutes + seconds
        return HHMMSS_from_rowdata



def concat_rowdata_to_date(line):
        """convert date columns to single output, returns DDMMYYYY from line in data file"""
        if int(line['Day'])<10:
                day='0'+str(line['Day'])
        else:
                day=str(line['Day'])
        if int(line['Month'])<10:
                month='0'+str(line['Month'])
        else:
                month=str(line['Month'])
        DDMMYYYY_from_rowdata = day+month+str(line['Year'])
        return DDMMYYYY_from_rowdata



def get_first_and_last_stop_refine_df(jpid, df):
        """get first_and last stop ids_for given journey pattern and filter given dataframe to keep only entries with first_stop_id"""
        with open("list_folder/jpid_start_stop.txt", "r") as output:  # each line = jpid, first stop
                for line in output:
                        line = line.split(",")
                        if jpid == line[0]:
                                first_stop_id = line[1]
                                last_stop_id = line[2]
                                last_stop_id = last_stop_id.rstrip("\n")
        #dfFirst contains rows with stop id equal to first stop id only
        dfFirst = df.loc[df["StopID"] == int(first_stop_id)]
        return dfFirst, first_stop_id, last_stop_id



def get_all_dates(dfFirst):
        """add all recorded dates from dataframe to list and write to txt file, return list of all recorded dates"""
        all_dates = []
        for index, row in dfFirst.iterrows():
                DDMMYYYY_from_rowdata = concat_rowdata_to_date(row)  # concatenate columns to one value, DDMMYYYY
                if DDMMYYYY_from_rowdata not in all_dates:
                        all_dates.append(DDMMYYYY_from_rowdata)

        with open('date_list.txt', 'w') as date_list:
                for item in all_dates:
                        date_list.write(str(item + "\n"))
        f = open("date_list.txt")
        list_of_dates = f.read()
        return list_of_dates



def generate_dicts_weekly_schedules(jpid, list_of_dates, dfFirst):
        """for a given journey pattern, generate 3 dicts containing bus departure times based on averages for M_F, Saturday and Sunday/Bank Holidays"""
        Weekday = {'2012': {}, '2013': {}} #returns Weekday = {'2012': {00010001: [1, 12012013, 091500]}, {}, {}...}
        Sat = {'2012': {}, '2013': {}}     #dict values=  Weekday = {year: {jpid: [day_of_week, DDMMYYYY, HHMMSS]}, {}, {}...}
        Sun = {'2012': {}, '2013': {}}

        for item, row in dfFirst.iterrows():
                #M-F
                for key, value in Weekday.items():
                        #only 2013 data after 1st Jan is used, when new consistent vehicle journey id system implemented, row['Day'] <2 ignored
                        if row['Day'] >= 2:
                                if row['WeekDay'] >= 0 and row['WeekDay'] <= 4:
                                        if key == str(row['Year']):
                                                if row['VehicleJourneyID'] not in Weekday[key]:
                                                        # add vjid
                                                        Weekday[key][row['VehicleJourneyID']] = [
                                                                [row['WeekDay'], concat_rowdata_to_date(row), concat_rowdata_to_HHMMSS(row)]]
                                                elif row['VehicleJourneyID'] in Weekday[key]:
                                                        # append instance of vjid
                                                        Weekday[key][row['VehicleJourneyID']].append(
                                                                [row['WeekDay'], concat_rowdata_to_date(row), concat_rowdata_to_HHMMSS(row)])
                #Sat
                for key, value in Sat.items():
                        if row['Day'] >= 2:
                                if row['WeekDay'] == 5:
                                        if str(row['Year']) == key:

                                                if row['VehicleJourneyID'] not in Sat[key]:
                                                        Sat[key][row['VehicleJourneyID']] = [
                                                            [row['WeekDay'], concat_rowdata_to_date(row), concat_rowdata_to_HHMMSS(row)]]
                                                elif row['VehicleJourneyID'] in Sat[key]:
                                                        Sat[key][row['VehicleJourneyID']].append(
                                                            [row['WeekDay'], concat_rowdata_to_date(row), concat_rowdata_to_HHMMSS(row)])
                #Sun
                for key, value in Sun.items():
                        if row['Day'] >= 2:
                                if row['WeekDay'] == 6:
                                        if str(row['Year']) == key:
                                                if row['VehicleJourneyID'] not in Sun[key]:
                                                        Sun[key][row['VehicleJourneyID']] = [
                                                                [row['WeekDay'], concat_rowdata_to_date(row), concat_rowdata_to_HHMMSS(row)]]
                                                elif row['VehicleJourneyID'] in Sun[key]:
                                                        Sun[key][row['VehicleJourneyID']].append(
                                                                [row['WeekDay'], concat_rowdata_to_date(row), concat_rowdata_to_HHMMSS(row)])
        mon_fri_file = jpid + "mfFreq.txt"
        saturday_file = jpid + "satFreq.txt"
        sunday_file = jpid + "sunFreq.txt"
        #write dicts to txt files as strings
        with open(mon_fri_file, 'w') as output:
            output.write(str(Weekday))
        with open(saturday_file, 'w') as output:
            output.write(str(Sat))
        with open(sunday_file, 'w') as output:
            output.write(str(Sun))
        return Weekday, Sat, Sun



def remove_bad_VJIDs(dictWeek):
        """return dicts without trip data before 2nd January, 2013 when consistent vjid system came into use
        Error resoled: vjids with single entries not useful, these are values from old, inconsistent numbering system. New system groups trips by start times.
        NOTE: RuntimeError: dictionary changed size during iteration; couldn't drop values during iteration, so add values to be dropped to list and go through list when iteration is over
        Resolved: write values to remove to list and remove once iteration is complete."""

        drop_list = []
        for key, value in dictWeek["2013"].items():
                if len(dictWeek["2013"][key]) == 0:
                        drop_list.append(key)
        for x in drop_list:
                del dictWeek["2013"][x]
        new_dictWeek = dictWeek
        return new_dictWeek



def nearest_minute(new_dictWeek):
        """get average start time from all instances of vehicle journey running and returns start time as HHMM"""
        schedule = []
        for key, value in new_dictWeek["2013"].items():  # each key is a different daily bus during the weekdays
                number_of_vjid_runs = 0
                sum_of_start_times_Secs = 0

                for line in new_dictWeek["2013"][key]:
                        number_of_vjid_runs += 1
                        sum_of_start_times_Secs += HHMMSS_to_seconds(str(line[2]))

                avg_start_time_Secs = sum_of_start_times_Secs / number_of_vjid_runs
                start_avg_HHMMSS = convert_seconds_to_HHMMSS(avg_start_time_Secs)
                if int(start_avg_HHMMSS[4:6]) > 30: #round up seconds to a minute if > 30
                        start_avg_HHMMSS = start_avg_HHMMSS[0:4] + str(int(start_avg_HHMMSS[4]) + 1) + start_avg_HHMMSS[4:6]
                start_avg_HHMM = start_avg_HHMMSS[0:4]
                schedule.append(start_avg_HHMM)
                schedule.sort(key=float)
        #print(schedule)
        return schedule



def tidy_schedule(schedule):
        """given schedule make new rounded out times"""
        newSchedule = []
        for x in schedule:
                if int(x[3]) < 4 and int(x[3]) >= 1:    # x[3] = HHM(M)SS, # example: 10:43 or less becomes 10:40. Early estimations are preferable than late estimations
                        x = x[:3] + "0"
                elif int(x[3]) <= 7 and int(x[3]) >= 4: # example: 10:44 to 10:47 -> 10:45, online start times generally end on a "0" or "5"
                        x = x[:3] + "5"
                elif int(x[3]) >= 8:                    # example: 10:48, 10:49 becomes 10:50
                        x = x[:2] + str(int(x[2]) + 1) + "0"
                if int(x[2]) >= 6:                      #x[2] = HH(M)M, 1870
                        if int(x[1]) < 9:               #x[1] = H(H)MM, 1870
                                third_value = int(x[2]) % 6             #1870, 7 % 6 = 1
                                x = x[:1] + str(int(x[1]) + 1) + str(third_value) + "0" #turn over an hour if 60 in minutes is reached, assign third value the remainder e.g. 1870 -> 1910
                                newSchedule.append(x)
                        else:
                                x = str(int(x[0]) + 1) + "0" + x[3] + "0"  # turn over an hour if 60 is reached
                                newSchedule.append(x)
                else:
                        newSchedule.append(x)
        return newSchedule



def remove_duplicates(newSchedule):
        """return list of unique start times for a single route, delete duplicates from schedule.
        Data contains runs of vjids having same average start times, ie.
        on route 7, vjid 102 & vjid 163 start at 0900, no need for both, two buses on same route can't depart at the same time"""
        list_of_start_times = []
        for start_time in newSchedule:
            if start_time not in list_of_start_times:
                list_of_start_times.append(start_time)
        return list_of_start_times



def generate_jsonfile(jpid, final_dict_schedule):
        """write each complete, cleaned schedule to a jpid named json file"""
        os.chdir("results")
        j = json.dumps(final_dict_schedule)
        load_json = json.loads(j)
        jsonfile = "tt" + str(jpid) + ".json"
        with open(jsonfile, mode='w', encoding='UTF-8') as outfile:
                json.dump(load_json, outfile)
        os.chdir("..") #leave results folder to start on next journey pattern



def generate_timetable(filename):
        """each file of one journey pattern id passed in, calls each function to generate a timetable for given jpid"""
        jpid = str(filename[0:8])
        df = pd.read_csv(filename)

        dfFirst, first_stop_id, last_stop_id = get_first_and_last_stop_refine_df(jpid, df) #look only at entries with stopseq == 0
        list_of_dates = get_all_dates(dfFirst)
        Weekday, Sat, Sun = generate_dicts_weekly_schedules(jpid, list_of_dates, dfFirst) #return 3 dicts for MF, Sa, Su schedules
        # output_list = []
        #final_dict = {'vjids':{}}

        final_dict_schedule = {}
        dict_of_3_schedules = {'Weekday': Weekday, 'Sat': Sat, 'Sun': Sun}
        final_dict_schedule['jpid'] = [jpid]
        final_dict_schedule['start_stop'] = first_stop_id #initialise final dict and add key holding first and last stop
        final_dict_schedule['end_stop'] = last_stop_id #initialise final dict and add key holding first and last stop

        for name, value in dict_of_3_schedules.items(): #values = (Weekday, Sat, Sun) Each holding different dicts with format {vjid: [day-of-week, DDMMYYYY, HHMMSS]}
                new_dictWeek = remove_bad_VJIDs(value) #remove value if it occurs before 02-01-2013, data has inconsistent vjid usage
                schedule = nearest_minute(new_dictWeek) #get schedule times to nearest minute
                newSchedule = tidy_schedule(schedule) #returns schedule with HHMM rounded out
                list_of_start_times = remove_duplicates(newSchedule) #returns list of unique bus departure times
                final_dict_schedule[name] = list_of_start_times
                #output_list.append(final_dict_schedule) #add complete schedules (3 in total for each journey pattern) to output
                generate_jsonfile(jpid, final_dict_schedule) #make returned dict in json file



"""file begins here"""
start_clock = time.time()
print(start_clock)
os.chdir("clean_data")
#output_list = []

for filename in os.listdir(os.getcwd()):
        if filename.endswith(".csv"):
                f = filename
                print("reading file:", f)
                generate_timetable(f)
        else:
                continue

#print(output_list)
print("script finished")
print("--- %s seconds ---" % (time.time() - start_clock))