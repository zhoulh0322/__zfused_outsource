# coding:utf-8
# --author-- lanhua.zhou
from __future__ import print_function


class Item(object):
    """
    数据类
    """

    def __init__(self, object, id, parent=None):
        self._parent_item = parent
        self._object = object
        self._id = id
        self._item_handle = None
        self._child_items = []

    def set_parent(self, parent):
        self._parent_item = parent

    def object(self):
        """
        itemdata object

        """
        return self._object

    def id(self):
        """
        return id

        """
        return self._id

    def append_child(self, item):
        self._child_items.append(item)
        item.set_parent(self)

    def child(self, row):
        return self._child_items[row]

    def children(self, allDescendents=False):
        if not allDescendents:
            return self._child_items

    def child_count(self, allDescendents=False):
        """
        return all child count

        rtype: int
        """
        if not allDescendents:
            return len(self._child_items)

        all_child = []

        def count(item, all_child):
            children = item.children()
            if children:
                all_child.append(item.children())
                for _item in children:
                    count(_item, all_child)
        count(self, all_child)

        return len(all_child)

    def parent(self):
        return self._parent_item

    def row(self):
        if self._parent_item:
            return self._parent_item._child_items.index(self)
        return 0


if __name__ == "__main__":
    import zfused_api

    _status_ids = zfused_api.status.status_ids()
    _projects = zfused_api.zFused.get("project", filter={"StatusId__in": "|".join([str(_s) for _s in _status_ids])})
    _all_data = []
    for _status_id in _status_ids:
        _status_item = Item("status", _status_id)
        for _project in _projects:
            if _status_id == _project["StatusId"]:
                _item = Item("project", _project["Id"])
                _status_item.append_child(_item)
        _all_data.append(_status_item)

    print(_all_data[0].children())
