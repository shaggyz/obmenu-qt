# Form implementation generated from reading ui file 'obmenu.ui'
#
# Created: Mon Feb 10 16:33:53 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError as e:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError as e:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_frmObmenu(object):
    def setupUi(self, frmObmenu):
        frmObmenu.setObjectName(_fromUtf8("frmObmenu"))
        frmObmenu.resize(640, 480)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(frmObmenu)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeMenu = QtWidgets.QTreeWidget(frmObmenu)
        self.treeMenu.setUniformRowHeights(True)
        self.treeMenu.setAnimated(False)
        self.treeMenu.setObjectName(_fromUtf8("treeMenu"))
        self.treeMenu.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.treeMenu)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblLabel = QtWidgets.QLabel(frmObmenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLabel.sizePolicy().hasHeightForWidth())
        self.lblLabel.setSizePolicy(sizePolicy)
        self.lblLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.lblLabel.setObjectName(_fromUtf8("lblLabel"))
        self.horizontalLayout.addWidget(self.lblLabel)
        self.txtLabel = QtWidgets.QLineEdit(frmObmenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtLabel.sizePolicy().hasHeightForWidth())
        self.txtLabel.setSizePolicy(sizePolicy)
        self.txtLabel.setObjectName(_fromUtf8("txtLabel"))
        self.horizontalLayout.addWidget(self.txtLabel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblId = QtWidgets.QLabel(frmObmenu)
        self.lblId.setMinimumSize(QtCore.QSize(50, 0))
        self.lblId.setObjectName(_fromUtf8("lblId"))
        self.horizontalLayout_2.addWidget(self.lblId)
        self.txtID = QtWidgets.QLineEdit(frmObmenu)
        self.txtID.setObjectName(_fromUtf8("txtID"))
        self.horizontalLayout_2.addWidget(self.txtID)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblAction = QtWidgets.QLabel(frmObmenu)
        self.lblAction.setMinimumSize(QtCore.QSize(50, 0))
        self.lblAction.setObjectName(_fromUtf8("lblAction"))
        self.horizontalLayout_3.addWidget(self.lblAction)
        self.cmbAction = QtWidgets.QComboBox(frmObmenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbAction.sizePolicy().hasHeightForWidth())
        self.cmbAction.setSizePolicy(sizePolicy)
        self.cmbAction.setObjectName(_fromUtf8("cmbAction"))
        self.horizontalLayout_3.addWidget(self.cmbAction)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lblExecute = QtWidgets.QLabel(frmObmenu)
        self.lblExecute.setMinimumSize(QtCore.QSize(50, 0))
        self.lblExecute.setObjectName(_fromUtf8("lblExecute"))
        self.horizontalLayout_4.addWidget(self.lblExecute)
        self.txtExecute = QtWidgets.QLineEdit(frmObmenu)
        self.txtExecute.setObjectName(_fromUtf8("txtExecute"))
        self.horizontalLayout_4.addWidget(self.txtExecute)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label = QtWidgets.QLabel(frmObmenu)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        self.txtIcon = QtWidgets.QLineEdit(frmObmenu)
        self.txtIcon.setObjectName(_fromUtf8("txtIcon"))
        self.horizontalLayout_5.addWidget(self.txtIcon)
        self.btnChangeIcon = QtWidgets.QPushButton(frmObmenu)
        self.btnChangeIcon.setObjectName(_fromUtf8("btnChangeIcon"))
        self.horizontalLayout_5.addWidget(self.btnChangeIcon)
        self.btnPrompt = QtWidgets.QPushButton(frmObmenu)
        self.btnPrompt.setObjectName(_fromUtf8("btnPrompt"))
        self.horizontalLayout_5.addWidget(self.btnPrompt)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.retranslateUi(frmObmenu)
        QtCore.QMetaObject.connectSlotsByName(frmObmenu)

    def retranslateUi(self, frmObmenu):
        frmObmenu.setWindowTitle(_translate("frmObmenu", "Openbox menu editor", None))
        self.lblLabel.setText(_translate("frmObmenu", "Label", None))
        self.lblId.setText(_translate("frmObmenu", "ID", None))
        self.lblAction.setText(_translate("frmObmenu", "Action", None))
        self.lblExecute.setText(_translate("frmObmenu", "Execute", None))
        self.label.setText(_translate("frmObmenu", "Icon      ", None))
        self.btnChangeIcon.setText(_translate("frmObmenu", "Change Icon", None))
        self.btnPrompt.setText(_translate("frmObmenu", "Prompt", None))

