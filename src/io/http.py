# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30
# Get temp token for OAuth use.

from src.oauth import Oauth
import urllib2
try:
    import simplejson as json
except ImportError: # For Python >= 2.6
    import json    

consumer_secret = "3EXyGMBqO4ThDaVn"
consumer_key = "xcc2DBt6hE3XLgtd"
#TODO: change these methods read from config / database
def get_oauth_token():
    return "0018a77e6645c6a218d13b14"

def get_oauth_token_secret():
    return "3b74c39cf7f8459abeeb451c8564d7ca"

def get_consumer_key():
    return "xcc2DBt6hE3XLgtd"

def get_consumer_secret():
    return "3EXyGMBqO4ThDaVn"

import time

def send(url, params={}):
    _time = str(int(time.time()))
    _params = dict(
        oauth_consumer_key=get_consumer_key(),
        oauth_nonce="x" + _time,
        oauth_signature_method="HMAC-SHA1",
        oauth_timestamp=_time,
        oauth_version="1.0",
        oauth_token=get_oauth_token(),
    )
    
    _params.update(params)
    _base_string = Oauth.build_base_string(_params, url)
    _params["oauth_signature"] = Oauth.generate_oauth_signature(_base_string,
                                                                get_consumer_secret(), 
                                                                get_oauth_token_secret())
    _url = Oauth.generate_url(url, _params)

    h = urllib2.Request(_url)
    res = urllib2.urlopen(h)
    json_response = json.loads(res.read()) #TODO: deal with every http error code
    res.close()
    
    return json_response