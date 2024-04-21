import json
import requests
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go

# Replace 'username' with the desired Lichess username
def get_lichess_rating_history(username='pcmcd',rating_type='Blitz'):

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


def get_lichess_user_performance_summary(username='pcmcd'):
    data_list = []
    url = f'https://lichess.org/api/user/{username}'
    response = requests.get(url)
    data = response.json()
    
    #remove some that don't have same columns
    del data['perfs']["streak"]
    del data['perfs']["racer"]

    return data.get("perfs")


def get_lichess_user_game_history(username='pcmcd',number_of_games='10'):

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

def enhance_game_data(games,user):
    games_list = []

    for game in games:
        game_dict = {}
        game_id = game.get("id")
        rated = game.get("rated")
        match_type = game.get("variant")
        match_speed = game.get("speed")
        status = game.get("status")
    
        start_date = datetime.fromtimestamp(game.get("createdAt")/1000)
        white = game.get("players").get("white").get("user").get("name")
        white_rating = game.get("players").get("white").get("rating")
        black = game.get("players").get("black").get("user").get("name")
        black_rating = game.get("players").get("black").get("rating")
        winner = game.get("winner")
        opening = game.get("opening").get("name")
        start_clock_time = game.get("clock").get("initial")
        clock_increment = game.get("clock").get("increment")
        total_game_duration = game.get("clock").get("totalTime")
        
        if user.lower().strip() == white.lower().strip():
            user_color = "white"
        else: 
            user_color = "black"
        
        if winner is None:
            user_result = "draw"
        elif user_color == winner:
            user_result = "win"
        else:
            user_result = "loss"

        if user_result == "draw":
            user_score = .5
        elif user_result == "win":
            user_score = 1
        elif user_result == "loss":
            user_score = 0
        else:
            user_score = None
        
        game_dict["game_id"] = game_id
        game_dict["rated"] = rated
        game_dict["match_type"] = match_type
        game_dict["match_speed"] = match_speed
        game_dict["status"] = status
        game_dict["start_date"] = start_date
        game_dict["white"] = white
        game_dict["white_rating"] = white_rating
        game_dict["black"] = black
        game_dict["black_rating"] = black_rating
        game_dict["winner"] = winner
        game_dict["opening"] = opening
        game_dict["start_clock_time"] = start_clock_time
        game_dict["clock_increment"] = clock_increment
        game_dict["total_game_duration"] = total_game_duration
        game_dict["user_result"] = user_result
        game_dict["user_color"] = user_color
        game_dict["user_score"] = user_score
        
        games_list.append(game_dict)
    
    return games_list
    
def create_df_from_data(data):
    df = pd.DataFrame(data)
    return df

def results_by_color(username="pcmcd",games=10):
    data = get_lichess_user_game_history(username,games)
    data = enhance_game_data(data,username)
    df= create_df_from_data(data)

    result_by_color_df = df.groupby('user_color').agg({'user_score': 'sum','game_id':'count'}).reset_index()
    result_by_color_df.columns = ['color', 'score', 'games']
    result_by_color_df = result_by_color_df.sort_values(by=['games','score','color'], ascending=[False,False,True])

    return result_by_color_df

def results_by_opening(username="pcmcd",games=10):
    data = get_lichess_user_game_history(username,games)
    data = enhance_game_data(data,username)
    df = create_df_from_data(data)
    result_by_opening_df = df.groupby('opening').agg({'user_score': 'sum','game_id':'count'}).reset_index()
    result_by_opening_df.columns = ['opening', 'score', 'games']
    result_by_opening_df = result_by_opening_df.sort_values(by=['games','score','opening'], ascending=[False,False,True])

    return result_by_opening_df

def player_overall_score(username="pcmcd",games=10):
    data = get_lichess_user_game_history(username,games)
    data = enhance_game_data(data,username)
    df = create_df_from_data(data)
    score_df = df["user_score"].sum()
    
    return (score_df,games)

def plotly_chart(username='pcmcd', format_choice='Blitz'):
    #getting data from Lichess API
    df = get_lichess_rating_history(username,format_choice)
    #calculate min and max for annotations
    min_rating = df['rating'].min()
    max_rating = df['rating'].max()

    # Get the dates associated with the minimum and maximum rating values
    date_min_rating = df['date'].loc[df['rating'].idxmin()].date()
    date_max_rating = df['date'].loc[df['rating'].idxmax()].date()

    # Create the trace for the line plot
    trace = go.Scatter(
        x=df['date'],
        y=df['rating'],
        mode='lines',
        name='Rating'
    )

    # Create the layout
    layout = go.Layout(
        title=f'Rating by Date for User: {username}, Format: {format_choice}',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Rating'),
        autosize=True,
        #width=2000,
        height=500,
        paper_bgcolor="LightSteelBlue",
    )

    # Create the plot data
    plot_data = [trace]
    fig = go.Figure(data=plot_data, layout=layout)

    # Add annotations
    fig.add_annotation(
        x=date_min_rating,
        y=min_rating,
        text=f"Low of {min_rating} on {date_min_rating}",
        showarrow=False,
        xanchor="auto",
        yshift=-10,
    )
    fig.add_annotation(
        x=date_max_rating,
        y=max_rating,
        text=f"High of {max_rating} on {date_max_rating}",
        showarrow=False,
        xanchor="auto",
        yshift=10,
    )

    # Convert the figure to an HTML string
    plot_div = fig.to_html(full_html=False)
    return plot_div