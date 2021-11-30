from logging import PlaceHolder
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import requests, json
import random

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# create an instance of Flask
app = Flask(__name__) 
bootstrap = Bootstrap(app)
# route decorator binds a function to a URL

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

key1 = '2751705df8c40b34efbd798cf7bdf9b6' 
key2 = '0d1d9d2ae255bb02b8d7fb4c90879192'
keys = [key1,key2] #two API keys 

class Location(FlaskForm):
    name = StringField('City', validators=[DataRequired()])

@app.route('/',methods=('GET', 'POST'))
def hello():
    form = Location()
    city = "United States"
    if form.validate_on_submit():
        city = form.name.data
        city = " ".join(city.split()) #strip lead and trailing spaces

    api_key = keys[random.randint(0,1)] #randomly pick an api key
    try:
        loc = requests.get('http://ip-api.com/json/') #documentation here: https://ip-api.com/docs
        loc_data = loc.json()
        if city=="United States": #default
            r = requests.get('https://gnews.io/api/v4/top-headlines?lang=en&topic=nation&country=us&token='+api_key+'')
        else: #search term
            r = requests.get('https://gnews.io/api/v4/search?q='+city+'&lang=en&country=us&token='+api_key+'')
        data = r.json()
        
    except:
        output = 'failed'
    return render_template('template.html',data=data,form=form,cit=city,loc_data=loc_data)

#<center>
#<div>
#<form method="POST" action="/">
#    {{ form.csrf_token }}
#    {{ form.name.label }} {{ form.name(size=20) }}
#    <input type="submit" value="Go">
#</form>
#</div>
#</center>

  
#<img src={{data['articles'][1]['image']}} width="250">
#<p>{{data['articles'][1]['title']}}</p>
#<p>{{data['articles'][1]['description']}}</p>
#<p>{{data['articles'][1]['url']}}</p>