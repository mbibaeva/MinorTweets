from flask import Flask
from flask import render_template, request, redirect, url_for
from collections import Counter, defaultdict, OrderedDict
import json
import re
import itertools
import http.client, urllib.request, urllib.parse, urllib.error, requests, base64
import pandas as pd
import db_handler
import twitter_api

app = Flask(__name__)
#tools = handler.Tools()

#@app.route('/', methods=['get'])
#def index():
#    return render_template('index.html')

@app.route('/', methods = ['get'])
def main():
    return render_template('main.html')



@app.route('/tatar', methods = ['post', 'get'])
def display_tatar():
    #df = pd.read_csv('all_data.csv', sep=';').fillna('')
    #names = tools.display_all()

    return render_template('tatar.html', tweets=[])


if __name__ == '__main__':
    app.run()