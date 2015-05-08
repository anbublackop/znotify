#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from query import Query
import search
from subprocess import call
import torrent
page_no,call_count=1,0

form_class=loadUiType("mainwindow.ui")[0]

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #setting up search tab treeview 
        self.SearchListModel = QStandardItemModel(0,len(search.header_data))
        self.SearchListModel.setHorizontalHeaderLabels(search.header_data)
        
        self.proxyModel = search.searchSortModel(None)
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.SearchListModel)
        
        self.resultsBrowser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultsBrowser.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.resultsBrowser.setModel(self.proxyModel)
        self.resultsBrowser.setRootIsDecorated(False)
        self.resultsBrowser.setAllColumnsShowFocus(True)
        self.resultsBrowser.setSortingEnabled(True)
        self.resultsBrowser.setColumnWidth(search.headers["Name"],400)
        self.resultsBrowser.hideColumn(search.headers["Description"]) # Hide url column
        self.resultsBrowser.hideColumn(search.headers["Download"])
        #self.resultsBrowser.hideColumn(search.headers["Category"])

        self.combo_searchcateg.addItems(search.categories)
        self.btn_search.clicked.connect(self.init_Search)
        self.display_more.clicked.connect(self.moreResults)  
        self.search_bar.returnPressed.connect(self.init_Search)
        self.search_bar.setFocus()
        

    def reset_List(self):
        row = self.SearchListModel.rowCount()
        if row > 0:
            self.SearchListModel.removeRows(0, row)
        
    def init_Search(self):
        search_Text = self.search_bar.text()

        if search_Text :
            self.status_label.setText("Status: Searching... ")
            
            category = self.combo_searchcateg.currentText()
            query_Obj = Query(search_Text, category)
            
            self.reset_List()

            search_Obj = search.TorrentzSearch()
            results = search_Obj.search_now(query_Obj)
            self.showResults(results)
        else:
            pass      
    
    def showResults(self,list_of_results):
        if list_of_results:
            ln=len(list_of_results)
            for tor_Obj in range(ln//2):
                row=self.SearchListModel.rowCount()
                self.SearchListModel.insertRow(row)
                
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["Name"]), list_of_results[tor_Obj].title)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["Age"]), list_of_results[tor_Obj].pub_Date)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["Size"]), list_of_results[tor_Obj].size)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["Seeders"]), list_of_results[tor_Obj].seeds)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["Peers"]), list_of_results[tor_Obj].peers)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["Category"]), list_of_results[tor_Obj].categ)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["Download"]), list_of_results[tor_Obj].mag_Link)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["Description"]), list_of_results[tor_Obj].desc_Link)
            
            self.resultsBrowser.sortByColumn(search.headers["Seeders"], Qt.DescendingOrder)
            self.btn_description.setEnabled(True)
            self.btn_download.setEnabled(True)
            self.btn_download.clicked.connect(self.download)
            self.btn_description.clicked.connect(self.open_desc)
            self.display_more.setEnabled(True)
            status = "Status: {} Results Found. ".format(ln//2)
        else :
            status = "Status: No Results Found. Please Check if you correctly typed the query."
        
        self.status_label.setText(status)
            
    def download(self):
        indexes=self.resultsBrowser.selectedIndexes()
        for i in indexes:
            if(i.column() == search.headers["Name"]):
                print(i.row(),search.headers["Download"])
                link = self.proxyModel.data(self.proxyModel.index(i.row(), search.headers["Download"]))
                #print(link)
                call(["xdg-open",link])
    
    def open_desc(self):
        indexes=self.resultsBrowser.selectedIndexes()
        for i in indexes:
            if(i.column() == search.headers["Name"]):
                link = self.proxyModel.data(self.proxyModel.index(i.row(), search.headers["Description"]))
                QDesktopServices.openUrl(QUrl(link))
                #call(["xdg-open",link])

    def moreResults(self):
        global page_no,call_count
        page_no+=1
        call_count+=1
        search_Text = self.search_bar.text()
        category = self.combo_searchcateg.currentText()
        query_Obj = Query(search_Text, category)
        self.reset_List()        
        search_Obj = search.TorrentzSearch()
        results = search_Obj.search_now(query_Obj, page_no)
        self.showResults(results)


if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    sys.exit(app.exec_())
