from flask import Flask, render_template, request
import random

app = Flask(__name__, template_folder="templates")

# Sample quotes database (you can replace this with your own database or API)
quotes = {
    'motivational': [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill"
    ],
    'funny': [
        "I'm not lazy, I'm on energy-saving mode.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "I told my computer I needed a break, and now it won't stop sending me vacation ads."
    ],
    'inspirational': [
        "The best way to predict the future is to invent it. - Alan Kay",
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt",
        "In the middle of difficulty lies opportunity. - Albert Einstein"
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quote', methods=['POST'])
def generate_quote():
    category = request.form['category']
    if category in quotes:
        quote = random.choice(quotes[category])
        return render_template('quote.html', quote=quote)
    else:
        return "Invalid category"

if __name__ == '__main__':
    app.run(debug=True)
