# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30
# Get temp token for OAuth use.

#TODO: Using pycurl to boost
from urllib import urlencode, quote as _quote
import hmac, hashlib, base64, time, urllib2

try:
    import simplejson as json
except ImportError: # For Python >= 2.6
    import json
    
def quote(_i):
    return _quote(_i, "")

request_token_url = "https://openapi.kuaipan.cn/open/requestToken"
access_token_url = "https://openapi.kuaipan.cn/open/accessToken"

oauth_verifier = "431222286"
tmp_token = "5afbc858cf5b4c38820313decdd9e1df"
tmp_secret = "de146776e0a748f6a8c6b9047f06807c"

http_method = "GET"

class Oauth:
    def __init__(self):
        pass
    
    def temp_token(self, consumer_key, consumer_secret):
        _time = str(int(time.time()))
        params = dict(
            oauth_consumer_key = consumer_key,
            oauth_nonce = "x" + _time,
            oauth_signature_method = "HMAC-SHA1",
            oauth_timestamp = _time,
            oauth_version = "1.0",
        )
        _base_string = Oauth.build_base_string(params, request_token_url)
        params["oauth_signature"] = Oauth.generate_oauth_signature(_base_string, consumer_secret)
        _url = Oauth.generate_url(request_token_url, params)

        _temp_token_dict = Oauth.process(_url, Oauth.get_tmp_token)
        
        self.temp_oauth_token_secret = _temp_token_dict["oauth_token_secret"]
        self.temp_oauth_token = _temp_token_dict["oauth_token"]
        self.oauth_callback_confirmed = _temp_token_dict["oauth_callback_confirmed"]
    
    def access_token(self, consumer_key, tmp_token, consumer_secret, tmp_secret):
        _time = str(int(time.time()))
        params = dict(
            oauth_consumer_key = consumer_key,
            oauth_nonce = "x" + _time,
            oauth_signature_method = "HMAC-SHA1",
            oauth_timestamp = _time,
            oauth_version = "1.0",
            oauth_token = tmp_token, #TODO: Using true temp token
#            oauth_verifier = oauth_verifier, #TODO: Using true verifier
        )
        _base_string = Oauth.build_base_string(params, access_token_url)
        params["oauth_signature"] = Oauth.generate_oauth_signature(_base_string, consumer_secret, tmp_secret) #TODO: Using true temp secret
        _url = Oauth.generate_url(access_token_url, params)

        token_dict = Oauth.process(_url, Oauth.get_access_token)
    
    @staticmethod
    def build_base_string(params, url): # Notice here the dict has been quoted twice.
        params_str_dict = [quote(k) + "=" + quote(v) for k, v in params.items()]
        params_str_dict.sort()
                
        return ("%s&%s&%s" % (http_method,
                             quote(url),
                             quote("&".join(params_str_dict))))
    
    @staticmethod
    def generate_oauth_signature(base_string, _consumer_secret, _oauth_token_secret=""):
        key = "%s&%s" % (_consumer_secret, _oauth_token_secret)
        _tmp_sig = hmac.new(key, base_string, digestmod=hashlib.sha1).digest()
        return base64.encodestring(_tmp_sig).replace("\n","")
    
    @staticmethod
    def generate_url(url, params):
        return url + "?" + urlencode(params)
        
    @staticmethod
    def process(request_url, operation):
        h = urllib2.Request(request_url)
        res = urllib2.urlopen(h)
        json_response = json.loads(res.read())
        res.close()
        
        return operation(json_response)
        
    @staticmethod
    def get_tmp_token(http_response):
        return dict(oauth_token_secret = http_response["oauth_token_secret"],
                    oauth_token = http_response["oauth_token"],
                    oauth_callback_confirmed = http_response["oauth_callback_confirmed"])
    
    @staticmethod
    def get_access_token(http_response):
        return dict(oauth_token_secret = http_response["oauth_token_secret"],
                    oauth_token = http_response["oauth_token"],
                    charged_dir = http_response["charged_dir"],
                    user_id = http_response["user_id"])

if __name__ == "__main__":
    o = Oauth()
    o.access_token()
#    print o.oauth_token_secret, o.oauth_token, 
