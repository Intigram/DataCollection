'''
    Takes the JSON files for the matches' data, extracts the relevant features and saves
    all of it in tabular form
'''

import os
import pandas as pd
import numpy as np
import json
from tqdm import tqdm
import pickle
import time

np.seterr(divide='ignore', invalid='ignore')
start = time.time()
total_matches = 0

# giving directory name
dirname = './collected_data'
 
# giving file extension
ext = '.json'

# name and location of file to save
final_filename = "../WinModel/data_all.csv"

# creating an empty list to save the data in, and then create the dataframe
to_save = []
 
# iterating over all files
for file in os.listdir(dirname):
    if file.endswith(ext) and '_matches_' in file:
        with open(os.path.join(dirname,file), "r") as jfile:

            data = json.load(jfile)
            data = data["match_data"]

            print(f">> Working through the data in: {file} <<")

            # begin extracting the features for each match in the file
            for m in tqdm(data):

                if m["gameMode"] != 'CLASSIC':
                    continue
                else:
                    # upated running game count
                    total_matches += 1

                    # flag for which side won (0=blue, 1=red)
                    winning_team = 0 if m["teams"][0]["win"] else 1

                    # info for total objectives taken by either sides
                    blue_turrets    = m["teams"][0]["objectives"]["tower"]["kills"]
                    blue_barons     = m["teams"][0]["objectives"]["baron"]["kills"]
                    blue_drakes     = m["teams"][0]["objectives"]["dragon"]["kills"]
                    blue_kills      = m["teams"][0]["objectives"]["champion"]["kills"]
                    blue_inhibs     = m["teams"][0]["objectives"]["inhibitor"]["kills"]
                    blue_heralds    = m["teams"][0]["objectives"]["riftHerald"]["kills"]
                    try:
                        total_blue_elders = m["participants"][0]["challenges"]["teamElderDragonKills"]
                    except KeyError:
                        continue #total_blue_barons = 0

                    red_turrets    = m["teams"][1]["objectives"]["tower"]["kills"]
                    red_barons     = m["teams"][1]["objectives"]["baron"]["kills"]
                    red_drakes     = m["teams"][1]["objectives"]["dragon"]["kills"]
                    red_kills      = m["teams"][1]["objectives"]["champion"]["kills"]
                    red_inhibs     = m["teams"][1]["objectives"]["inhibitor"]["kills"]
                    red_heralds    = m["teams"][1]["objectives"]["riftHerald"]["kills"]
                    try:
                        total_red_elders = m["participants"][5]["challenges"]["teamElderDragonKills"]
                    except KeyError:
                        continue #total_red_elders = 0
                    
                    # info for first major objectives taken by either side (boolean flag)
                    blue_first_blood    = float(m["teams"][0]["objectives"]["champion"]["first"])
                    blue_first_herald   = float(m["teams"][0]["objectives"]["riftHerald"]["first"])
                    blue_first_drake    = float(m["teams"][0]["objectives"]["dragon"]["first"])
                    blue_first_baron    = float(m["teams"][0]["objectives"]["baron"]["first"])
                    blue_first_inhib    = float(m["teams"][0]["objectives"]["inhibitor"]["first"])
                    blue_first_turret   = float(m["teams"][0]["objectives"]["tower"]["first"])
                    # to have soul, the team should have four drakes total not counting elders, i.e.:
                    blue_got_soul = float(m["teams"][0]["objectives"]["dragon"]["kills"] - total_blue_elders == 4)

                    red_first_blood    = float(m["teams"][1]["objectives"]["champion"]["first"])
                    red_first_herald   = float(m["teams"][1]["objectives"]["riftHerald"]["first"])
                    red_first_drake    = float(m["teams"][1]["objectives"]["dragon"]["first"])
                    red_first_baron    = float(m["teams"][1]["objectives"]["baron"]["first"])
                    red_first_inhib    = float(m["teams"][1]["objectives"]["inhibitor"]["first"])
                    red_first_turret   = float(m["teams"][1]["objectives"]["tower"]["first"])
                    # to have soul, the team should have four drakes total not counting elders, i.e.:
                    red_got_soul = float(m["teams"][1]["objectives"]["dragon"]["kills"] - total_red_elders == 4)

                    # info for stats and objectives taken by each player in either side - init
                    blue_player_kills   = []
                    blue_player_xp      = []
                    blue_player_gold    = []
                    blue_player_dmg     = []
                    blue_player_vs      = []
                    red_player_kills   = []
                    red_player_xp      = []
                    red_player_gold    = []
                    red_player_dmg     = []
                    red_player_vs      = []

                    # loop through players to add above data
                    for p in m["participants"]:
                        if p["teamId"] == 100:      # blue side
                            blue_player_kills.append(p["kills"])
                            blue_player_xp.append(p["champExperience"])
                            blue_player_gold.append(p["goldEarned"])
                            blue_player_dmg.append(p["totalDamageDealtToChampions"])
                            blue_player_vs.append(p["visionScore"])
                        elif p["teamId"] == 200:    # red side
                            red_player_kills.append(p["kills"])
                            red_player_xp.append(p["champExperience"])
                            red_player_gold.append(p["goldEarned"])
                            red_player_dmg.append(p["totalDamageDealtToChampions"])
                            red_player_vs.append(p["visionScore"])
                    
                    # calculations for actual features
                    total_blue_kills    = blue_kills / (red_kills + blue_kills) if (red_kills + blue_kills) != 0 else 0
                    total_red_kills     = red_kills / (red_kills + blue_kills) if (red_kills + blue_kills) != 0 else 0

                    total_blue_barons   = blue_barons / (red_barons + blue_barons) if (red_barons + blue_barons) != 0 else 0
                    total_red_barons    = red_barons / (red_barons + blue_barons) if (red_barons + blue_barons) != 0 else 0

                    total_blue_turrets  = blue_turrets / (red_turrets + blue_turrets) if (red_turrets + blue_turrets) != 0 else 0
                    total_red_turrets   = red_turrets / (red_turrets + blue_turrets) if (red_turrets + blue_turrets) != 0 else 0

                    total_blue_drakes   = blue_drakes / (red_drakes + blue_drakes) if (red_drakes + blue_drakes) != 0 else 0
                    total_red_drakes    = red_drakes / (red_drakes + blue_drakes) if (red_drakes + blue_drakes) != 0 else 0

                    total_blue_inhibs   = blue_inhibs / (red_inhibs + blue_inhibs) if (red_inhibs + blue_inhibs) != 0 else 0
                    total_red_inhibs    = red_inhibs / (red_inhibs + blue_inhibs) if (red_inhibs + blue_inhibs) != 0 else 0

                    total_blue_heralds  = blue_heralds / (red_heralds + blue_heralds) if (red_heralds + blue_heralds) != 0 else 0
                    total_red_heralds   = red_heralds / (red_heralds + blue_heralds) if (red_heralds + blue_heralds) != 0 else 0

                    total_blue_gold     = np.sum(blue_player_gold) / (np.sum(blue_player_gold) + np.sum(red_player_gold))
                    total_red_gold      = np.sum(red_player_gold) / (np.sum(blue_player_gold) + np.sum(red_player_gold))

                    total_blue_elders   = total_blue_elders / (total_blue_elders + total_red_elders) if total_blue_elders != 0 else 0
                    total_red_elders    = total_red_elders / (total_blue_elders + total_red_elders) if total_red_elders != 0 else 0

                    total_blue_vs     = np.sum(blue_player_vs) / (np.sum(blue_player_vs) + np.sum(red_player_vs))
                    total_red_vs      = np.sum(red_player_vs) / (np.sum(blue_player_vs) + np.sum(red_player_vs))

                    # calculations of indivudal player-based medians
                    med_blue_kills  = [0,0,0,0,0]
                    med_red_kills   = [0,0,0,0,0]
                    for k in range(5):
                        if (blue_player_kills[k] + red_player_kills[k]) != 0:
                            med_blue_kills[k]   = blue_player_kills[k] / (blue_player_kills[k] + red_player_kills[k])
                            med_red_kills[k]    = red_player_kills[k] / (blue_player_kills[k] + red_player_kills[k])
                    med_blue_kills  = np.median(med_blue_kills)
                    med_red_kills   = np.median(med_red_kills)

                    med_blue_xp  = [0,0,0,0,0]
                    med_red_xp   = [0,0,0,0,0]
                    for k in range(5):
                        if (blue_player_xp[k] + red_player_xp[k]) != 0:
                            med_blue_xp[k]   = blue_player_xp[k] / (blue_player_xp[k] + red_player_xp[k])
                            med_red_xp[k]    = red_player_xp[k] / (blue_player_xp[k] + red_player_xp[k])
                    med_blue_xp  = np.median(med_blue_xp)
                    med_red_xp   = np.median(med_red_xp)

                    med_blue_gold  = [0,0,0,0,0]
                    med_red_gold   = [0,0,0,0,0]
                    for k in range(5):
                        if (blue_player_gold[k] + red_player_gold[k]) != 0:
                            med_blue_gold[k]   = blue_player_gold[k] / (blue_player_gold[k] + red_player_gold[k])
                            med_red_gold[k]    = red_player_gold[k] / (blue_player_gold[k] + red_player_gold[k])
                    med_blue_gold  = np.median(med_blue_gold)
                    med_red_gold   = np.median(med_red_gold)

                    med_blue_dmg  = [0,0,0,0,0]
                    med_red_dmg   = [0,0,0,0,0]
                    for k in range(5):
                        if (blue_player_dmg[k] + red_player_dmg[k]) != 0:
                            med_blue_dmg[k]   = blue_player_dmg[k] / (blue_player_dmg[k] + red_player_dmg[k])
                            med_red_dmg[k]    = red_player_dmg[k] / (blue_player_dmg[k] + red_player_dmg[k])
                    med_blue_dmg  = np.median(med_blue_dmg)
                    med_red_dmg   = np.median(med_red_dmg)

                    med_blue_vs  = [0,0,0,0,0]
                    med_red_vs   = [0,0,0,0,0]
                    for k in range(5):
                        if (blue_player_vs[k] + red_player_vs[k]) != 0:
                            med_blue_vs[k]   = blue_player_vs[k] / (blue_player_vs[k] + red_player_vs[k])
                            med_red_vs[k]    = red_player_vs[k] / (blue_player_vs[k] + red_player_vs[k])
                    med_blue_vs  = np.median(med_blue_vs)
                    med_red_vs   = np.median(med_red_vs)

                    row = [total_blue_barons,total_blue_drakes,total_blue_heralds,total_blue_inhibs,total_blue_kills,total_blue_turrets,
                        blue_first_blood, blue_first_herald, blue_first_drake, blue_first_baron, blue_first_inhib, blue_first_turret, total_blue_vs,
                        total_blue_gold, med_blue_kills, med_blue_xp, med_blue_gold, med_blue_dmg, blue_got_soul, total_blue_elders, med_blue_vs,
                        total_red_barons, total_red_drakes, total_red_heralds, total_red_inhibs, total_red_kills, total_red_turrets,
                        red_first_blood, red_first_herald, red_first_drake, red_first_baron, red_first_inhib, red_first_turret, total_red_vs,
                        total_red_gold, med_red_kills, med_red_xp, med_red_gold, med_red_dmg, red_got_soul, total_red_elders, med_red_vs,
                        winning_team]
                    
                    to_save.append(row)

            # save current state for backup if needed
            with open('df_list.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([to_save], f)

print(">> Going to save data to DataFrame <<")
cols = ["total_blue_barons", "total_blue_drakes", "total_blue_heralds", "total_blue_inhibs", "total_blue_kills", "total_blue_turrets",
        "blue_first_blood", "blue_first_herald", "blue_first_drake", "blue_first_baron", "blue_first_inhib", "blue_first_turret", "total_blue_vs",
        "total_blue_gold", "med_blue_kills", "med_blue_xp", "med_blue_gold", "med_blue_dmg", "blue_got_soul", "total_blue_elders", "med_blue_vs",
        "total_red_barons", "total_red_drakes", "total_red_heralds", "total_red_inhibs", "total_red_kills", "total_red_turrets",
        "red_first_blood", "red_first_herald", "red_first_drake", "red_first_baron", "red_first_inhib", "red_first_turret", "total_red_vs",
        "total_red_gold", "med_red_kills", "med_red_xp", "med_red_gold", "med_red_dmg", "red_got_soul", "total_red_elders", "med_red_vs",
        "winning_team"]
df = pd.DataFrame(to_save, columns=cols)

print(">> Exporting DataFrame to file <<")
df.to_csv(final_filename, index=False)

print(f"=== Done in {time.time()-start} seconds ===")
print(f"\t\t*** Processed a TOTAL of {total_matches} matches ***")
                