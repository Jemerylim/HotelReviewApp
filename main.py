from pickle import GET
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route('/', methods=('GET','POST'))
def main():
    if request.method == 'POST':
        messages = []
        hotel = request.form['reviews']
        messages.append({'hotel':hotel})
        return render_template("reviews.html", hotels = messages)

    hotels = ['k hotel', 'hotel 81', 'diamonds']
    return render_template("home.html", hotels = hotels)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/reviews')
def reviewsPage():
    #value 
    return render_template("reviews.html")