'''
    Get match data from the lists of MatchIDs.
    We'll use a command line argument for the region, so that we can run a version of this 
    program for each region simoultaneously, since API rate limits apply to each region separately.
'''

import json
import time
import sys
from tqdm import tqdm
from api_funcs import get_match_data

# get our configuration
f = open('config.json')
config = json.load(f)
f.close()

# get argument for region to run this on
region =        sys.argv[1]

# get previously fetched match IDs
f = open(f'{region}_match_ids.json')
region_match_ids = json.load(f)
region_match_ids = region_match_ids["match_ids"]
f.close()

print("START: Going to fetch match data")
try:                                        # try to find a starting point
    f = open(f'{region}_matches_3.json')
    match_data = json.load(f)
    f.close()
    match_data["match_data"] = []   # new list to save this time
    start = match_data["start_time"]
    starting_index = region_match_ids.index(match_data["last_match_id"])
except FileNotFoundError:                   # if there is none, start from the beginning
    match_data = {"match_data":[], "last_match_id":"", "start_time": 0, "stop_time": 0, "restart_time": 0}
    start = time.time()
    match_data["start_time"] = start
    starting_index = 0

call_count = 0
finished = True

for i, match_id in enumerate(tqdm(region_match_ids[starting_index:])):
    
    if call_count == 20: # sleep for a while after many calls so as to not exceed rate limits
        time.sleep(5)
        call_count = 0
    
    curr_data = get_match_data(config,region,match_id)
    call_count += 1
    match_data["last_match_id"] = match_id

    # check if the key was no longer valid, and if so stop
    if curr_data == 403:
        match_data["stop_time"] = time.time()
        finished = False
        break
    
    # otherwise, if we got data, add it to our data object
    if curr_data is not None:
        match_data["match_data"].append(curr_data)

# save current progress
with open(f"{region}_matches_4.json", "w") as outfile:
    outfile.write(json.dumps(match_data, indent=4))

if finished:
    print(f"DONE: Saved match data in {time.time()-start} seconds.")
else:
    print(f"STOP: API key no longer valid in {time.time()-start} seconds.")