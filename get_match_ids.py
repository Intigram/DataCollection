'''
    Get MatchIds from the lists of player PUUIDs.
    We'll use a command line argument for the region, so that we can run a version of this 
    program for each region simoultaneously, since API rate limits apply to each region separately.
    We also need a play region (EUW, NA or KR), since that's how the PUUIDs were split.
'''

import json
import time
import sys
from tqdm import tqdm
from api_funcs import get_match_ids

# get our configuration
f = open('config.json')
config = json.load(f)
f.close()

# get argument for region to run this on
region =        sys.argv[1]
play_region =   sys.argv[2]

# get previously fetched PUUIDs
f = open(f'{play_region}_puuids.json')
region_puuids = json.load(f)
region_puuids = region_puuids["puuids"]
f.close()

print("START: Going to fetch match identifiers")
match_ids = {"match_ids":[]}
call_count = 0
start = time.time()

for puuid in tqdm(region_puuids):
    if call_count > 20: # sleep for a while after many calls so as to not exceed rate limits
        time.sleep(5)
        call_count = 0
    
    curr_ids = get_match_ids(config,region,puuid)
    call_count += 1
    
    if curr_ids is not None:
        match_ids["match_ids"] += curr_ids
    
with open(f"{region}_match_ids.json", "w") as outfile:
    outfile.write(json.dumps(match_ids, indent=4))

print(f"DONE: Saved match identifiers in {time.time()-start} seconds.")