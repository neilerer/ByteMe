#find_empty_timetable_files.py

#imports
import os
import os.path
import time
import json


def find_empty_files():
        """return list of files with empty schedule dicts"""
        empty_files = []
        for filename in os.listdir(os.getcwd()):
                if filename.endswith(".json"):
                        f = filename
                        print("reading file:", f)
                else:
                        continue
                with open(f, "r") as jsonfile:
                        if f not in empty_files:
                                load_j = json.load(jsonfile)
                                if len(load_j['Weekday']) == 0:
                                        if len(load_j['Sat']) == 0:
                                                if len(load_j['Sun']) == 0:
                                                        empty_files.append(f)
        return empty_files

def remove_empty_tt_files(empty_files):
        for filename in os.listdir(os.getcwd()):
                if filename.endswith(".json") and filename in empty_files:
                        os.remove(filename)
                else:
                        continue


start = time.time()
print(os.getcwd())
os.chdir("clean_data/results")
start_file_count = len([name for name in os.listdir('.') if os.path.isfile(name) if name.endswith(".json")])
print("number of json files: ", start_file_count)
empty_files = find_empty_files()
remove_empty_tt_files(empty_files)


print("--- %s seconds ---" % (time.time() - start))
final_file_count = len([name for name in os.listdir('.') if os.path.isfile(name) if name.endswith(".json")])

print("number of json files before cleaning: ", start_file_count)
print("final count of json files: ", final_file_count)
print("files removed: ", int(start_file_count) - int(final_file_count))
print("script finished")

"""
OUTPUT:
...
reading file: tt084X1002.json
--- 0.3002943992614746 seconds ---
number of json files before cleaning:  477
final count of json files:  418
files removed: 59
script finished
"""