# Form implementation generated from reading ui file 'loopwidget.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from pyqtgraph import QtCore, QtGui, QtWidgets


class Ui_LoopWidget(object):
    def setupUi(self, LoopWidget):
        LoopWidget.setObjectName("LoopWidget")
        LoopWidget.resize(763, 601)
        self.horizontalLayout = QtWidgets.QHBoxLayout(LoopWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = PlotWidget(parent=LoopWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lblDelay = QtWidgets.QLabel(parent=LoopWidget)
        self.lblDelay.setText("")
        self.lblDelay.setObjectName("lblDelay")
        self.gridLayout.addWidget(self.lblDelay, 5, 1, 1, 1)
        self.btnPrev = QtWidgets.QPushButton(parent=LoopWidget)
        self.btnPrev.setObjectName("btnPrev")
        self.gridLayout.addWidget(self.btnPrev, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=LoopWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=LoopWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lblGala = QtWidgets.QLabel(parent=LoopWidget)
        self.lblGala.setText("")
        self.lblGala.setObjectName("lblGala")
        self.gridLayout.addWidget(self.lblGala, 8, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=LoopWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.lblIdx = QtWidgets.QLabel(parent=LoopWidget)
        self.lblIdx.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblIdx.setObjectName("lblIdx")
        self.gridLayout.addWidget(self.lblIdx, 3, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=LoopWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=LoopWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 7, 0, 1, 1)
        self.lblBeta = QtWidgets.QLabel(parent=LoopWidget)
        self.lblBeta.setText("")
        self.lblBeta.setObjectName("lblBeta")
        self.gridLayout.addWidget(self.lblBeta, 7, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=LoopWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        self.btnNext = QtWidgets.QPushButton(parent=LoopWidget)
        self.btnNext.setObjectName("btnNext")
        self.gridLayout.addWidget(self.btnNext, 1, 1, 1, 1)
        self.lblAlpha = QtWidgets.QLabel(parent=LoopWidget)
        self.lblAlpha.setText("")
        self.lblAlpha.setObjectName("lblAlpha")
        self.gridLayout.addWidget(self.lblAlpha, 6, 1, 1, 1)
        self.lblTot = QtWidgets.QLabel(parent=LoopWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTot.sizePolicy().hasHeightForWidth())
        self.lblTot.setSizePolicy(sizePolicy)
        self.lblTot.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblTot.setObjectName("lblTot")
        self.gridLayout.addWidget(self.lblTot, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.comboSeries = QtWidgets.QComboBox(parent=LoopWidget)
        self.comboSeries.setObjectName("comboSeries")
        self.verticalLayout_2.addWidget(self.comboSeries)
        self.btnDelete = QtWidgets.QPushButton(parent=LoopWidget)
        self.btnDelete.setObjectName("btnDelete")
        self.verticalLayout_2.addWidget(self.btnDelete)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(LoopWidget)
        QtCore.QMetaObject.connectSlotsByName(LoopWidget)

    def retranslateUi(self, LoopWidget):
        _translate = QtCore.QCoreApplication.translate
        LoopWidget.setWindowTitle(_translate("LoopWidget", "Form"))
        self.btnPrev.setText(_translate("LoopWidget", "<"))
        self.label_2.setText(_translate("LoopWidget", "of"))
        self.label.setText(_translate("LoopWidget", "Loop #"))
        self.label_4.setText(_translate("LoopWidget", "Delay (ms)"))
        self.lblIdx.setText(_translate("LoopWidget", "0"))
        self.label_3.setText(_translate("LoopWidget", "α"))
        self.label_5.setText(_translate("LoopWidget", "β"))
        self.label_7.setText(_translate("LoopWidget", "GALA"))
        self.btnNext.setText(_translate("LoopWidget", ">"))
        self.lblTot.setText(_translate("LoopWidget", "0"))
        self.btnDelete.setText(_translate("LoopWidget", "Delete current Loop"))
from pyqtgraph import PlotWidget
