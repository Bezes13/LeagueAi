import requests
import csv
import time

api_key = "RGAPI-566bf67f-e145-454a-ac1e-4c8004debd51"
off_time = 5
region = "euw1"
regionMatch = "europe"


def get_summoner_info(summoner_name):
    base_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    return execute_request(base_url)


def get_matches(puuid):
    base_url = f"https://{regionMatch}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    return execute_request(base_url)


def get_match(match_id):
    base_url = f"https://{regionMatch}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    return execute_request(base_url)


def get_high_league(league):
    base_url = f"https://{region}.api.riotgames.com/lol/league/v4/{league}/by-queue/RANKED_SOLO_5x5"
    return execute_request(base_url)


def execute_request(base_url):
    header = {
        "X-Riot-Token": api_key
    }
    try:
        response = requests.get(base_url, headers=header)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Fehler bei der API-Anfrage. Status-Code: {response.status_code}")
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
        info = get_summoner_info(name)
        while info is None:
            time.sleep(off_time)
            info = get_summoner_info(name)
        matches = get_matches(info['puuid'])
        while matches is None:
            time.sleep(off_time)
            matches = get_matches(info['puuid'])
        for matchID in matches:
            entry = []
            match = get_match(matchID)
            while match is None:
                time.sleep(off_time)
                match = get_match(matchID)
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

            for p in players0:
                entry.append(p)
            for p in players1:
                entry.append(p)
            if not data.__contains__(matchID):
                data[matchID] = entry

        with open('matches.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            for row in data.values():
                csv_writer.writerow(row)
                csv_writer.writerow(invert_data(row))


def add_challenger_games(data):
    league = get_high_league("challengerleagues")
    players = league['entries']
    add_data(players, data)


def add_master_games(data):
    league = get_high_league('masterleagues')
    players = league['entries']
    add_data(players, data)


def add_grandmaster_games(data):
    league = get_high_league('grandmasterleagues')
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


if __name__ == "__main__":
    data = {}
    add_challenger_games(data)
    add_master_games(data)
    add_grandmaster_games(data)
    with open('matches.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        for row in data.values():
            csv_writer.writerow(row)
            csv_writer.writerow(invert_data(row))
