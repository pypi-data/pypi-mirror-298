import os

import h5py

from silx.gui import qt as Qt
from silx.gui.icons import getQIcon

from ..model.Node import Node
from ..model.ModelDef import ModelColumns


_registeredNodes = {}
_registeredAttributes = {}


def getNodeClass(nodeType, attrs=None):
    klass = None
    if attrs:
        for key, value in attrs.items():
            info = _registeredAttributes.get(key)
            if info:
                if hasattr(value, "decode"):
                    value = value.decode()
                klass = info.get(value)
                if klass:
                    break
    if not klass:
        klass = _registeredNodes.get(nodeType)
    return klass


def registerNodeClass(klass):
    global _registeredNodes
    global _registeredAttributes

    nodeType = klass.nodeType
    if nodeType in _registeredNodes:
        raise AttributeError(
            "Failed to register node type {0}."
            "Already registered."
            "".format(klass.__name__)
        )

    # TODO : some kind of checks on the klass
    _registeredNodes[nodeType] = klass

    attribute = klass.attribute
    # TODO : improve this...
    if attribute:
        if attribute[0] in _registeredAttributes:
            if attribute[1] in _registeredAttributes[attribute[0]]:
                raise AttributeError(
                    "Failed to register attribute {0}."
                    "Already registered."
                    "".format(klass.__name__)
                )
        else:
            _registeredAttributes[attribute[0]] = {}
        _registeredAttributes[attribute[0]][attribute[1]] = klass


def H5NodeClassDef(
    nodeType,
    # icons=None,
    # editors=None,
    attribute=None,
    **kwargs,
):
    def inner(cls):
        cls.nodeType = nodeType
        if "editors" in kwargs:
            editors = kwargs.get("editors")
            cls.editors = editors
        if "icons" in kwargs:
            icons = kwargs.get("icons")
            cls.icons = icons
        cls.attribute = attribute
        registerNodeClass(cls)
        return cls

    return inner


def _getNodeInfo(h5File, h5Path):
    attrs = dict([(key, value) for key, value in h5File[h5Path].attrs.items()])
    itemClass = h5File.get(h5Path, getclass=True)
    itemLink = h5File.get(h5Path, getclass=True, getlink=True)
    return itemClass, itemLink, attrs


def H5NodeFactory(h5File, h5Path):
    # TODO : allow for a h5py object to be passed
    klass = itemClass = itemLink = attrs = None

    try:
        if isinstance(h5File, h5py.File):
            itemClass, itemLink, attrs = _getNodeInfo(h5File, h5Path)
        else:
            with h5py.File(h5File, mode="r") as h5f:
                itemClass, itemLink, attrs = _getNodeInfo(h5f, h5Path)
    except KeyError:
        klass = Hdf5ErrorNode

    if klass is None:
        klass = getNodeClass(itemLink, attrs=attrs)
    if klass is None:
        klass = getNodeClass(itemClass, attrs=attrs)
    if klass is None:
        klass = getNodeClass("H5Base", attrs=attrs)
    if klass is not None:
        return klass(h5File=h5File, h5Path=h5Path)
    else:
        raise ValueError(
            "Node creation failed. " "(was : {0}:{1})".format(h5File, h5Path)
        )


_H5NodeFactory = H5NodeFactory


def setH5NodeFactory(factory):
    global _H5NodeFactory
    _H5NodeFactory = factory


@H5NodeClassDef("H5Base")
class H5Base(Node):
    className = "H5Base"

    h5File = property(lambda self: self.__h5File)
    h5Path = property(lambda self: self.__h5Path)

    def __init__(self, h5File=None, h5Path="/", **kwargs):
        # temporary until the API is frozen

        if h5File is None:
            raise ValueError("<h5File> argument is mandatory.")

        self.__h5File = h5File
        self.__h5Path = (h5Path != "/" and h5Path.rstrip("/")) or h5Path
        self.className = os.path.basename(h5File).rpartition(".")[0]

        super(H5Base, self).__init__(subject=self, **kwargs)

        basepath = os.path.basename(self.h5Path)
        self._setDataInternal(ModelColumns.NameColumn, basepath)
        self._setDataInternal(ModelColumns.NameColumn, basepath, role=Qt.Qt.EditRole)

    @staticmethod
    def factory(h5File, h5Path):
        return _H5NodeFactory(h5File, h5Path)

    def _loadChildren(self):
        base = self.h5Path.rstrip("/")
        with h5py.File(self.__h5File, mode="r") as h5f:
            # not using value.name in case this item is an external
            # link : value.name is relative to the external file's root.
            try:
                paths = [base + "/" + key for key in h5f[self.__h5Path].keys()]
            except AttributeError:
                paths = []
        newChildren = [H5Base.factory(self.__h5File, path) for path in paths]
        newChildren = newChildren
        return newChildren

    def _refreshNode(self):
        with h5py.File(self.h5File, mode="r") as h5f:
            thisItem = h5f[self.h5Path]
            try:
                keys = set(thisItem.keys())
            except AttributeError:
                return
            if not keys:
                return
            children = set()
            for index in range(self.childCount()):
                child = self.child(index)
                if isinstance(child, H5Base):
                    children.add(os.path.basename(child.h5Path.rstrip("/")))
            diff = keys - children

        for newItem in diff:
            self.appendChild(_H5NodeFactory(self.h5File, self.h5Path + "/" + newItem))


@H5NodeClassDef(None, icons=Qt.QStyle.SP_MessageBoxCritical)
class Hdf5ErrorNode(H5Base):
    def __init__(self, *args, **kwargs):
        super(Hdf5ErrorNode, self).__init__(*args, **kwargs)
        self._setIsValid(False)

    def _loadChildren(self):
        """
        Reimplementation of H5Base._loadChildren to return an empty list.
        :return:
        """
        return []


@H5NodeClassDef(h5py.File, icons=Qt.QStyle.SP_FileIcon)
class H5File(H5Base):
    className = "H5Base"

    def __init__(self, *args, **kwargs):
        super(H5File, self).__init__(*args, **kwargs)

        self._setDataInternal(
            ModelColumns.NameColumn,
            os.path.basename(self.h5File).rpartition(".")[0],
            role=Qt.Qt.DisplayRole,
        )

        self._setDataInternal(ModelColumns.NameColumn, self.h5File, Qt.Qt.ToolTipRole)


@H5NodeClassDef(nodeType=h5py.ExternalLink, icons=Qt.QStyle.SP_FileLinkIcon)
class H5ExternalLinkNode(H5Base):
    recurseDeletion = False

    def __init__(self, **kwargs):
        super(H5ExternalLinkNode, self).__init__(**kwargs)

        with h5py.File(self.h5File, mode="r") as h5f:
            item = h5f[self.h5Path]
            self.__externalFile = filename = item.file.filename
            followLink = item.attrs.get("XsocsExpand")
            del item
        self.__followLink = followLink if followLink is not None else False

        basename = os.path.basename(filename).rpartition(".")[0]
        self._setDataInternal(ModelColumns.NameColumn, basename, role=Qt.Qt.DisplayRole)
        self._setDataInternal(ModelColumns.NameColumn, filename, role=Qt.Qt.ToolTipRole)

    externalFile = property(lambda self: self.__externalFile)


@H5NodeClassDef(nodeType=h5py.Group, icons=Qt.QStyle.SP_DirIcon)
class H5GroupNode(H5Base):
    pass


@H5NodeClassDef(nodeType=h5py.Dataset)
class H5DatasetNode(H5Base):
    def __init__(self, **kwargs):
        super(H5DatasetNode, self).__init__(**kwargs)
        iconTpl = "item-{0}dim"
        with h5py.File(self.h5File, mode="r") as h5f:
            item = h5f[self.h5Path]
            ndims = len(item.shape)
            if ndims == 0:
                data = item[()]
                if hasattr(data, "decode"):
                    text = data.decode().replace("\n", " ")
                else:
                    text = str(data)
            elif ndims == 1 and item.shape[0] < 5:
                text = str(item[:])
            else:
                text = "..."
            del item

        icon = iconTpl.format(ndims)
        try:
            icon = getQIcon(icon)
        except ValueError:
            icon = getQIcon("item-ndim")

        self._setDataInternal(ModelColumns.NameColumn, icon, Qt.Qt.DecorationRole)

        self._setDataInternal(ModelColumns.ValueColumn, text, role=Qt.Qt.DisplayRole)
