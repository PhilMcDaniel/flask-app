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
