import json
import requests
import pandas as pd
from datetime import datetime

# Replace 'username' with the desired Lichess username
def get_lichess_rating_history(username,rating_type):

    # Fetch the user's rating history from the Lichess API
    url = f'https://lichess.org/api/user/{username}/rating-history'
    response = requests.get(url)
    data = response.json()
    #print(json.dumps(data,indent=0))

    rating_list = []
    for mode in data:
        format = mode.get('name')
        for points in mode.get('points'):
            date = datetime(points[0], points[1]+1, points[2])
            rating = points[3]
            rating_list.append([username,format,date,rating])
            
    #print(rating_list)
    df = pd.DataFrame(rating_list,columns=['username', 'format', 'date','rating'])
    df.head(10)
    # ['Bullet' 'Blitz' 'Rapid' 'Puzzles']
    df = df[df["format"] == rating_type]

    #bullet_df.head(10)

    return df

#df = get_lichess_rating_history('pcmcd','Puzzles')
#df.head(10)


def get_lichess_user_performance_summary(username):
    data_list = []
    url = f'https://lichess.org/api/user/{username}'
    response = requests.get(url)
    data = response.json()
    
    #remove some that don't have same columns
    del data['perfs']["streak"]
    del data['perfs']["racer"]

    return data.get("perfs")


def get_lichess_user_game_history(username,number_of_games):

    url = f'https://lichess.org/api/games/user/{username}'
    headers = {'Accept':'application/x-ndjson'}
    params = {
        "max":{number_of_games},
        "sort":"dateDesc",
        "opening":True,
        "moves":False
              }
    resp = requests.get(url=url,headers=headers,params=params)
    
    #split the ndjson games
    lines = resp.text.strip().split("\n")
    # Convert each line to a dictionary and collect them in a list
    games = []
    for line in lines:
        games.append(json.loads(line))
    
    return games

games = get_lichess_user_game_history("pcmcd",2)


# func for wins/losses by opening

# visualize it