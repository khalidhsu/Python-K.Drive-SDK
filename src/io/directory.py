# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30

from http import send
from file import kfile

class kfolder:
    def __init__(self, root, path, name, _id):
        self.root = root
        self.path = path
        self.name = name
        self._id = _id
    
    def fullpath(self):
        return "%s/%s" %(self.path, self.name)
    
    def __str__(self):
        return "+ %s/%s" % (self.path, self.name) 
    
def get_directory_url(version="1", root="kuaipan", path=""):
    return "http://openapi.kuaipan.cn/%s/metadata/%s/%s" % (version, root, path)
    
def ls(path, root="kuaipan", list="true", page=0, page_size=20, sort_by="date"):
    params = dict(#list=list,
                   page=str(page),
                   page_size=str(page_size),
#                   sort_by=sort_by
                   )
    ls_data = send(get_directory_url(root=root, path=path), params)
    files, folders = [], []
    for _file in ls_data["files"]:
        _name = _file['name']
        _is_deleted = _file['is_deleted']
        _id = _file['file_id']
        
        if _file["type"] == "folder":            
            folders.append(kfolder(root, path, _name, _id))
        elif _file["type"] == "file":
            files.append(kfile(root, path, _name, _id))
    
    return folders, files
    
if __name__ == "__main__":
    fos, fis = ls("books/java/Application Server")

#    fos, fis = ls(folders[0].fullpath())
    for f in fos: print f
    for f in fis: print f