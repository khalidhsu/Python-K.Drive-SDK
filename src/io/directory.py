# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30

from http import send
from file import kfile

class kfolder:
    def __init__(self, path="", name="", _id="", root="kuaipan", page=0, page_size=20, sort_by="date", filter_ext=""):
        self.root = root
        self.path = path
        self.name = name
        self._id = _id
        self.page = page
        self.page_size = page_size
        self.sort_by = sort_by
        self.filter_ext = filter_ext
    
    def fullpath(self):
        return "%s/%s" %(self.path, self.name)
    
    def __str__(self):
        return "+ %s/%s" % (self.path, self.name)
    
    def rmdir(self, to_recycle=True):
        if not self.path:
            raise Exception("Remove root is not allowed/too dangerous, please goto kuaipan.cn and do it there.")
        params = dict(
                      root=self.root,
                      path=self.path,
                      )
        if not to_recycle:
            params["to_recycle"] = "False"
        del_data = send(rm_url(), params)
        msg = del_data["msg"]
        if "ok" != msg:
            raise Exception(msg)
    
    def create(self, _path):
        new_path = self.check_path(_path)        
        params = dict(
                      root=self.root,
                      path=new_path
                      )
        new_folder_data = send(mkdir_url(), params)
        msg = new_folder_data["msg"]
        if "ok" != msg:
            raise Exception(msg)
        
        _id = new_folder_data["file_id"]        
        return kfolder(new_path, _path, _id, self.root)
    
    def ls(self):
        params = dict(
                      page=str(self.page), 
                      page_size=str(self.page_size),
#                      filter_ext=self.filter_ext, sort_by=self.sort_by
#                       sort_by=sort_by
                       )
        ls_data = send(ls_url(root=self.root, path=self.path), params)
        files, folders = [], []
        for _file in ls_data["files"]:
            _name = _file['name']
            _is_deleted = _file['is_deleted']
            _id = _file['file_id']
            
            if not _is_deleted:
                if _file["type"] == "folder":
                    _folder = kfolder(self.path, _name, _id, self.root, )
                    folders.append(_folder)
                elif _file["type"] == "file":
                    files.append(kfile(self.root, self.path, _name, _id))
        
        return folders, files
    
    def check_path(self, _path): # Check if can add new path
        if "/" in _path: raise Exception("Slash is not allowed as folder name.")
        if self.path:
            new_path = "%s/%s" % (self.path, _path)
        else:
            new_path = _path
        if not _path or len(new_path) > 255: 
            raise Exception("Folder empty or too long.")
         
        return new_path
    
def ls_url(version="1", root="kuaipan", path=""):
    return "http://openapi.kuaipan.cn/%s/metadata/%s/%s" % (version, root, path)

def mkdir_url(version="1"):
    return "http://openapi.kuaipan.cn/%s/fileops/create_folder" % version

def rm_url(version="1"):
    return "http://openapi.kuaipan.cn/%s/fileops/delete " % version

if __name__ == "__main__":
#    home = kfolder("hahaha")
#    home.rmdir()

    home = kfolder()
#    home.create("hahaha")
    fos, fis = home.ls()#("books/java/网络编程")

    for f in fos: print f
    for f in fis: print f