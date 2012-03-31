# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30
# Send the request to K drive.

from src.oauth import Oauth
from urllib import quote
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
    url = url.encode("UTF-8")
    _time = str(int(time.time()))
    _params = dict(
        oauth_consumer_key=get_consumer_key(),
        oauth_nonce="fqoiwhf" + _time,
        oauth_signature_method="HMAC-SHA1",
        oauth_timestamp=_time,
        oauth_version="1.0",
        oauth_token=get_oauth_token(),
    )
    
    _params.update(params)
    _base_string = Oauth.build_base_string(_params, url)
    print _base_string
    _params["oauth_signature"] = Oauth.generate_oauth_signature(_base_string,
                                                                get_consumer_secret(), 
                                                                get_oauth_token_secret())
#    print _params["oauth_signature"]
    index = url.index("//")
    url = url[:index + 2] + quote(url[index+2:])

    _url = Oauth.generate_url(url, _params)
    print _url

    h = urllib2.Request(_url)
    res = urllib2.urlopen(h)
    json_response = json.loads(res.read()) #TODO: deal with every http error code
    res.close()
    
    return json_response
