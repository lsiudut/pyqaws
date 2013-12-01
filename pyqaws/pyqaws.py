#!/usr/bin/env python2.7

import sys
from boto import boto, ec2
import ConfigParser
import threading
import time

from PyQt4 import QtGui, QtCore
from mainwindow import Ui_MainWindow
from instancemanager import InstanceManager
from qthelpers import AMITableWidgetItem
from genericthread import GenericThread

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class ConnectThread(threading.Thread):
    def __init__(self, connection, account_name, account_config):
        super(ConnectThread, self).__init__()
        self.connection = connection
        self.account_name = account_name
        self.account_config = account_config

    def run(self):
        connection = boto.ec2.connect_to_region(self.account_config['region'], aws_access_key_id = self.account_config['aws_aki'], aws_secret_access_key = self.account_config['aws_sak'])
        self.connection[self.account_name] = connection
        
class InstanceDetailsDialog(QtGui.QDialog):
    def __init__(self, parent, instance_manager):
        super(InstanceDetailsDialog, self).__init__(parent)

        centralLayout = QtGui.QVBoxLayout()

        for attr in instance_manager.getAttributes():
            hlay = QtGui.QHBoxLayout()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            labelDesc = QtGui.QLabel(attr)
            labelDesc.setFont(font)

            if instance_manager.isEditable(attr):
                valueWidget = QtGui.QLineEdit()
                valueWidget.setText(str(instance_manager.get(attr)))
                valueWidget.setReadOnly(True)
            else:
                valueWidget = QtGui.QLabel(str(instance_manager.get(attr)))
                valueWidget.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextEditable|QtCore.Qt.TextSelectableByMouse)

            hlay.addWidget(labelDesc)
            hlay.addItem(QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
            hlay.addWidget(valueWidget)

            centralLayout.addLayout(hlay)

        centralLayout.addItem(QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
        self.setLayout(centralLayout)
        self.setGeometry(300, 300, 650, 300)
        self.setWindowTitle('Instance Details')
        self.show()

class Main(QtGui.QMainWindow, Ui_MainWindow):
    configAccountTabFields = [
                                ("name", "Name"),
                                ("architecture", "Arch"),
                                ("id", "ID"),
                                ("public_dns_name", "Public Address"),
                                ("instance_type", "Instance Type"),
                                ("state", "State"),
                                ("groups", "Sec Groups"),
                                ("launch_time", "Starttime"),
                                ("placement", "Placement"),
                            ]

    accounts = {}
    connections = {}
    accountTables = {}

    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        app = QtGui.QApplication(sys.argv)
        QtGui.QMainWindow.__init__(self, parent, f)

        self.tray = QtGui.QSystemTrayIcon(QtGui.QIcon("icons/aws.png"), app)
        QtCore.QObject.connect(self.tray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.signalTrayClicked)

        self.setupUi(self)
       
        self.show()

        self.initCustom()
        self.loadConfig()
        
        self.initializeConnections()
        self.initializeAccountsUI()

        self.tray.show()

        sys.exit(app.exec_())
        
    def initCustom(self):
        pass

    def addConnectionTab(self, name):
        tab = QtGui.QWidget()
        
        tabTableLayout = QtGui.QHBoxLayout(tab)

        font = QtGui.QFont()
        font.setPointSize(8)

        tableWidget = QtGui.QTableWidget(tab)
        tableWidget.setFont(font)
        tableWidget.setObjectName("tableWidget%s" % name)
        tableWidget.setColumnCount(len(self.configAccountTabFields))
        tableWidget.setRowCount(0)
        tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        tableWidget.setSortingEnabled(True)
        tableWidget.setAlternatingRowColors(True)
        tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        tableWidget.horizontalHeader().setDefaultSectionSize(200)
        tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

#        QtCore.QObject.connect(tableWidget, QtCore.SIGNAL(_fromUtf8("cellDoubleClicked(int,int)")), self.signalCellDoubleClicked)
        QtCore.QObject.connect(tableWidget, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QTableWidgetItem*)")), self.signalDetailsClicked)
        QtCore.QObject.connect(tableWidget, QtCore.SIGNAL(_fromUtf8("customContextMenuRequested(const QPoint&)")), self.customContextMenu)

        for i in xrange(0, len(self.configAccountTabFields)):
            item = QtGui.QTableWidgetItem()
            item.setText(self.configAccountTabFields[i][1])
            tableWidget.setHorizontalHeaderItem(i, item)

        tabTableLayout.addWidget(tableWidget)

        self.tabAccounts.addTab(tab, name)

        self.accountTables[name] = tableWidget

        return tableWidget

    def loadConfig(self):
    	config = ConfigParser.ConfigParser()
        config.read(['config.cfg'])

        for section in config.sections():
            accounts = {}
            accounts['aws_aki'] = config.get(section, 'aws_aki')
            accounts['aws_sak'] = config.get(section, 'aws_sak')
            accounts['region'] = config.get(section, 'region')
            self.accounts[ section ] = accounts

    def initializeConnections(self):
        threads = []
        for (account_name, account_config) in self.accounts.items():
            t = ConnectThread(self.connections, account_name, account_config)
            t.start()
            threads.append(t)

        [ t.join() for t in threads ]
        
        for (account, connection) in self.connections.items():
            tab = self.addConnectionTab(account)

    def initializeAccountsUI(self):
        self.connection_threads  = []
        for (account, connection) in self.connections.items():
            self.connection_threads.append( GenericThread(self.getInstances, connection, self.accountTables[account]) )

        self.connect(self, QtCore.SIGNAL('setTabIcon(PyQt_PyObject)'), self.setTabIcon)
        self.connect(self, QtCore.SIGNAL('addInstance(PyQt_PyObject)'), self.addInstance)
        self.connect(self, QtCore.SIGNAL('deleteInstance(PyQt_PyObject)'), self.deleteInstance)
        self.connect(self, QtCore.SIGNAL('updateInstance(PyQt_PyObject)'), self.updateInstance)
        
        for thread in self.connection_threads:
            thread.start()

    def addInstance(self, data):
        tab = data[0]
        instance = data[1]
        tabCount = tab.rowCount()

        tab.setRowCount(tabCount+1)
        for i in xrange(0, len(self.configAccountTabFields)):
            instance_manager = InstanceManager(instance, ro = True)
            item = AMITableWidgetItem(instance_manager)
            item.setText(instance_manager.get(self.configAccountTabFields[i][0]))
            tab.setItem(tabCount, i, item)

        tab.resizeColumnsToContents()

    def deleteInstance(self, data):
        pass

    def updateInstance(self, data):
        pass

    def setTabIcon(self, data):
        table = data[0]
        icon = data[1]

        page_index = self.tabAccounts.indexOf(table.parent())
        self.tabAccounts.setTabIcon(page_index, QtGui.QIcon("icons/" + icon))

    """
        This function is ment to run as thread. It's responsible for fetching instances, track changes
        and updating table in UI.
    """
    def getInstances(self, connection, table):
        instances = []

        while True:
            self.emit(QtCore.SIGNAL('setTabIcon(PyQt_PyObject)'), [table, "busy.png"])
            reservations = connection.get_all_instances()

            for reservation in reservations:
                for instance in reservation.instances:
                    if instance.id in instances:
                        pass
                    else:
                        # this is little hacky, but there will be time (hue hue hue) for cleanups
                        instances.append(instance.id)
                        self.emit(QtCore.SIGNAL('addInstance(PyQt_PyObject)'), [ table, instance ])
            
            self.emit(QtCore.SIGNAL('setTabIcon(PyQt_PyObject)'), [table, "ok.png"])
            time.sleep(30)
        

    def searchInstance(self, search_string):
        for table in self.accountTables.values():
            finding = table.findItems(search_string, QtCore.Qt.MatchContains)
            
            if finding:
                widget = finding[0]
                page_index = self.tabAccounts.indexOf(widget.tableWidget().parentWidget())

                if page_index > -1:
                    self.tabAccounts.setCurrentIndex(page_index)
                    table.setCurrentItem(widget)
                    return

    def getActionWithMapper(self, name, slot, widget):
        mapper = QtCore.QSignalMapper(self)
        action = QtGui.QAction(QtGui.QIcon(), name, self)
        mapper.setMapping(action, widget)
        action.triggered.connect(mapper.map)
        mapper.mapped['QWidget*'].connect(slot)

        return action

    def customContextMenu(self, pos):
        related_widget = self.sender()
        related_instance = related_widget.currentItem().getRelatedInstance()
        custom_menu = QtGui.QMenu()

        instance_state = related_instance.get("state")

        action_copy = self.getActionWithMapper('&Copy', self.signalCopyClicked, related_widget)
        action_details = self.getActionWithMapper('&Details', self.signalDetailsClicked, related_widget)
        action_start_instance = self.getActionWithMapper('Start Instance', self.signalStartInstance, related_widget)
        action_stop_instance = self.getActionWithMapper('Stop Instance', self.signalStopInstance, related_widget)

        if instance_state == 'running':
            action_start_instance.setDisabled(True)
        else:
            action_stop_instance.setDisabled(True)
        
        custom_menu.addAction(action_copy)
        custom_menu.addSeparator()
        custom_menu.addAction(action_details)
        custom_menu.addAction(action_start_instance)
        custom_menu.addAction(action_stop_instance)

        custom_menu.exec_(QtGui.QCursor.pos())

    def signalDetailsClicked(self, sender):
        if type(sender) == AMITableWidgetItem:
            instance = sender.getRelatedInstance()
        else:
            instance = sender.currentItem().getRelatedInstance()

        InstanceDetailsDialog(self, instance)

    def signalCopyClicked(self, sender):
        value_to_copy = sender.currentItem().text()

        clipboard = QtGui.QApplication.clipboard()
        clipboard.setText(value_to_copy)

    def signalStartInstance(self, sender):
        print 'Starting %s' % sender.currentItem().getRelatedInstance().get("id")
        pass

    def signalStopInstance(self, sender):
        print 'Stopping %s' % sender.currentItem().getRelatedInstance().get("id")
        pass

    def signalTrayClicked(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.show() if self.isHidden() else self.hide()

main = Main()
