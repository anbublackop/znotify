from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import urllib.request
from bs4 import BeautifulSoup
from torrent import Torrent, TorrentzEngine
from parser import MyParser

headers={"Name":0,"Age":1,"Size":2,"Seeders":3,"Peers":4,"Category":5,"Download":6,"Description":7}

header_data=("Name","Age","Size","Seeders","Peers","Category","Download","Description")




categories = ("Any","Anime","Application","Books","Games","Movies","Music","TV")

categories_keywords = { "Anime" : ("anime"),
                        "Application" : ("app","software"),
                        "Books" : ("book","comic"),
                        "Games" : ("game"),
                        "Movies" : ("movie",),
                        "Music" : ("music","audio"),
                        "TV" : ("tv","show")
                    }


class searchSortModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
    
    
    
class TorrentzSearch():

    def __init__(self):
        pass
        
    def search_now(self,query_Obj,pages=1):
        query = urllib.parse.quote(query_Obj.search_String)
        
        full_results = list()
        for page_no in range(pages):
            #"""
            full_url = TorrentzEngine.Feed_Url(query, page_no)
            
            req = urllib.request.Request(full_url,headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            
            """
            static=open("static.xml","r")
            page_xml_obj=BeautifulSoup(static.read(),"xml")
            #"""
            
            parsed_results = MyParser.Parse_Page(response)
            filtered_results = parsed_results
            
            full_results.extend(filtered_results)
            
        return full_results

    def filter_categories(self,results,categ):
        if categ == "Any" : 
            return results
        else:
            new_results = list()
            index=headers["Category"]
            for i in results : 
                cat=i[index]
                for keyword in categories_keywords[categ] : 
                    if keyword in cat :
                        new_results.append(i)
                        break
            return new_results
