#importing required libraries
import sys
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

#creating main window class
class MainWindow(QMainWindow):

    #initialzing
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()

        #Setting up ICON
        self.setWindowIcon(QtGui.QIcon('aurora_ico.ico'))
        # set the title
        self.setWindowTitle("Aurora Browser")

        # setting  the geometry of window
        self.setGeometry(10, 10, 400, 300)

        # creating a label widget
        self.label = QLabel("Icon is set", self)

        # moving position
        self.label.move(100, 100)

        # setting up border
        self.label.setStyleSheet("border: 1px solid black;")

        # setting default browser new page url to google
        self.browser.setUrl(QUrl('https://google.com'))
        self.setCentralWidget(self.browser)

        #show Minimized on default
        self.showMaximized()

        # creating navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        #creating back button
        back_btn = QAction('◀️	', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        #creating forward button
        forward_btn = QAction('▶️', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        #creating reload button
        reload_btn = QAction('🔃', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        #creating home button
        home_btn = QAction('🏠', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

    #setting up new tab/home page
    def navigate_home(self):
        self.browser.setUrl(QUrl('https://google.com'))

    # navigating browser to re-direct to url
    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())


app = QApplication(sys.argv)
QApplication.setApplicationName('Aurora Browser')
window = MainWindow()
app.exec_()