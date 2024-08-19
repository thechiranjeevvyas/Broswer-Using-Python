import sys
import os  #importing this library for inserting tabs
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import * #importing this library for placing icons
from PyQt5.QtPrintSupport import *  #importing this library for inserting tabs
from PyQt5 import QtGui #importing this library for setting up icon

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs): #here args and kwargs are added for tabs
        super(MainWindow, self).__init__(*args, **kwargs)
        self.browser = QWebEngineView()

        ######### Setting up ICON ##########
        self.setWindowIcon(QtGui.QIcon('aurora_ico.ico'))
        # set the title
        self.setWindowTitle("Aurora Browser")

        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)

        # creating a label widget
        self.label = QLabel("Icon is set", self)

        # moving position
        self.label.move(100, 100)

        # setting up border
        self.label.setStyleSheet("border: 1px solid black;")

        self.show()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        #First we will create tabs
        #Followed by Navbar
        #Followed by adding new tab
        #Followed by giving command of double click
        #Followed by closing tab
        #Followed by updating url

        
        #######Tabs########
        # creating a tab widget 
        self.tabs = QTabWidget()

		# making document mode true
        self.tabs.setDocumentMode(True)

		# adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

		# adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)

		# making tabs closeable
        self.tabs.setTabsClosable(True)

		# adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

		# making tabs as central widget
        self.setCentralWidget(self.tabs)

		# creating a status bar
        self.status = QStatusBar()

		# setting status bar to the main window
        self.setStatusBar(self.status)

        # creating a line edit widget for URL
        self.urlbar = QLineEdit()

		# adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        
        # creating first tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        
        
        
        ########### navbar ############
        navbar = QToolBar()
        self.addToolBar(navbar)
        navbar.setIconSize(QSize(1,1))

        back_btn = QAction('◀️', self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())  #changed to lambda
        navbar.addAction(back_btn)

        forward_btn = QAction('▶️', self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward()) #changed to lambda
        navbar.addAction(forward_btn)

        reload_btn = QAction('🔃', self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload()) # changed to lambda
        navbar.addAction(reload_btn)

        home_btn = QAction('🏠', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)


		# creating a line edit widget for URL
		# adding a separator
        navbar.addSeparator()

        self.urlbar = QLineEdit()

		# adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

		# adding line edit to tool bar
        navbar.addWidget(self.urlbar)
        
        # similarly adding stop action
        stop_btn = QAction('❌', self)
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navbar.addAction(stop_btn)

        # showing all the components
        self.show()

		# setting window title
        self.setWindowTitle("Aurora Browser")


    def navigate_home(self):
        return

    def navigate_to_url(self):
        return

    def update_url(self, q):
        return

	
    
    
    ######### method for adding new tab###########
    def add_new_tab(self, qurl = None, label ="Blank"):

		# if url is blank
        if qurl is None:
			# creating a google url
            qurl = QUrl('http://www.google.com')

		# creating a QWebEngineView object
        browser = QWebEngineView()

		# setting url to browser
        browser.setUrl(qurl)

		# setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

		# adding action to the browser when url is changed
		# update the url
        browser.urlChanged.connect(lambda qurl, browser = browser:
								self.update_urlbar(qurl, browser))

		# adding action to the browser when loading is finished
		# set the tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.tabs.setTabText(i, browser.page().title()))

	# when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):

		# checking index i.e
		# No tab under the click
        if i == -1:
			# creating a new tab
            self.add_new_tab()

	# when tab is changed
    def current_tab_changed(self, i):

		# get the curl
        qurl = self.tabs.currentWidget().url()

		# update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())

		# update the title
        self.update_title(self.tabs.currentWidget())

	# when tab is closed
    def close_current_tab(self, i):

		# if there is only one tab
        if self.tabs.count() < 2:
			# do nothing
            return

		# else remove the tab
        self.tabs.removeTab(i)

	########method for updating the title
    def update_title(self, browser):

		# if signal is not from the current tab
        if browser != self.tabs.currentWidget():
			# do nothing
            return

		# get the page title
        title = self.tabs.currentWidget().page().title()

        # set the window title 
        self.setWindowTitle("% s - Aurora Browser" % title)


	# action to go to home
    def navigate_home(self):

		# go to google
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

	######### method for navigate to url#############
    def navigate_to_url(self):

		# get the line edit text
		# convert it to QUrl object
        q = QUrl(self.urlbar.text())

		# if scheme is blank
        if q.scheme() == "":
			# set scheme
            q.setScheme("http")

		# set the url
        self.tabs.currentWidget().setUrl(q)

	# method to update the url
    def update_urlbar(self, q, browser = None):

		# If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
            return

		# set text to the url bar
        self.urlbar.setText(q.toString())

		# set cursor position
        self.urlbar.setCursorPosition(0)

    
app = QApplication(sys.argv)
QApplication.setApplicationName('Aurora Browser')
window = MainWindow()
app.exec_()