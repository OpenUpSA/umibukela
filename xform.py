import csv


def deep_dict_set(deep_dict, value, layers):
    layer = layers[0]

    if layers[1:]:
        if layer in deep_dict:
            deep_dict[layer] = deep_dict_set(deep_dict[layer], value, layers[1:])
        else:
            deep_dict[layer] = deep_dict_set({}, value, layers[1:])
    else:
        deep_dict[layer] = value

    return deep_dict


def make_row_dict(column_deep_keys, row_values):
    row_dict = {}
    for col_idx in range(len(column_deep_keys)):
        row_dict = deep_dict_set(row_dict, row_values[col_idx], column_deep_keys[col_idx])

    return row_dict

class CSVDicts:
    def __init__(self, filename):
        self.f = open(filename)
        self.f = csv.reader(self.f, delimiter=',', quotechar='"')
        header = self.f.next()
        self.column_deep_keys = map(lambda column: column.split('/'), header)

    def __iter__(self):
        return self

    def next(self):
        row = self.f.next()
        return make_row_dict(self.column_deep_keys, row)

# l = xform.CSVDicts('SASSA-Citizen_2016_01_19_04_35_51.csv')
# for item in l:
#    print item
#
# '{"facility": "paarl", "capturer": "Bukiwe", "surveyor": "H Williams", "meta": {"instanceID": "uuid:26bb3ff3-cafb-41f5-9ef3-5eee2b443192"}, "sim_imei": "354993060885132", "end": "2015-06-02T15:30:36.951+02", "service": "existing_grant_issue", "performance_group": {"respect": "4", "queues": "4", "service_satisfaction": "4", "clean": "4", "information": "4"}, "visit_reason": {"war_veterans": "False", "social_relief": "False", "old_age": "True", "disability": "False", "care_dependency": "False", "in_aid": "False", "foster_child": "False", "child_support": "False"}, "start": "2015-06-02T15:24:29.515+02", "demographics_group": {"gender": "female", "age": "older_60"}, "today": "2015-06-02", "phone_number": "n/a", "yes_no_group": {"documents": "yes", "nametag": "yes", "alt_id": "yes", "bribe": "no"}, "_uuid": "26bb3ff3-cafb-41f5-9ef3-5eee2b443192", "personal_comment": "None", "transport_amount": "twentysix_fifty", "improvements_comment": "n/a", "device_id": "354993060885132", "visit_frequency": "second", "_submission_time": "2015-06-15T12:14:43", "frequency_reason": ":-)no", "service_other": "n/a", "clinic_feedback": "yes", "waiting_time": "thirty_one"}'
#
#...
