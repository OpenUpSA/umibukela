"""
  _    _ ______          _   _______ _    _
 | |  | |  ____|   /\   | | |__   __| |  | |
 | |__| | |__     /  \  | |    | |  | |__| |
 |  __  |  __|   / /\ \ | |    | |  |  __  |
 | |  | | |____ / ____ \| |____| |  | |  | |
 |_|  |_|______/_/    \_\______|_|  |_|  |_|

 - no optional questions - no n/a in cycle1 data
 - one "select all that apply" - visit_reason
   - map valid answers to new columns val True/False
 - remaining columns
   - map known responses to cycle2 values
   - map known responses to 'other' if in cycle2, otherwise n/a
"""


import csv
import pandas as pd


f = open('cycle1/Health_citizen_survey_all.csv')
r = csv.DictReader(f, delimiter=',', quotechar='"')
df = pd.DataFrame(list(r))

# change column names
df.columns = ['waiting_group/medicine_time', 'device_id', 'yes_no_group/examined_private', 'performance_group/respect_admin', 'performance_group/queues', 'performance_group/respect_professionals', 'yes_no_group/consent', 'yes_no_group/safety', 'yes_no_group/all_medication', 'yes_no_group/complaint', 'yes_no_group/complaint_response', 'performance_group/equipment', 'waiting_group/register_time', 'performance_group/ambulance', 'tracking_no', 'personal_comment1', 'personal_comment2', 'clinic_committee', 'clinic_committee_function', 'clinic_feedback', 'improvements_comment', 'demographics_group/gender', 'facility', 'demographics_group/age', 'demographics_group/disability', 'distance', 'demographics_group/income', 'town_village', 'district', 'province', 'surveyor', 'today', 'visit_reason', 'travel_distance', '_uuid', 'waiting_group/professional_time', 'submitted_date', 'performance_group/clean']


# change values

# method
# for val in pd.unique(df.where(df['device_id']=='MAVCEC1')['facility'].ravel()):
#    print val
#
# deviceid doesn't seem to be fixed to a site
#
# df.where(df['town_village']=='Folweni').replace(inplace=True, to_replace={'facility':{'Clinic':'notclinic'}})
# doesn't seem to work

for c in df.columns:
    if c.startswith('waiting_group/'):
        print("### %s ###" % c)
        for val in pd.unique(df[c].ravel()):
            print("'%s': ''," % val)

replacements_all = {
    'town_village': {},
    'district': {},
    'province': {},
    'surveyor': {},
    'today': {},
    'visit_reason': {},
    'travel_distance': {
        '2 km or less': '',
        'More than 8 km': '',
        '3 - 5 km': '',
        '6 - 8 km': '',
    },
    'waiting_group/register_time': {
        'More than 4 hours': '',
        '1 - 2 hours': '',
        'Less than 1 hour': '',
        '2 - 3 hours': '',
        '3 - 4 hours': '',
        'More than 4 hours3 - 4 hours': '',
        'More than 4 hoursLess than 1 hour': '',
    },
    'waiting_group/professional_time': {
        'More than 4 hours': '',
        '2 - 3 hours': '',
        '1 - 2 hours': '',
        '3 - 4 hours': '',
        'Less than 1 hour': '',
        '2 - 3 hours1 - 2 hours': '',
        '3 - 4 hours2 - 3 hours1 - 2 hours': '',
        '2 - 3 hoursLess than 1 hour': '',
    },
    'waiting_group/medicine_time': {
        'More than 4 hours': '',
        '1 - 2 hours': '',
        'Less than 1 hour': '',
        '2 - 3 hours': '',
        '3 - 4 hours': '',
        'More than 4 hours3 - 4 hours': '',
        'More than 4 hoursLess than 1 hour': '',
    },
    'yes_no_group/safety': {
        'Yes': '',
        'No': '',
        'YesNo': '',
    },
    'yes_no_group/examined_private': {
        'Yes': '',
        'No': '',
        'YesNo': '',
    },
    'yes_no_group/consent': {
        'Yes': '',
        'No': '',
        'YesNo': '',
    },
    'yes_no_group/all_medication': {
        'Yes': '',
        'No': '',
        'YesNo': '',
    },
    'yes_no_group/complaint': {
        'Yes': '',
        'No': '',
        'YesNo': '',
    },
    'yes_no_group/complaint_response': {
        'Yes': '',
        'No': '',
        'YesNo': '',
    },
    'personal_comment1': {},
    'performance_group/clean': {
        'Very poor': '',
        'Not good.not bad': '',
        'Poor': '',
        'Good': '',
        'Excellent': '',
        'Not good.not badGood': '',
        'PoorGood': '',
    },
    'performance_group/queues': {
        'Poor': '',
        'Very poor': '',
        'Not good.not bad': '',
        'Good': '',
        'Excellent': '',
        'Very poorExcellent': '',
        'PoorGood': '',
        'Very poorGood': '',
        'Very poorPoor': '',
        'GoodExcellent': '',
    },
    'performance_group/respect_admin': {
        'Poor': '',
        'Very poor': '',
        'Good': '',
        'Not good.not bad': '',
        'Excellent': '',
        'Not good.not badExcellent': '',
        'PoorGood': '',
        'Very poorGood': '',
    },
    'performance_group/respect_professionals': {
        'Very poor': '',
        'Good': '',
        'Poor': '',
        'Excellent': '',
        'Not good.not bad': '',
        'Not good.not badExcellent': '',
        'Very poorExcellent': '',
        'Very poorNot good.not bad': '',
        'GoodExcellent': '',
        'Very poorGood': '',
    },
    'performance_group/ambulance': {
        'Very poor': '',
        'Poor': '',
        'Not good.not bad': '',
        'Good': '',
        'Excellent': '',
        'Very poorExcellent': '',
        'PoorGood': '',
        'Very poorPoorExcellent': '',
        'Not good.not badExcellent': '',
    },
    'performance_group/equipment': {
        'Very poor': '',
        'Poor': '',
        'Not good.not bad': '',
        'Good': '',
        'Excellent': '',
        'PoorExcellent': '',
        'Very poorExcellent': '',
    },
    'personal_comment2': {},
    'clinic_committee': {
        'Yes': '',
        'No': '',
        'Don\'t know': '',
    },
    'clinic_committee_function': {
        'Yes': '',
        'No': '',
        'Don\'t know': '',
    },
    'clinic_feedback': {},
    'improvements_comment': {},
    'demographics_group/gender': {
        'Male': '',
        'Female': '',
    },
    'demographics_group/age': {
        '19 - 40 years old': '',
        '41 - 60 years old': '',
        'Older than 60 years': '',
        'Under 18 years old': '',
    },
    'demographics_group/disability': {
        'No': '',
        'Yes': '',
    },
    'demographics_group/income': {
        'Government grant': '',
        'I do not earn income': '',
        'Permanent employment': '',
        'Temporary employment': '',
        'Small scale vendor (no employees)': '',
        'Own business (with employees)': '',
    },
}

replacements_MAVCEC1 = {
    'facility': {
        'Thabong Clinic': 'thabong',
        'Thabong': 'thabong',
    },
}

replacements_MAVCEC4 = {
    'facility': {
        'Port St Johns': 'port_st_johns',
    },
}

replacements_MAVCJHB5 = {
    'facility': {
        'Soshoanguve Block X Clinic': 'tshwane',
        'Clinic': 'tswane',
        'ufvh': 'tswane',
        'ju5huh': 'tswane',
        'tshwane': 'tswane',
        'Soshoanguve': 'tswane',
    },
}

replacements_MAVCKZN2 = {
    'facility': {
        'siphosethu nzoyi': 'umlazi',
        'Q clinic': 'umlazi',
        'D': 'umlazi',
    },
}

replacements_MAVCKZN5 = {
    'facility': {
        'Clinic': 'folweni',
    },
}

# [c for c in df2.columns if c.startswith("visit_reason")]
# Out[251]:
# ['visit_reason/accompanying',
#  'visit_reason/emergency',
#  'visit_reason/not_well',
#  'visit_reason/other',
#  'visit_reason/pregnant',
#  'visit_reason/regular_collection']
