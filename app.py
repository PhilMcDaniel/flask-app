from flask import Flask, render_template, request
import lichess

app = Flask(__name__)


# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    # Render the HTML template and pass the visualization data
    return render_template('index.html')


@app.route("/user_summary", methods = ['GET','POST'])
def user_summary():
    if request.method == 'POST':
        username = request.form['username']
        data = lichess.get_lichess_user_performance_summary(username)
        return render_template("user_summary.html", data=data,username = username)
    else:
        return render_template("user_summary.html")

@app.route('/game_history', methods = ['GET','POST'])
def game_history():
    if request.method == 'POST':
        #get user input
        username = request.form['username']
        num_games = int(request.form['num_games'])
        #get game history
        games = lichess.get_lichess_user_game_history(username,num_games)
        games_enhanced = lichess.enhance_game_data(games,username)
        df = lichess.create_df_from_data(games_enhanced)
        #get overall score
        points,available_points = lichess.player_overall_score(username,num_games)
        return render_template('game_history.html', table=df.to_html(),username=username,num_games=num_games,points=points,available_points=available_points)
    else:
        return render_template('game_history.html')
    
@app.route('/results_by_color', methods = ['GET','POST'])
def results_by_color():
    if request.method == 'POST':
        #get user input
        username = request.form['username']
        num_games = int(request.form['num_games'])
        #get game summary
        df = lichess.results_by_color(username,num_games)
        #get overall score
        points,available_points = lichess.player_overall_score(username,num_games)
        return render_template('results_by_color.html', table=df.to_html(),username=username,num_games=num_games,points=points,available_points=available_points)
    else:
        return render_template('results_by_color.html')
    
@app.route('/results_by_opening', methods = ['GET','POST'])
def results_by_opening():
    if request.method == 'POST':
        #get user input
        username = request.form['username']
        num_games = int(request.form['num_games'])
        #get game summary
        df = lichess.results_by_opening(username,num_games)
        #get overall score
        points,available_points = lichess.player_overall_score(username,num_games)
        return render_template('results_by_opening.html', table=df.to_html(),username=username,num_games=num_games,points=points,available_points=available_points)
    else:
        return render_template('results_by_opening.html')

@app.route('/data_viz', methods=['GET', 'POST'])
def data_viz():
    if request.method == 'POST':
        username = request.form['username']
        format_choice = request.form['format_choice']
        plot_div = lichess.plotly_chart(username, format_choice)
        return render_template('data_viz.html', plot_div=plot_div,username = username,format_choice = format_choice)
    else:
        return render_template('data_viz.html')


if __name__ == '__main__':
    app.run(debug=True)