'''
    Get players and save into file first 50 summoner names, for each region
'''

import json
import time
from api_funcs import get_first_players

# get our configuration
f = open('config.json')
config = json.load(f)

print("START: Going to fetch the summoner names")
summ_names = {}
call_count = 0
start = time.time()

for region in config["league_regions"]:
    if call_count > 0: # sleep for a while after many calls so as to not exceed rate limits
        time.sleep(5)
        call_count = 0
    
    region_list = list()    # list of summoner names in each region
    
    for tier in config["tiers"]:
        if tier not in ["MASTER", "GRANDMASTER", "CHALLENGER"]:
            for division in config["divisions"]:
                names = get_first_players(config,region,tier,division)
                call_count += 1
                region_list += names
                print(f"Fetched players from {region} {tier} {division}")
        else:
            data = get_first_players(config,region,tier)
            call_count += 1
            region_list += names
            print(f"Fetched players from {region} {tier}")
    summ_names[region] = region_list
    
with open("summoner_names.json", "w") as outfile:
    outfile.write(json.dumps(summ_names, indent=4))

print(f"DONE: Saved summoner names in {time.time()-start} seconds.")