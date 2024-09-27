from silx.gui import qt as Qt

from .Node import Node
from .ModelDef import ModelColumns, ModelRoles


class RootNode(Node):
    ColumnNames = ModelColumns.ColumnNames

    def __init__(self, *args, **kwargs):
        super(RootNode, self).__init__(*args, **kwargs)
        for index, name in enumerate(self.ColumnNames):
            self._setDataInternal(index, name, Qt.Qt.DisplayRole)


class Model(Qt.QAbstractItemModel):
    ColumnsWithDelegates = [0, 1]
    ModelRoles = ModelRoles
    ModelColumns = ModelColumns

    RootNode = RootNode

    sigRowsRemoved = Qt.Signal(object, int, int)

    def __init__(self, parent=None, **kwargs):
        super(Model, self).__init__(parent)
        self.__root = self.RootNode(nodeName="__root__", model=self, **kwargs)
        self.__root.sigInternalDataChanged.connect(self.__internalDataChanged)

    def columnsWithDelegates(self):
        if self.ColumnsWithDelegates is None:
            return []
        return self.ColumnsWithDelegates

    def startModel(self):
        self.__root.start()

    def stopModel(self):
        self.__root.stop()

    def appendGroup(self, group, groupName=None):
        if groupName is not None:
            group.nodeName = groupName
        self.beginInsertRows(Qt.QModelIndex(), self.rowCount(), self.rowCount())
        self.__root.appendChild(group)
        self.endInsertRows()

    def _beginRowAdded(self, index, start, end):
        self.beginInsertRows(index, start, end)

    def _endRowAdded(self):
        self.endInsertRows()

    def removeRow(self, row, parent=Qt.QModelIndex()):
        if not parent.isValid():
            node = self.__root
        else:
            node = parent.data(ModelRoles.InternalDataRole)

        if not node:
            return False

        child = node.child(row)
        if not child:
            return False

        self.beginRemoveRows(parent, row, row)
        node._removeChild(child)
        self.endRemoveRows()
        self.sigRowsRemoved.emit(parent, row, row)

        return True

    def __internalDataChanged(self, indices):
        modelIndex = Qt.QModelIndex()
        for index in reversed(indices[1:]):
            modelIndex = self.index(index, indices[0], modelIndex)
        self.dataChanged.emit(modelIndex, modelIndex)

    def parent(self, index):
        if not index.isValid():
            return Qt.QModelIndex()
        node = index.data(ModelRoles.InternalDataRole)

        if node is None:
            return Qt.QModelIndex()

        if node == self.__root:
            return Qt.QModelIndex()

        parent = node.parent()

        # Dirty (?) hack
        # Sometimes when removing rows the view gets kinda lost,
        # and asks for indices that have been removed.
        # closing all editors before removing a row fixed one problem.
        # but there is still an issue if the removed row was selected.
        # This seems to fix it... maybe
        if parent is None:
            return Qt.QModelIndex()

        if parent == self.__root:
            return Qt.QModelIndex()

        row = parent.row()
        if row < 0:
            return Qt.QModelIndex()
        return self.createIndex(row, 0, parent)

    def flags(self, index):
        if not index.isValid():
            return Qt.Qt.NoItemFlags

        node = index.data(ModelRoles.InternalDataRole)
        return node.flags(index.column())

    def columnCount(self, parent=Qt.QModelIndex(), **kwargs):
        return len(self.RootNode.ColumnNames)

    def headerData(self, section, orientation, role=Qt.Qt.DisplayRole):
        if role == Qt.Qt.DisplayRole and orientation == Qt.Qt.Horizontal:
            return self.__root.data(section, role=Qt.Qt.DisplayRole)
        return None

    def data(self, index, role=Qt.Qt.DisplayRole, **kwargs):
        if not index.isValid():
            raise ValueError("Invalid index.")

        node = index.internalPointer()

        data = node.data(index.column(), role)
        return data

    def index(self, row, column, parent=Qt.QModelIndex(), **kwargs):
        if not self.hasIndex(row, column, parent):
            return Qt.QModelIndex()
        if not parent.isValid():
            node = self.__root
        else:
            node = parent.data(ModelRoles.InternalDataRole)
        child = node.child(row)

        if child is not None:
            return self.createIndex(row, column, child)
        return Qt.QModelIndex()

    def refresh(self):
        self.__root.refresh()

    def reset(self):
        self.beginResetModel()
        children = [self.__root.child(row) for row in range(self.__root.childCount())]
        self.__root.clear()
        self.endResetModel()

        for child in children:
            child.clear()
            self.__root.appendChild(child)

    def rowCount(self, parent=Qt.QModelIndex(), **kwargs):
        if not parent.isValid():
            node = self.__root
        else:
            node = parent.data(ModelRoles.InternalDataRole)
        if node is not None:
            return node.childCount()
        return 0

    def setData(self, index, value, role=Qt.Qt.EditRole):
        if not index.isValid():
            return False
        node = index.data(role=ModelRoles.InternalDataRole)
        rc = node.setData(index.column(), value, role)
        return rc
