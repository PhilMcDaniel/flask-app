import plotly.graph_objs as go
from flask import Flask, render_template, request
import lichess

app = Flask(__name__)


# Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    username = request.form.get('username', 'pcmcd') #default to me
    format_choice = request.form.get('format', 'Puzzles')  # Default to 'Puzzle'
    bullet_df = lichess.get_lichess_rating_history(username,format_choice)
    # Create the trace for the line plot
    trace = go.Scatter(
        x=bullet_df['date'],
        y=bullet_df['rating'],
        mode='lines',
        name='Rating'
    )

    # Create the layout
    layout = go.Layout(
        title=f'Rating by Date for User: {username}, Format: {format_choice}',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Rating')
    )

    # Create the plot data
    plot_data = [trace]
    fig = go.Figure(data=plot_data, layout=layout)

    # Convert the figure to an HTML string
    plot_div = fig.to_html(full_html=False)

    # Render the HTML template and pass the visualization data
    return render_template('index.html', plot=plot_div, username=username, format_choice=format_choice)

if __name__ == '__main__':
    app.run(debug=True)