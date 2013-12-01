# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sun Feb 17 14:03:51 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1104, 560)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.searchEdit = QtGui.QLineEdit(self.centralWidget)
        self.searchEdit.setObjectName(_fromUtf8("searchEdit"))
        self.horizontalLayout.addWidget(self.searchEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tabAccounts = QtGui.QTabWidget(self.centralWidget)
        self.tabAccounts.setObjectName(_fromUtf8("tabAccounts"))
        self.verticalLayout.addWidget(self.tabAccounts)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBarTop = QtGui.QMenuBar(MainWindow)
        self.menuBarTop.setGeometry(QtCore.QRect(0, 0, 1104, 21))
        self.menuBarTop.setObjectName(_fromUtf8("menuBarTop"))
        self.menuMenu = QtGui.QMenu(self.menuBarTop)
        self.menuMenu.setObjectName(_fromUtf8("menuMenu"))
        MainWindow.setMenuBar(self.menuBarTop)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        MainWindow.insertToolBarBreak(self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionAdd_AWS_account = QtGui.QAction(MainWindow)
        self.actionAdd_AWS_account.setObjectName(_fromUtf8("actionAdd_AWS_account"))
        self.actionRemove_AWS_account = QtGui.QAction(MainWindow)
        self.actionRemove_AWS_account.setObjectName(_fromUtf8("actionRemove_AWS_account"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuMenu.addAction(self.actionExit)
        self.menuBarTop.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabAccounts.setCurrentIndex(-1)
        QtCore.QObject.connect(self.searchEdit, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), MainWindow.searchInstance)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Search:", None))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu", None))
        self.actionAdd_AWS_account.setText(_translate("MainWindow", "Add AWS account", None))
        self.actionRemove_AWS_account.setText(_translate("MainWindow", "Remove AWS account", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)

