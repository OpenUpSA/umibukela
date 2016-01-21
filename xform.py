header = 'today,start,end,device_id,sim_imei,phone_number,facility,surveyor,capturer,visit_reason/old_age,visit_reason/disability,visit_reason/child_support,visit_reason/foster_child,visit_reason/care_dependency,visit_reason/war_veterans,visit_reason/social_relief,visit_reason/in_aid,service,service_other,transport_amount,waiting_time,visit_frequency,frequency_reason,yes_no_group/documents,yes_no_group/nametag,yes_no_group/bribe,yes_no_group/alt_id,performance_group/clean,performance_group/queues,performance_group/respect,performance_group/information,performance_group/service_satisfaction,personal_comment,clinic_feedback,improvements_comment,demographics_group/gender,demographics_group/age,meta/instanceID,_uuid,_submission_time'

row = '2015-06-02,2015-06-02T15:24:29.515+02,2015-06-02T15:30:36.951+02,354993060885132,354993060885132,n/a,paarl,H Williams,Bukiwe,True,False,False,False,False,False,False,False,existing_grant_issue,n/a,twentysix_fifty,thirty_one,second,:-)no,yes,yes,no,yes,4,4,4,4,4,None,yes,n/a,female,older_60,uuid:26bb3ff3-cafb-41f5-9ef3-5eee2b443192,26bb3ff3-cafb-41f5-9ef3-5eee2b443192,2015-06-15T12:14:43'

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


def make_row_dict():
    column_deep_keys = map(lambda column: column.split('/'), header.split(','))

    row_dict = {}
    row_values = row.split(',')

    for col_idx in range(len(column_deep_keys)):
        row_dict = deep_dict_set(row_dict, row_values[col_idx], column_deep_keys[col_idx])

    return row_dict


# '{"facility": "paarl", "capturer": "Bukiwe", "surveyor": "H Williams", "meta": {"instanceID": "uuid:26bb3ff3-cafb-41f5-9ef3-5eee2b443192"}, "sim_imei": "354993060885132", "end": "2015-06-02T15:30:36.951+02", "service": "existing_grant_issue", "performance_group": {"respect": "4", "queues": "4", "service_satisfaction": "4", "clean": "4", "information": "4"}, "visit_reason": {"war_veterans": "False", "social_relief": "False", "old_age": "True", "disability": "False", "care_dependency": "False", "in_aid": "False", "foster_child": "False", "child_support": "False"}, "start": "2015-06-02T15:24:29.515+02", "demographics_group": {"gender": "female", "age": "older_60"}, "today": "2015-06-02", "phone_number": "n/a", "yes_no_group": {"documents": "yes", "nametag": "yes", "alt_id": "yes", "bribe": "no"}, "_uuid": "26bb3ff3-cafb-41f5-9ef3-5eee2b443192", "personal_comment": "None", "transport_amount": "twentysix_fifty", "improvements_comment": "n/a", "device_id": "354993060885132", "visit_frequency": "second", "_submission_time": "2015-06-15T12:14:43", "frequency_reason": ":-)no", "service_other": "n/a", "clinic_feedback": "yes", "waiting_time": "thirty_one"}'
