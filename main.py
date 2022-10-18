import base64
import io
from pickle import GET
from random import random
from string import whitespace
from flask import Flask, render_template, request, jsonify, session, url_for
from flask_cors import CORS, cross_origin
from firebase import firebase
from werkzeug.utils import redirect
import requests
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import  FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import urllib
import numpy as np

app = Flask(__name__)
app.secret_key = 'secret'
fb_app = firebase.FirebaseApplication('https://hotel-review-f7091-default-rtdb.asia-southeast1.firebasedatabase.app/', authentication=None)
displaymessage =''
hotels = ['Campbell Inn', 'Grand Hyatt Singapore', 'Hotel 81 Bugis', 'Ibis Styles Singapore on Macpherson', 'JEN Singapore Orchardgateway by Shangri-La', 'K Hotel 14', 'Lion Peak Hotel Raffles', 'Shangri-La Singapore', 'Studio M Hotel', 'Vintage Inn']
hotelswebsite = {'Campbell Inn': 'https://nomadrest.com/campbell-inn-singapore/', 'K Hotel 14':'https://khotel.co/k-hotel-14/', 'Grand Hyatt Singapore':'https://www.hyatt.com/en-US/hotel/singapore/grand-hyatt-singapore/sinrs', 'Hotel 81 Bugis':'https://www.hotel81.com.sg/hotel81-bugis.shtml', 'Ibis Styles Singapore on Macpherson':'https://all.accor.com/hotel/9411/index.en.shtml?utm_campaign=seo+maps&utm_medium=seo+maps&utm_source=google+Maps&y_source=1_MTUzNjI0MDYtNzE1LWxvY2F0aW9uLndlYnNpdGU%3D', 'JEN Singapore Orchardgateway by Shangri-La':'https://www.shangri-la.com/hotels/jen/','Lion Peak Hotel Raffles':'https://populoushotel.zoombookdirect.com/?utm_source=googlemybusiness&utm_medium=organic&utm_campaign=google_my_business', 'Shangri-La Singapore':'https://www.shangri-la.com/en/singapore/shangrila/', 'Studio M Hotel':'https://www.millenniumhotels.com/en/singapore/studio-m-hotel/', 'Vintage Inn':'http://www.vintageinn.sg'}


""" def plot_wordcloud(data):
    uniquewords = set(data)
    uniquedict={}
    freqlist = []
    for words in uniquewords:
        freqlist.append(data.count(words))
    uniquedict['words'] = list(uniquewords)
    uniquedict['freq'] = freqlist
    dfm = pd.DataFrame(uniquedict)
    d = {a: x for a, x in dfm.values}
    wc = WordCloud(background_color='white', width=1000,height=600)
    wc.fit_words(d)
    return wc.to_image() """

def green_colour_func():
    return ("hsl(119,93%%, %d%%)"% np.random.randint(45,51))


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
       headings = ("Title", "Score", "DateTime", "Review")
       hotel = session['hotel'][0]['hotel']
       reviewdata = fb_app.get('/'+hotel,None)
       return render_template('reviews.html', hotels = hotel, reviewdata = reviewdata, headings = headings, hotelwebsite = hotelswebsite[hotel])


@app.route('/refresh', methods=('GET','POST'))
def refreshData():
    displaymessage = ''
    if request.method == "POST":
        hotel = request.form['reviewstorefresh']
        messages = []
        messages.append(hotel)
        displaymessage = hotel + ' data has been refreshed.'
        api_url = 'http://127.0.0.1:5000/scrapeone'
        data = {"query_string" : hotel}
        response = requests.post(api_url,json=data)
        #return redirect(url_for('refreshData'))

        #elif request.method =='GET':
    return render_template('refreshdata.html', hotels = hotels, displaymessage = displaymessage)



@app.route('/makecloud', methods=('GET','POST'))
def cloudpage():
    if request.method == "POST":
        session['keyword'] = ''
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
       img = io.BytesIO()
       #plot_wordcloud(data=keyword).save(img, format='PNG')
       #fig = WordCloud(collocations = False, background_color = 'white').generate(keyword)
       #plt.imshow(fig, interpolation='bilinear')
       #plt.axis('off')
       #output = io.BytesIO()
       #plt.savefig(output, format='png')
       #data = base64.b64encode(output.getbuffer()).decode("ascii")= base64.b64encode(img.getvalue()).decode(
       #data = base64.b64encode(img.read())
       #data = data.replace("b&#39;", "") 
       #data = data.replace("&#39;", "")
       #basedata = 'data:image/png;base64,'+ data
       try:
            stop_words = ["hostel","hotel","thing"]
            wordcloud = WordCloud(
                background_color="white",max_words=1000,stopwords=stop_words)
            wordcloud.generate(keyword)
            #wordcloud.recolor(color_func=green_colour_func())
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            image = io.BytesIO()
            plt.savefig(image, format="png")
            image.seek(0)
            string = base64.b64encode(image.read())
            image_64 = "data:image/png;base64," +   urllib.parse.quote_plus(string)
            session['keyword'] = ''
            return render_template('cloud.html',img_data = image_64)
       except ValueError:
        return None
       #return render_template('cloud.html',keyword = data,img_data = data)

    return render_template('cloud.html', hotels = hotel,keyword =  keyword)




if __name__ == "__main__":
    app.run(debug=True)


#export FLASK_APP=main
#flask run --port 5001