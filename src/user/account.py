# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30
# Get temp token for OAuth use.
from src.io import send

def get_user_info_url(version="1"):
    return "http://openapi.kuaipan.cn/%s/account_info" % version    

class Account:
    def __init__(self):        
        user_data = send(get_user_info_url())
        self.max_file_size = user_data['max_file_size']
        self.user_name = user_data['user_name']
        self.quota_used = user_data['quota_used']
        self.quota_total = user_data['quota_total']
        self.user_id = user_data['user_id']

if __name__ == "__main__":
    user = Account()
    print user.user_name, user.user_id, user.quota_used