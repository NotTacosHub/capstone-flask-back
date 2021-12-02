from flask import json, jsonify
from app import app
from dotenv import load_dotenv
import facebook
import os
from flask_cors import CORS
CORS(app)
load_dotenv()


FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')


def getposts():
    graph = facebook.GraphAPI(access_token=FB_ACCESS_TOKEN, version="2.12")
    myinfo = graph.get_object(id='4716878148369487', fields='posts')
    return jsonify(myinfo)


def getpostinfo(postid):
    graph = facebook.GraphAPI(access_token=FB_ACCESS_TOKEN, version="2.12")
    mypostinfo = graph.get_object(id=postid, fields='message,created_time')
    return jsonify(mypostinfo)
