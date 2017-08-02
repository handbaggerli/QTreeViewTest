# -*- coding: utf-8 -*-

from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets
from MyData import MyData



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    data = MyData(no_tables=3, no_views=5)
    ui.initData(display_data=data)
    ui.connect_user_signals() # Signale erst am Schluss connection.

    MainWindow.show()
    sys.exit(app.exec_())

