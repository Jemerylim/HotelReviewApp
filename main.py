import json
from pickle import GET
from flask import Flask, render_template, request, jsonify, session, url_for
from flask_cors import CORS, cross_origin
from firebase import firebase
from werkzeug.utils import redirect
import requests
#from flask_navigation import Navigation

app = Flask(__name__)
app.secret_key = 'secret'
fb_app = firebase.FirebaseApplication('https://hotel-review-f7091-default-rtdb.asia-southeast1.firebasedatabase.app/', authentication=None)
displaymessage =''
hotels = ['Campbell Inn', 'Grand Hyatt Singapore', 'Hotel 81 Bugis', 'Ibis Styles Singapore on Macpherson', 'JEN Singapore Orchardgateway by Shangri-La', 'K Hotel 14', 'Lion Peak Hotel Raffles', 'Shangri-La Singapore', 'Studio M Hotel', 'Vintage Inn']

@app.route('/', methods=('GET','POST'))
def main(): 
    if request.method == 'POST':
        if request.form['btn_identifier'] == 'view_button':
            messages = []
            hotel = request.form['reviews']
            messages.append({'hotel':hotel})
            session['hotel'] = messages
            #return render_template("reviews.html", hotels = messages)
            return redirect(url_for('reviewsPage'))

    #elif request.method == 'GET':
        #displaymessage = session['message']

    return render_template("home.html", hotels = hotels)

@app.route('/reviews', methods=('GET','POST'))
def reviewsPage():
    if request.method == "POST":
        return redirect(url_for('reviewsPage'))

    elif request.method =='GET':
       hotel = session['hotel'][0]['hotel']
       reviewdata = fb_app.get('/'+hotel,None)
    return render_template('reviews.html', hotels = hotel, reviewdata = reviewdata)


@app.route('/refresh', methods=('GET','POST'))
def refreshData():
    displaymessage = ''
    if request.method == "POST":
        hotel = request.form['reviewstorefresh']
        messages = []
        messages.append(hotel)
        displaymessage = hotel + ' data has been refreshed.'

        #return redirect(url_for('refreshData'))

        #elif request.method =='GET':
    return render_template('refreshdata.html', hotels = hotels, displaymessage = displaymessage)



@app.route('/makecloud', methods=('GET','POST'))
def cloudpage():
    if request.method == "POST":
        messages = []
        hotel = request.form['hotelname']
        messages.append({'hotel':hotel})
        session['hotel'] = messages
        api_url = 'http://127.0.0.1:5002/api/keywords'
        data = {"query_string" : hotel}
        response = requests.post(api_url,json=data)
        session['keyword'] = (response.json())['keyword']
        
        return redirect(url_for('hotelcloud'))

    return render_template('viewcloud.html', hotels = hotels)


@app.route('/hotelcloud', methods=('GET','POST'))
def hotelcloud():
    if request.method == "POST":
        
        return redirect(url_for('reviewsPage'))

    elif request.method =='GET':
       keyword = session['keyword'] 
       hotel = session['hotel'][0]['hotel']
       reviewdata = fb_app.get('/'+hotel,None)
    return render_template('cloud.html', hotels = hotel,keyword =  keyword)



if __name__ == "__main__":
    app.run(debug=True)


#export FLASK_APP=main
#flask run --port 5001