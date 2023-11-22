'''
    Get PUUID (player identifiers) given each region's list of summoner names.
    We need the identifiers because we can't get the matches directly from the summoner name.
    We'll use a command line argument for the region, so that we can run a version of this 
    program for each region simoultaneously, since API rate limits apply to each region separately.
'''

import json
import time
import sys
from tqdm import tqdm
from api_funcs import get_puuid

# get our configuration
f = open('config.json')
config = json.load(f)
f.close()

# get argument for region to run this on
region = sys.argv[1]

# get previously fetched summoner names
f = open('summoner_names.json')
all_names = json.load(f)
f.close()
region_names = all_names[region]

print("START: Going to fetch the identifiers")
puuids = {"puuids":[]}
call_count = 0
start = time.time()

for name in tqdm(region_names):
    if call_count > 20: # sleep for a while after many calls so as to not exceed rate limits
        time.sleep(5)
        call_count = 0
    
    curr_id = get_puuid(config,region,name)
    call_count += 1
    
    if curr_id is not None:
        puuids["puuids"] += [curr_id]
    
with open(f"{region}_puuids.json", "w") as outfile:
    outfile.write(json.dumps(puuids, indent=4))

print(f"DONE: Saved identifiers names in {time.time()-start} seconds.")