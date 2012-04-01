# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30

from http import send

def rm_url(version="1"):
    return "http://openapi.kuaipan.cn/%s/fileops/delete " % version

def mv_url(version="1"):
    return "http://openapi.kuaipan.cn/%s/fileops/move" % version

def cp_url(version="1"):
    return "http://openapi.kuaipan.cn/%s/fileops/copy" % version

class kfile:
    def __init__(self, path="", name="", _id="", root="kuaipan"):
        self.root = root
        self.path = path
        self.name = name
        self._id = _id
    
    def __str__(self):
        return "%s/%s" %(self.path, self.name)
    
    def mv(self, _to_path):
        if len(_to_path) > 255: raise Exception("To path too long.")
        params = dict(
                      root=self.root,
                      from_path=self.path,
                      to_path=_to_path,
                      )
        mv_data = send(mv_url(), params)
        if mv_data:
            self.path = _to_path
    
    def cp(self, _to_path):
        if len(_to_path) > 255: raise Exception("To path too long.")
        params = dict(
                      root=self.root,
                      from_path=self.path,
                      to_path=_to_path,
                      )
        send(cp_url(), params)
        
    def rm(self, to_recycle=True):
        if not self.path:
            raise Exception("Remove root is not allowed/too dangerous, please goto kuaipan.cn and do it there.")
        params = dict(
                      root=self.root,
                      path=self.path,
                      )
        if not to_recycle:
            params["to_recycle"] = "False"
        send(rm_url(), params)
    
    def download(self):
        pass
    
    def upload(self):
        pass