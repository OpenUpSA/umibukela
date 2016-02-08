import umibukela.cycle1_2


"""
  _________   _____    _________ _________   _____
 /   _____/  /  _  \  /   _____//   _____/  /  _  \
 \_____  \  /  /_\  \ \_____  \ \_____  \  /  /_\  \
 /        \/    |    \/        \/        \/    |    \
/_______  /\____|__  /_______  /_______  /\____|__  /
        \/         \/        \/        \/         \/

 - no optional questions
 - one "select all that apply" - visit_reason
   - map valid answers to new columns val True/False
 - remaining columns
   - map known responses to cycle2 values
   - map known responses to 'other' if in cycle2, otherwise n/a
"""


# In alphabetical order of the original column names according to pandas
#
# 'waiting_group/medicine_time',
columns = ['yes_no_group/alt_id', 'yes_no_group/bribe', 'performance_group/information', 'yes_no_group/nametag', 'performance_group/queues', 'performance_group/respect', 'yes_no_group/documents', 'tracking_no', 'transport_amount', 'waiting_time', 'visit_frequecy', 'frequency_reason', 'personal_comment', 'clinic_feedback', 'improvements_comment', 'demographics_group/gender', 'facility', 'demographics_group/age', 'picture_permission', 'town_village', 'district', 'province', 'surveyor', 'today', 'visit_reason', 'service', 'performance_group/clean', 'performance_group/service_satisfaction', 'submitted_date', 'device_id', '_uuid']


# change values

# method
# for val in pd.unique(df.where(df['device_id']=='MAVCEC1')['facility'].ravel()):
#    print val
#
# deviceid doesn't seem to be fixed to a site
#
# df.where(df['town_village']=='Folweni').replace(inplace=True, to_replace={'facility':{'Clinic':'notclinic'}})
# doesn't seem to work

# for c in df.columns:
#     if c.startswith('waiting_group/'):
#         print("### %s ###" % c)
#         for val in pd.unique(df[c].ravel()):
#             print("'%s': ''," % val)

#    'visit_reason': {
#        '3 days for infant': 'accompanying',
replacements_all = {
    'yes_no_group/alt_id': {},
    'yes_no_group/bribe': {},
    'performance_group/information': {},
    'yes_no_group/nametag': {},
    'performance_group/queues': {},
    'performance_group/respect': {},
    'yes_no_group/documents': {},
    'transport_amount': {},
    'waiting_time': {},
    'visit_frequecy': {},
    'frequency_reason': {},
    'personal_comment': {},
    'clinic_feedback': {},
    'improvements_comment': {},
    'demographics_group/gender': {},
    'demographics_group/age': {},
    'picture_permission': {},
    'town_village': {},
    'district': {},
    'province': {},
    'service': {},
    'performance_group/clean': {},
    'performance_group/service_satisfaction': {},
}

#     'MAVCEC1': {
#         'facility': {
#             'Thabong Clinic': 'thabong',
device_replacements = {
    'MAVCCT4': {
        'facility': {},
    },
    'MAVCKZN3': {
        'facility': {},
    },
    'MAVCKZN4': {
        'facility': {},
    },
    'MAVCT3': {
        'facility': {},
    },
    'MAVEC3': {
        'facility': {},
    },
    'MAVEC5': {
        'facility': {},
    },
    'MAVJHB1': {
        'facility': {},
    },
    'MAVJHB2': {
        'facility': {},
    },
    'MAVJHB4': {
        'facility': {},
    },
    'MAVKZN1': {
        'facility': {},
    },
}

#    'MAVCEC1': 'Health Citizen Survey MAVCEC1 - Data.csv',
device_files = {
    'MAVCCT4': 'SASSA Citizen Survey Service Office MAVCCT4.csv',
    'MAVCKZN3': 'SASSA Citizen Survey Service Office MAVCKZN3.csv',
    'MAVCKZN4': 'SASSA Citizen Survey Service Office MAVCKZN4.csv',
    'MAVCT3': 'SASSA Citizen Survey Service Office MAVCT3.csv',
    'MAVEC3': 'SASSA Citizen Survey Service Office MAVEC3.csv',
    'MAVEC5': 'SASSA Citizen Survey Service Office MAVEC5.csv',
    'MAVJHB1': 'SASSA Citizen Survey Service Office MAVJHB1.csv',
    'MAVJHB2': 'SASSA Citizen Survey Service Office MAVJHB2.csv',
    'MAVJHB4': 'SASSA Citizen Survey Service Office MAVJHB4.csv',
    'MAVKZN1': 'SASSA Citizen Survey Service Office MAVKZN1.csv',
}


# [c for c in df2.columns if c.startswith("visit_reason")]
#
#    'visit_reason': ['accompanying',
select_all_that_applies_columns = {
    'visit_reason': {},
}

def run():
    return umibukela.cycle1_2.run(columns, device_files, device_replacements, select_all_that_applies_columns)
