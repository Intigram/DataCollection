import requests

'''
    Get 50 first summoner names in a given division, by region
'''
def get_first_players(config, region, tier, division=None, queue="RANKED_SOLO_5x5", sz=50):
    # api-endpoint
    if division is not None:    # if below the apex tiers (where there are divisions)
        URL = f"https://{region}.{config['api_endpoint']}{config['league']}entries/{queue}/{tier}/{division}"
        
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'page':1}
        
        # sending get request and saving the response as response object
        try:
            r = requests.get(url = URL, params = PARAMS, headers = {"X-Riot-Token": config["api_key"]})
            data = r.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR:\n{e}")
            return None
    else:                       # the apex tiers have a different call
        URL = f"https://{region}.{config['api_endpoint']}{config['league']}{tier.lower()}leagues/by-queue/{queue}"
        # sending get request and saving the response as response object
        try:
            r = requests.get(url = URL, headers = {"X-Riot-Token": config["api_key"]})
            data = r.json()
            data = data["entries"]
        except requests.exceptions.RequestException as e:
            print(f"ERROR:\n{e}")
            return None
    
    # extracting data in json format
    return [p["summonerName"] for p in data[:sz]]

'''
    Get a player's PUUID given a summoner name
'''
def get_puuid(config, region, summoner_name):
    URL = f"https://{region}.{config['api_endpoint']}{config['summoner']}{summoner_name}"
    # sending get request and saving the response as response object
    try:
        r = requests.get(url = URL, headers = {"X-Riot-Token": config["api_key"]})
        data = r.json()
        if r.status_code == 200:
            return data["puuid"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"ERROR:\n{e}")
        return None

'''
    Get 100 match IDs given a PUUID
'''
def get_match_ids(config,region,puuid,count=100,type="ranked"):
    URL = f"https://{region}.{config['api_endpoint']}{config['match']}by-puuid/{puuid}/ids"
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'count':count, 'type':type}
    
    # sending get request and saving the response as response object
    try:
        r = requests.get(url = URL, params=PARAMS, headers = {"X-Riot-Token": config["api_key"]})
        data = r.json()
        if r.status_code == 200:
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"ERROR:\n{e}")
        return None
    
'''
    Get match data from a match ID
'''
def get_match_data(config,region,match_id):
    URL = f"https://{region}.{config['api_endpoint']}{config['match']}{match_id}"
    
    # sending get request and saving the response as response object
    try:
        r = requests.get(url = URL, headers = {"X-Riot-Token": config["api_key"]})
        data = r.json()
        if r.status_code == 200 and len(data["info"]["participants"])>0 and not data["info"]["participants"][0]["gameEndedInEarlySurrender"]:
            return data["info"]
        elif r.status_code == 403:
            return 403
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"ERROR:\n{e}")
        return None