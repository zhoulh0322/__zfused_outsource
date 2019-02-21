# coding:utf-8
# --author-- lanhua.zhou

from qtpy import QtGui

class Pixmap(QtGui.QPixmap):
    def __init__(self, *args):
        QtGui.QPixmap.__init__(self, *args)
        
        self._color = None