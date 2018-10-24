from collections import OrderedDict


def form_questions(form):
    d = OrderedDict()
    children = form['children']
    for child in children:
        if 'children' in child:
            for minor in child['children']:
                if 'pathstr' in minor:
                    d.update({minor['pathstr']: ''})
        else:
            d.update({child['pathstr']: ''})

    if 'Contact_number' in d:
        del d['Contact_number']
    if 'Full_name' in d:
        del d['Full_name']
    if 'Monitor_name' in d:
        del d['Monitor_name']
    if 'phonenumber' in d:
        del d['phonenumber']
    if 'capturer' in d:
        del d['capturer']
    if 'surveyor' in d:
        del d['surveyor']
    if 'Monitor_Name' in d:
        del d['Monitor_Name']
    if 'phone_number' in d:
        del d['phone_number']
    return d


def export_row(answer, fields):
    obj = answer.answers
    for k in fields.keys():
        try:
            fields[k] = obj[k]
        except KeyError:
            del fields[k]
    return fields
