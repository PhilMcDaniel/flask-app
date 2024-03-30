import json
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Replace 'username' with the desired Lichess username
username = 'pcmcd'

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
bullet_df = df[df["format"] == 'Bullet']
blitz_df = df[df["format"] == 'Blitz']
rapid_df = df[df["format"] == 'Rapid']
puzzle_df = df[df["format"] == 'Puzzles']


fig = px.line(bullet_df, x='date', y='rating', title='Rating Over Time')

# Customize the chart
fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Rating',
    xaxis_rangeslider_visible=True
)

# Show the chart
fig.show()