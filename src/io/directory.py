# -*- coding: UTF-8 -*-
# Daoyu 2012/3/30

from http import send

class directory:
    def __init__(self, root, path, ):
        self.root = root
        self.path = path
    
def get_directory_url(version="1", root="kuaipan", path=""):
    return "http://openapi.kuaipan.cn/%s/metadata/%s/%s" % (version, root, path)
    
def ls(path, root="kuaipan", list="true", file_limit=20, page=0, page_size=20, filter_ext="", sort_by="date"):
    params = dict(#list=list,
#                   file_limit=str(file_limit),
                   page=str(page),
                   page_size=str(page_size),
#                   filter_ext=filter_ext,
#                   sort_by=sort_by
                   )
    ls_data = send(get_directory_url(root=root, path=path), params)
    print ls_data
    
if __name__ == "__main__":
    ls("books/java", filter_ext="7z,abc")