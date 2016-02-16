import json
import csv
import sys
import httplib
import base64

"""
submits a formhub survey to KoboToolbox given an XForm in JSON and a formhub
csv export.

e.g.

submit_csv.submit('form.json', 'formhub_export.csv', 'form_id', 'username', 'password')
-----..........................................................................
...............................................................................
...............................................................................
............................................................................
{'successful': 308, 'failed': 0, 'already': 5, 'total': 313}"""

class Element(object):
    def __init__(self, element, path):
        self.label = element.get('label', '')
        self.name = element['name']
        self.path = path + [element['name']]
        self.pathstr = pathstr(self.path)

    def __str__(self):
        return "%s %s" % (self.__class__, self.pathstr)


class Question(Element):
    pass


class MultipleChoice(Question):
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


def traverse(element, state, handlers, path=None, group_labels=None):
    """
    """
    path = path or []  # list of names in structure leading to current element
    group_labels = group_labels or []  # list of labels in groups in path
    for child in element['children']:
        deeper_path = path + [child['name']]
        if child.get('type') == 'group':
            deeper_group_labels = group_labels + [child.get('label', '')]
            traverse(child, state, handlers, deeper_path, deeper_group_labels)
        elif child.get('type') == 'select one':
            question = SelectOne(child, path, group_labels)
            state = handlers[SelectOne](question, state)
        elif child.get('type') == 'select all that apply':
            question = SelectAllThatApply(child, path, group_labels)
            state = handlers[SelectAllThatApply](question, state)
        else:
            question = Question(child, path)
            state = handlers[SelectOne](question, state)
    return state


def deep_set(deep_dict, path, value):
    key = path[0]
    if path[1:]:
        if key in deep_dict:
            deep_dict[key] = deep_set(deep_dict[key], path[1:], value)
        else:
            deep_dict[key] = deep_set({}, path[1:], value)
    else:
        deep_dict[key] = value

    return deep_dict


def deep_get(deep_dict, path):
    key = path[0]
    if path[1:]:
        return deep_get(deep_dict[key], path[1:])
    else:
        return deep_dict[key]


def select_one(q, state):
    val = deep_get(state, ['row', q.pathstr])
    if val == 'n/a':
        val = None
    path = ['submission'] + q.path
    return deep_set(state, path, val)


def select_all_that_apply(q, state):
    selected = []
    path = ['submission'] + q.path
    for o in q.options:
        val = deep_get(state, ['row', o.pathstr])
        if val == 'n/a':
            return deep_set(state, path, None)
        elif val == 'True':
            selected += [o.name]
    return deep_set(state, path, selected)


def submit(form_path, submissions_path, form_id, username, password):
    with open(form_path) as form_file:
        form = json.loads(form_file.read())

    with open(submissions_path) as submissions_file:
        submissions = list(csv.DictReader(submissions_file))

    handlers = {
        SelectOne: select_one,
        SelectAllThatApply: select_all_that_apply,
    }

    headers = {
        "Content-type": "application/json",
        "Authorization": "Basic %s" % auth(username, password),
    }

    successful = 0
    already = 0
    failed = 0
    for submission in submissions:
        state = {
            'row': submission,
            'submission': {},
        }

        state = traverse(form, state, handlers)

        body = json.dumps({
            'submission': state['submission'],
            'id': form_id,
        })

        conn = httplib.HTTPSConnection("kc.kobotoolbox.org")
        conn.request("POST", "/api/v1/submissions", body, headers)
        response = conn.getresponse()
        if response.status == 201:
            successful += 1
            sys.stdout.write('.')
        elif response.status == 202:
            already += 1
            sys.stdout.write('-')
        else:
            failed += 1
            sys.stdout.write(response.status, response.reason)
        sys.stdout.flush()
        conn.close()

    print({
        'successful': successful,
        'already': already,
        'failed': failed,
        'total': len(submissions)
    })


def auth(u, p):
    return base64.b64encode("%s:%s" % (u, p))
