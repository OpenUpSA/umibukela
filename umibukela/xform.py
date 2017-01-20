class XForm(dict):

    def set_by_path(self, path, el):
        return self._set_child_by_path(self, path.split('/'), el)

    def get_by_path(self, path):
        return self._get_child_by_path(self, path.split('/'))

    def del_by_path(self, path):
        return self._del_child_by_path(self, path.split('/'))

    @classmethod
    def _get_child_by_path(cls, parent, path):
        for c in parent.get('children'):
            if c.get('name', '') == path[0]:
                if len(path) == 1:
                    return c
                else:
                    return cls._get_child_by_path(c, path[1:])
        return None

    @classmethod
    def _del_child_by_path(cls, parent, path):
        for i, c in enumerate(parent.get('children')):
            if c.get('name', '') == path[0]:
                if len(path) == 1:
                    parent.get('children').pop(i)
                    return True
                else:
                    return cls._del_child_by_path(c, path[1:])
        return None

    @classmethod
    def _set_child_by_path(cls, parent, path, el):
        if len(path) == 1:
            cls._del_child_by_path(parent, path)
            el['name'] = path[0]
            parent['children'].append(el)
        else:
            direct_parent = cls._get_child_by_path(parent, path[:-1])
            cls._set_child_by_path(direct_parent, [path[-1]], el)


class Element(object):
    def __init__(self, element, path):
        self.label = element['label']
        self.name = element['name']
        self.path = path + [element['name']]
        self.pathstr = pathstr(self.path)

    def __str__(self):
        return "%s %s" % (self.__class__, self.pathstr)


class MultipleChoice(Element):
    def __init__(self, question, path, group_labels):
        super(MultipleChoice, self).__init__(question, path)
        self.options = [Option(o, self.path) for o in question['children']]
        self.group_labels = group_labels


class Option(Element):
    pass


class SelectOne(MultipleChoice):
    pass


class SelectAllThatApply(MultipleChoice):
    pass


def pathstr(path):
    """ / separated path from array of strings"""
    return '/'.join(path)
