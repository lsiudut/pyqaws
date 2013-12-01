#!/usr/bin/env python2.7

from PyQt4 import QtGui

class AMITableWidgetItem(QtGui.QTableWidgetItem):
    def __init__(self, related_instance = None):
        super(QtGui.QTableWidgetItem, self).__init__(1001)
        self.related_instance = related_instance

    def getRelatedInstance(self):
        return self.related_instance

