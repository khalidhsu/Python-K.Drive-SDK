# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30

from http import send

class kfile:
    def __init__(self, root, path, name, _id):
        self.root = root
        self.path = path
        self.name = name
        self._id = _id
    
    def __str__(self):
        return "%s/%s" %(self.path, self.name)
    
    def download(self):
        pass
    
    def upload(self):
        pass