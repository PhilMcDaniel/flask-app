from flask import Flask, render_template, request
import lichess

app = Flask(__name__)


# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    # Render the HTML template and pass the visualization data
    return render_template('index.html')


@app.route("/user_summary")
def user_summary_table():
    data = lichess.get_lichess_user_performance_summary("pcmcd")
    return render_template("user_summary_table.html", data=data)

@app.route('/game_history')
def display_dataframe():
    user = "pcmcd"
    number_of_games = 10
    games = lichess.get_lichess_user_game_history(user,number_of_games)
    games_enhanced = lichess.enhance_game_data(games,user)
    df = lichess.create_df_from_data(games_enhanced)
    return render_template('game_history.html', table=df.to_html())


@app.route('/data_viz', methods=['GET', 'POST'])
def data_viz():
    if request.method == 'POST':
        username = request.form['username']
        format_choice = request.form['format_choice']
        plot_div = lichess.plotly_chart(username, format_choice)
        return render_template('data_viz.html', plot_div=plot_div)
    else:
        return render_template('data_viz.html')


if __name__ == '__main__':
    app.run(debug=True)