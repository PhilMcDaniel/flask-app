import plotly.graph_objs as go
from flask import Flask, render_template, request
import lichess

app = Flask(__name__)


# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    #user inputs
    username = request.form.get('username', 'pcmcd') #default to me
    format_choice = request.form.get('format', 'Puzzles')  # Default to 'Puzzle'
    
    #getting data from Lichess API
    df = lichess.get_lichess_rating_history(username,format_choice)
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

    # Render the HTML template and pass the visualization data
    return render_template('index.html', plot=plot_div, username=username, format_choice=format_choice)


@app.route("/user_summary_table")
def user_summary_table():
    data = lichess.get_lichess_user_performance_summary("pcmcd")
    return render_template("user_summary_table.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)