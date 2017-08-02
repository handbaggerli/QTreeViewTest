# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\GitRepos\QTreeViewTest\GuiBuilder\QTreeViewTest\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from MyModel import MyModel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(323, 287)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.treeView = QtWidgets.QTreeView(self.centralWidget)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonPrint = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonPrint.setObjectName("pushButtonPrint")
        self.horizontalLayout.addWidget(self.pushButtonPrint)
        self.pushButtonReset = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonReset.setObjectName("pushButtonReset")
        self.horizontalLayout.addWidget(self.pushButtonReset)
        self.pushButtonLoad = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonLoad.setObjectName("pushButtonLoad")
        self.horizontalLayout.addWidget(self.pushButtonLoad)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 323, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Datenansicht Tree View mit Model"))
        self.pushButtonPrint.setText(_translate("MainWindow", "Print"))
        self.pushButtonReset.setText(_translate("MainWindow", "Reset"))
        self.pushButtonLoad.setText(_translate("MainWindow", "Load"))


    #
    # connect signals to slot
    #
    def connect_user_signals(self):
        self.pushButtonReset.clicked.connect(self.__reset)
        self.pushButtonLoad.clicked.connect(self.__load)
        self.pushButtonPrint.clicked.connect(self.__print)

    # Hier nur Dummy, Daten werden nicht ans Model uebergeben.
    def initData(self, display_data):
        self.display_data = display_data
        headers = ()
        self.data_model = MyModel(headers=headers, data=None, parent=None)
        self.treeView.setModel(self.data_model)


    # Print Selection Info to Status Bar
    def printSelection(self):
        has_selection = self.treeView.selectionModel().currentIndex().isValid()
        model = self.treeView.model()
        if has_selection:
            row = self.treeView.selectionModel().currentIndex().row()
            column = self.treeView.selectionModel().currentIndex().column()
            data1 = self.treeView.selectionModel().currentIndex().data() # Selektierter Datensatz ueber Tree View
            data2 = model.getItem(index=self.treeView.selectionModel().currentIndex()).data(column=column) # Selektierter Datensatz ueber Model
            if self.treeView.selectionModel().currentIndex().parent().isValid():
                parentIndex = self.treeView.selectionModel().currentIndex().parent()
                rowData = model.getItem(index=parentIndex).data(column=0) # Typ ist auf Position 0

                self.statusBar.showMessage("Position: {row}, {column} von Typ {type}".format(row=row, column=column, type=rowData))
            else:
                self.statusBar.showMessage("Position: {row}, {column} Top Level".format(row=row, column=column))


    def __reset(self):
        headers = ("Object", "Description")
        self.data_model = MyModel(headers=headers, data=self.display_data, parent=None)
        self.treeView.setModel(self.data_model)
        for column in range(self.data_model .columnCount()):
            self.treeView.resizeColumnToContents(column)
        self.treeView.selectionModel().selectionChanged.connect(self.printSelection) # Muss hier connected werden, da Model geaendert wurde


    def __load(self):
        headers = ("Object", "Description")
        self.data_model = MyModel(headers=headers, data=self.display_data, parent=None)
        self.treeView.setModel(self.data_model)
        for column in range(self.data_model .columnCount()):
            self.treeView.resizeColumnToContents(column)
        self.treeView.selectionModel().selectionChanged.connect(self.printSelection) # Muss hier connected werden, da Model geaendert wurde


    def __print(self):
        model = self.treeView.model()
        rows = model.rowCount()
        for row in range(rows):
            curr_index = model.index(row=row, column=0)
            current_item = model.getItem(index=curr_index)
            # Prints Top Level
            for col in range(current_item.columnCount()):
                print(current_item.data(column=col), end=' ')
            print('')

            for child in range(current_item.childCount()):
                self.__printChild(child_item=current_item.child(row=child))


    def __printChild(self, child_item):
        for col in range(child_item.columnCount()):
            print(child_item.data(column=col), end=' ')
        print('')




