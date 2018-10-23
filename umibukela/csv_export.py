def export_row(answer):
    obj = answer.answers
    if 'Contact_number' in obj:
        del obj['Contact_number']
    if 'Full_name' in obj:
        del obj['Full_name']
    if 'Monitor_name' in obj:
        del obj['Monitor_name']
    if 'phonenumber' in obj:
        del obj['phonenumber']
    if 'capturer' in obj:
        del obj['capturer']
    if 'surveyor' in obj:
        del obj['surveyor']
    if 'Monitor_Name' in obj:
        del obj['Monitor_Name']

    obj['created_at'] = answer.created_at
    obj['updated_at'] = answer.updated_at
    return obj
