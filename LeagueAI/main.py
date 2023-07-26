import requests
import csv
import time
api_key = "RGAPI-fdcb7d1c-1f16-4d95-b9e6-8fb60da77e64"
offtime = 5

def get_summoner_info(api_key, region, summoner_name):
    base_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": api_key
    }
    return execute_request(base_url, headers)


def get_matches(api_key, region, puuid):
    base_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {
        "X-Riot-Token": api_key
    }
    return execute_request(base_url, headers)


def get_match(api_key, region, matchId):
    base_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}"
    headers = {
        "X-Riot-Token": api_key
    }
    return execute_request(base_url, headers)


def get_high_league(api_key, region, league):
    base_url = f"https://{region}.api.riotgames.com/lol/league/v4/{league}/by-queue/RANKED_SOLO_5x5"
    headers = {
        "X-Riot-Token": api_key
    }
    return execute_request(base_url, headers)


def execute_request(base_url, header):
    try:
        response = requests.get(base_url, headers=header)

        # Überprüfen, ob die Anfrage erfolgreich war (Status-Code 200)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            #print(f"Fehler bei der API-Anfrage. Status-Code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None


def add_data(players, data):
    count = len(players)
    player_index = 0
    for player in players:
        print(str(player_index) + "/" + str(count))
        player_index += 1
        name = player['summonerName']
        info = get_summoner_info(api_key, region, name)
        while info is None:
            time.sleep(offtime)
            info = get_summoner_info(api_key, region, name)
        matches = get_matches(api_key, regionMatch, info['puuid'])
        while matches is None:
            time.sleep(offtime)
            matches = get_matches(api_key, regionMatch, info['puuid'])
        for matchID in matches:
            entry = []
            match = get_match(api_key, regionMatch, matchID)
            while match is None:
                time.sleep(offtime)
                match = get_match(api_key, regionMatch, matchID)
            mode = match['info']['gameMode']
            if not mode == 'CLASSIC':
                continue
            team0 = match['info']['teams'][0]['teamId']
            team1 = match['info']['teams'][1]['teamId']
            if match['info']['teams'][1]['win']:
                win = team1
            else:
                win = team0
            entry.append(win)
            players0 = []
            players1 = []
            for participant in match['info']['participants']:
                if participant['teamId'] == team0:
                    players0.append(participant['championId'])
                else:
                    players1.append(participant['championId'])

            for player in players0:
                entry.append(player)
            for player in players1:
                entry.append(player)
            if not data.__contains__(matchID):
                data[matchID] = entry

        with open('matches.csv', 'w', newline='') as csvfile:
            # CSV-Schreibobjekt erstellen
            csv_writer = csv.writer(csvfile)

            # Daten in die CSV-Datei schreiben
            for row in data.values():
                csv_writer.writerow(row)
                csv_writer.writerow(invert_data(row))



def add_challenger_games(data):
    region = "euw1"
    league = get_high_league(api_key, region, "challengerleagues")
    players = league['entries']
    add_data(players, data)


def add_master_games(data):
    region = "euw1"
    league = get_high_league(api_key, region, 'masterleagues')
    players = league['entries']
    add_data(players, data)


def add_grandmaster_games(data):
    region = "euw1"
    league = get_high_league(api_key, region, 'grandmasterleagues')
    players = league['entries']
    add_data(players, data)


def invert_data(entry):
    new_entry = []
    if entry[0] == 100:
        new_entry.append(200)
    else:
        new_entry.append(100)
    new_entry.extend(entry[6:11])
    new_entry.extend(entry[1:6])
    return new_entry

# Verwendungsbeispiel
if __name__ == "__main__":
    region = "euw1"  # Beispielregion (EU West)
    regionMatch = "europe"
    summoner_name = "Bezes"
    summoner_info = get_summoner_info(api_key, region, summoner_name)
    if summoner_info:
        print(f"Beschwörername: {summoner_info['name']}")
        print(f"Level: {summoner_info['summonerLevel']}")
        print(f"Beschwörer-ID: {summoner_info['id']}")
        print(summoner_info)
    else:
        print("Summoner nicht gefunden oder ein Fehler ist aufgetreten.")
        print(summoner_info)

    data = {}
    add_challenger_games(data)
    add_master_games(data)
    add_grandmaster_games(data)
    with open('matches.csv', 'w', newline='') as csvfile:
        # CSV-Schreibobjekt erstellen
        csv_writer = csv.writer(csvfile)

        # Daten in die CSV-Datei schreiben
        for row in data.values():
            csv_writer.writerow(row)
            csv_writer.writerow(invert_data(row))






