# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Wed Feb  5 17:53:24 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_frmAbout(object):
    def setupUi(self, frmAbout):
        frmAbout.setObjectName(_fromUtf8("frmAbout"))
        frmAbout.resize(608, 325)
        self.verticalLayout = QtGui.QVBoxLayout(frmAbout)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(frmAbout)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lblVersion = QtGui.QLabel(frmAbout)
        self.lblVersion.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblVersion.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblVersion.setObjectName(_fromUtf8("lblVersion"))
        self.horizontalLayout.addWidget(self.lblVersion)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(frmAbout)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.label_2 = QtGui.QLabel(frmAbout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_7 = QtGui.QLabel(frmAbout)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_8 = QtGui.QLabel(frmAbout)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_2.addWidget(self.label_8)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.label_3 = QtGui.QLabel(frmAbout)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(frmAbout)
        self.label_4.setOpenExternalLinks(False)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.label_5 = QtGui.QLabel(frmAbout)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtGui.QLabel(frmAbout)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_2.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(frmAbout)
        QtCore.QMetaObject.connectSlotsByName(frmAbout)

    def retranslateUi(self, frmAbout):
        frmAbout.setWindowTitle(_translate("frmAbout", "Openbox menu editor - About", None))
        self.label.setText(_translate("frmAbout", "Openbox menu editor", None))
        self.lblVersion.setText(_translate("frmAbout", "Program version: ", None))
        self.label_2.setText(_translate("frmAbout", "Simple menu editor for openbox desktop manager.", None))
        self.label_7.setText(_translate("frmAbout", "Author", None))
        self.label_8.setText(_translate("frmAbout", "<html><head/><body><p>Nicolás Daniel Palumbo &lt;<a href=\"mailto=n@xinax.net\"><span style=\" text-decoration: underline; color:#0000ff;\">n@xinax.net</span></a><a href=\"mailto=n@xinax.net\"><span style=\" color:#000000;\">&gt;</span></a></p></body></html>", None))
        self.label_3.setText(_translate("frmAbout", "Contributing", None))
        self.label_4.setText(_translate("frmAbout", "<html><head/><body><p>You can find the application source code, documentation<br> and report errors/bugs on the github project website:<br><a href=\"https://github.com/shaggyz/obmenu-qt\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/shaggyz/obmenu-qt</span></a></p></body></html>", None))
        self.label_5.setText(_translate("frmAbout", "License", None))
        self.label_6.setText(_translate("frmAbout", "<html><head/><body><p>This program was released under the General Public License 2, (C) 2014<br>A full copy of license is in the file COPYING delivered with this application. <br>Also a online version of this file can be found <a href=\"https://raw.github.com/shaggyz/obmenu-qt/master/COPYING\"><span style=\" text-decoration: underline; color:#0000ff;\">here</span></a></p></body></html>", None))
