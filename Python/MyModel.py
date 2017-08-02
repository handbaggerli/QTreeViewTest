# -*- coding: utf-8 -*-


##
## Implement the Abstract Table Model
##
##

from PyQt5 import QtCore, QtGui
from MyTreeItem import MyTreeItem


class MyModel(QtCore.QAbstractItemModel):
    def __init__(self, headers, data, parent=None):
        super(MyModel, self).__init__(parent=parent)

        rootData = [header for header in headers]
        self.rootItem = MyTreeItem(rootData)  # Root Item beinhaltet den Header

        if data is None:
            return

        # Umwandeln des Datenobjekts in ein Tree Item Objekt.
        # Aktuell gibt es nur 2 Levels, Prinzip ist aber immer das Gleiche.
        for type, name, objects in data.data:
            # 1. Hirarchie ist Child of Root Item !
            self.rootItem.insertChildren(position=self.rootItem.childCount(), count=1, columns=2)
            self.rootItem.child(row=self.rootItem.childCount() - 1).setData(column=0, value=type)
            self.rootItem.child(row=self.rootItem.childCount() - 1).setData(column=1, value=name)
            for object_name, object_path in objects:
                # 2. Hirarchie, parent ist Pointer auf aktuelles Objekt, danach muss Child inserted werden
                parent = self.rootItem.child(row=self.rootItem.childCount() - 1)
                parent.insertChildren(position=parent.childCount(), count=1, columns=2)
                parent.child(row=parent.childCount() - 1).setData(column=0, value=object_name)
                parent.child(row=parent.childCount() - 1).setData(column=1, value=object_path)


    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.rootItem.columnCount()


    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None

        item = self.getItem(index)
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return 0

        return QtCore.Qt.ItemIsEditable | super(MyModel, self).flags(index)

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QtCore.QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QtCore.QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result