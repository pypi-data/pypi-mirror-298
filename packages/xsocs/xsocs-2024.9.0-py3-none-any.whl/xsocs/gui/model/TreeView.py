from functools import partial

from silx.gui import qt as Qt

from .ModelDef import ModelRoles
from .NodeEditor import EditorMixin


class TreeView(Qt.QTreeView):
    def __init__(self, parent=None, model=None):
        super(TreeView, self).__init__(parent)

        self.__autoRefresh = False
        # WARNING : had to set this as a queued connection, otherwise
        # there was a crash after the slot was called (conflict with
        # __setHiddenNodes probably)
        # TODO : investigate
        self.expanded.connect(self.__expanded, Qt.Qt.QueuedConnection)
        self.collapsed.connect(self.__collapsed)

        self.header().setSectionResizeMode(Qt.QHeaderView.ResizeToContents)
        self.__showUniqueGroup = False
        self.__userRoot = False
        # self.setSelectionBehavior(Qt.QAbstractItemView.SelectRows)

        if model:
            self.setModel(model)

    showUniqueGroup = property(lambda self: self.__showUniqueGroup)

    def disableDelegateForColumn(self, column, disable):
        self.__openPersistentEditors(Qt.QModelIndex(), openEditor=False)
        if disable:
            self.setItemDelegateForColumn(column, None)
        else:
            self.setItemDelegateForColumn(column, ItemDelegate(self))
        self.__openPersistentEditors(Qt.QModelIndex(), openEditor=True)

    def __delegateEvent(self, column, node, args, kwargs):
        self.delegateEvent(column, node, *args, **kwargs)

    def delegateEvent(self, column, node, *args, **kwargs):
        # TODO : proper class event
        pass

    def drawDelayedItems(self):
        """
        Forces the drawing of delayed items,
        even if the tree refresh is locked.
        This calls Node._treeDrawRequest
        :return:
        """
        # auto = self.setAutoRefresh(True)
        # self.viewport().update()
        # self.setAutoRefresh(auto)
        rootIdx = self.rootIndex()
        if not rootIdx.isValid():
            return

        rootNode = rootIdx.data(ModelRoles.InternalDataRole)

        if not rootNode:
            return

        rootNode.viewDrawRequest(recurse=True, processEvents=True)
        self.viewport().update()

    def setAutoRefresh(self, auto):
        """
        If set to True, the calls to Node._treeDrawRequest will be delayed
        until either set to False, or TreeView.refreshItems is called.
        WARNING : at the moment this will draw ALL loaded nodes,
            not only the visible ones.
        :param auto:
        :return: the auto value that was set prior to this call.
        """
        if auto == self.__autoRefresh:
            return auto

        previousAuto = self.__autoRefresh
        self.__autoRefresh = auto

        if auto:
            self.viewport().update()

        return previousAuto

    def isAutoRefresh(self):
        """
        Return the value of the autoRefresh flag.
        See `TreeView.setAutoRefresh`.
        :return:
        """
        return self.__autoRefresh

    def drawRow(self, painter, option, index):
        """
        Reimplementation of the QTreeView.drawRow method to allow for
        delayed redraw of dirty nodes.
        :param painter:
        :param option:
        :param index:
        :return:
        """
        node = index.data(ModelRoles.InternalDataRole)

        if not self.__autoRefresh and node:
            node.viewDrawRequest()

        super(TreeView, self).drawRow(painter, option, index)

    def keyReleaseEvent(self, event):
        # TODO : better filtering
        key = event.key()
        modifiers = event.modifiers()

        if key == Qt.Qt.Key_Delete and modifiers == Qt.Qt.NoModifier:
            model = self.model()
            selected = self.selectedIndexes()
            nodes = []
            for index in selected:
                leftIndex = model.sibling(index.row(), 0, index)
                leftNode = leftIndex.data(ModelRoles.InternalDataRole)
                if leftNode not in nodes:
                    nodes.append(leftNode)

            self.selectionModel().clear()

            for node in nodes:
                node.delete(widget=self, confirm=True, force=False)

        super(TreeView, self).keyReleaseEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Filter mouse events to catch the right click to display a menu.
        :param event:
        :return:
        """
        if event.button() == Qt.Qt.RightButton and event.buttons() == Qt.Qt.NoButton:
            index = self.indexAt(event.pos())
            node = index.data(ModelRoles.InternalDataRole)

            if node:
                persistentIndex = Qt.QPersistentModelIndex(index)
                qMenu = node.getQMenu(self, persistentIndex=persistentIndex)
                if qMenu and not qMenu.isEmpty():
                    qMenu.exec_(event.globalPos())
                    return

        super(TreeView, self).mouseReleaseEvent(event)

    def setShowUniqueGroup(self, show):
        self.__showUniqueGroup = show
        self.__openPersistentEditors(Qt.QModelIndex(), openEditor=False)
        self.__updateUniqueGroupVisibility()
        self.__openPersistentEditors(Qt.QModelIndex(), openEditor=True)

    def __updateUniqueGroupVisibility(self):
        if self.__userRoot:
            return
        model = self.model()
        if model and model.rowCount() == 1 and not self.__showUniqueGroup:
            index = model.index(0, 0)
            self.__setRootIndex(index)
            self.__setHiddenNodes(index)
        else:
            self.__setRootIndex(Qt.QModelIndex())

    def __setRootIndex(self, index):
        super(TreeView, self).setRootIndex(index)

    def rowsInserted(self, index, start, end):
        super(TreeView, self).rowsInserted(index, start, end)
        self.__updateUniqueGroupVisibility()
        self.__setHiddenNodes(index)
        self.__openPersistentEditors(index, True)

    def __openPersistentEditors(self, parent, openEditor=True, onCollapse=False):
        model = self.model()

        if not model:
            return

        if openEditor:
            meth = self.openPersistentEditor
        else:
            meth = self.closePersistentEditor

        columnCount = self.model().columnCount()

        if not parent.isValid():
            parent = self.rootIndex()

        children = []
        if (
            onCollapse
            or self.isExpanded(parent)
            or parent == self.rootIndex()
            or not parent.isValid()
        ):
            children = [
                model.index(row, 0, parent) for row in range(model.rowCount(parent))
            ]
        while len(children) > 0:
            curParent = children.pop(-1)

            if self.isExpanded(curParent):
                children.extend(
                    [
                        model.index(row, 0, curParent)
                        for row in range(model.rowCount(curParent))
                    ]
                )

            for colIdx in range(columnCount):
                sibling = model.sibling(curParent.row(), colIdx, curParent)
                node = sibling.data(ModelRoles.InternalDataRole)

                if node and node.hidden:
                    continue
                persistent = sibling.data(ModelRoles.PersistentEditorRole)
                if persistent or not openEditor:
                    meth(sibling)

    def setRootIndex(self, index):
        self.__openPersistentEditors(self.rootIndex(), False)
        if index.isValid():
            self.__userRoot = True
            super(TreeView, self).setRootIndex(index)
        else:
            self.__userRoot = False
            self.__updateUniqueGroupVisibility()
        self.__setHiddenNodes(self.rootIndex())
        self.__openPersistentEditors(self.rootIndex(), True)

    def setModel(self, model):
        if self.model():
            try:
                self.__openPersistentEditors(self.rootIndex(), False)
                self.setRootIndex(Qt.QModelIndex())
                prevModel = self.model()
                prevModel.sigRowsRemoved.disconnect(self.rowsRemoved)
                for col in prevModel.columnCount():
                    self.setItemDelegateForColumn(col, None)
            except TypeError:
                pass
        super(TreeView, self).setModel(model)

        if model:
            for col in model.columnsWithDelegates():
                delegate = ItemDelegate(self)
                self.setItemDelegateForColumn(col, delegate)
                delegate.sigDelegateEvent.connect(partial(self.__delegateEvent, col))
                delegate = ItemDelegate(self)
                self.setItemDelegateForColumn(col, delegate)
                delegate.sigDelegateEvent.connect(partial(self.__delegateEvent, col))

        self.__updateUniqueGroupVisibility()
        self.__setHiddenNodes(model.index(0, 0))
        self.__openPersistentEditors(Qt.QModelIndex())

        try:
            self.model().sigRowsRemoved.connect(self.rowsRemoved)
        except TypeError:
            pass

    def rowsAboutToBeRemoved(self, index, start, end):
        self.__openPersistentEditors(index, False)
        super(TreeView, self).rowsAboutToBeRemoved(index, start, end)

    def rowsRemoved(self, index, start, end):
        super(TreeView, self).rowsRemoved(index, start, end)
        self.__openPersistentEditors(index, True)

    def dataChanged(self, topLeft, bottomRight, roles=None):
        super(TreeView, self).dataChanged(topLeft, bottomRight)
        # TODO : only way i found to force the view to check the flags
        # (in case the enable/disable state has changed)
        self.viewport().update()

    def __setHiddenNodes(self, index):
        if not index.isValid():
            index = self.rootIndex()
        if not self.isExpanded(index) and index != self.rootIndex():
            return
        model = self.model()
        if not model:
            return
        rowCount = model.rowCount(index)
        for row in range(rowCount):
            child = index.child(row, 0)
            childNode = child.data(ModelRoles.InternalDataRole)
            if childNode and childNode.hidden:
                self.setRowHidden(row, index, True)

    def __expanded(self, index):
        self.__setHiddenNodes(index)
        self.__openPersistentEditors(index, True)

    def __collapsed(self, index):
        self.__openPersistentEditors(index, False, onCollapse=True)

    def pathToIndex(self, itemPath):
        model = self.model()
        if not model:
            return None

        index = self.model().index(0, 0)

        if not index.isValid():
            return index

        if itemPath == "/":
            return index

        pathSplit = [split for split in itemPath.split("/") if split]

        for elem in pathSplit:
            for row in range(model.rowCount(index)):
                child = model.index(row, 0, index)
                name = model.data(child, Qt.Qt.DisplayRole)
                if name == elem:
                    index = child
                    break
            else:
                index = Qt.QModelIndex()
                break
        return index


class ItemDelegate(Qt.QStyledItemDelegate):
    sigDelegateEvent = Qt.Signal(object, object, object)

    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)

    def sizeHint(self, option, index):
        hint = index.data(ModelRoles.InternalDataRole).sizeHint(index.column())
        if hint.isValid():
            return hint
        return super(ItemDelegate, self).sizeHint(option, index)

    def createEditor(self, parent, option, index):
        node = index.data(role=ModelRoles.InternalDataRole)
        if node:
            editor = node.getEditor(parent, option, index)
            if editor:
                if isinstance(editor, EditorMixin):
                    editor.setViewCallback(self.__notifyView)
                    editor.setModelCallback(self.__notifyModel)
                return editor
        return super(ItemDelegate, self).createEditor(parent, option, index)

    def __notifyModel(self, editor, *args, **kwargs):
        node = editor.node
        if node:
            node._openedEditorEvent(editor, editor.column, args, kwargs)
        # self.commitData.emit(editor)

    def __notifyView(self, editor, *args, **kwargs):
        self.sigDelegateEvent.emit(editor.node, args, kwargs)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def setEditorData(self, editor, index):
        node = index.data(role=ModelRoles.InternalDataRole)
        if node and node.setEditorData(editor, index.column()):
            return
        super(ItemDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        node = index.data(role=ModelRoles.InternalDataRole)
        if node:
            if node._applyEditorData(editor, index.column()):
                return
            try:
                editorData = editor.getEditorData()
            except AttributeError:
                pass
            else:
                node.setData(index.column(), editorData, role=Qt.Qt.EditRole)
        super(ItemDelegate, self).setModelData(editor, model, index)

    def paint(self, painter, option, index):
        klass = index.data(role=ModelRoles.EditorClassRole)
        if klass is not None:
            if not getattr(klass, "persistent", False) and klass.paint(
                painter, option, index
            ):
                return
        super(ItemDelegate, self).paint(painter, option, index)
