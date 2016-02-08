import umibukela.cycle1_2


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


# In alphabetical order of the original column names according to pandas
columns = ['waiting_group/medicine_time', 'device_id', 'yes_no_group/examined_private', 'performance_group/respect_admin', 'performance_group/queues', 'performance_group/respect_professionals', 'yes_no_group/consent', 'yes_no_group/safety', 'yes_no_group/all_medication', 'yes_no_group/complaint', 'yes_no_group/complaint_response', 'performance_group/equipment', 'waiting_group/register_time', 'performance_group/ambulance', 'tracking_no', 'personal_comment1', 'personal_comment2', 'clinic_committee', 'clinic_committee_function', 'clinic_feedback', 'improvements_comment', 'demographics_group/gender', 'facility', 'demographics_group/age', 'demographics_group/disability', 'distance', 'demographics_group/income', 'town_village', 'district', 'province', 'surveyor', 'date', 'visit_reason', 'travel_distance', '_uuid', 'waiting_group/professional_time', 'submitted_date', 'performance_group/clean']


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

replacements_all = {
    'visit_reason': {
        '3 days for infant': 'accompanying',
        '6 weeks': 'other',
        'Accompanying someone else': 'accompanying',
        'Accompanying someone elseI visit regularly to collect monthly medication and/or check-up.': 'accompanying,regular_collection',
        'Emergency': 'emergency',
        'EmergencyAccompanying someone else': 'emergency,accompanying',
        'EmergencyI visit regularly to collect monthly medication and/or check-up.': 'emergency,accompanying',
        'Family planning': 'other',
        'Generally not feeling well': 'not_well',
        'Generally not feeling wellAccompanying someone else': 'not_well,accompanying',
        'Generally not feeling wellEmergency': 'not_well,emergency',
        'Generally not feeling wellI visit regularly to collect monthly medication and/or check-up.': 'not_well,regular_collection',
        'Generally not feeling wellchild to scale': 'not_well,other',
        'Generally not feeling welltesting': 'not_well,other',
        'I visit regularly to collect monthly medication and/or check-up.': 'regular_collection',
        'Immunisation': 'other',
        'Personal': 'other',
        'Pregnant mother and children': 'pregnant',
        'Pregnant mother and childrenEmergencyI visit regularly to collect monthly medication and/or check-up.': 'pregnant,emergency,regular_collection',
        'baby vaccination': 'other',
        'body height and weight': 'other',
        'checking TB': 'other',
        'checkup': 'other',
        'child check up': 'accompanying',
        'child immunization': 'accompanying',
        'child sick': 'accompanying',
        'child vaccination': 'accompanying',
        'child was not feeling well': 'accompanying',
        'child was sick': 'accompanying',
        'child': 'accompanying',
        'children immunisation': 'accompanying',
        'chronic / high blood': 'other',
        'contraception': 'other',
        'diahria': 'other',
        'diarrhea': 'other',
        'doctor appointment': 'other',
        'family planning': 'other',
        'getting results': 'other',
        'have water bumps under my feet.': 'other',
        'i transferred by hospital': 'other',
        'immunisation': 'other',
        'immunizations': 'other',
        'inLabour': 'pregnant',
        'injection': 'other',
        'maternity': 'pregnant',
        'my children were sick': 'accompanying',
        'new born': 'other',
        'pregnancy test': 'other',
        'pregnancy': 'pregnant',
        'pregnant an to check blood': 'pregnant,other',
        'preventing': 'other',
        'prevention': 'other',
        'private matter': 'other',
        'private': 'other',
        'taking child to the clinic': 'accompanying',
        'test Tb': 'other',
        'testing HIV and high blood': 'other',
        'testing': 'other',
        'the child is sick': 'accompanying',
        'to check BP and diabetes.': 'other',
        'to check BP': 'other',
        'to check bp': 'other',
        'tooth pains': 'other',
        'transfer': 'other',
        'treatment': 'other',
        'vommiting and drousy': 'other',
    },
    'travel_distance': {
        '2 km or less': 'under_two',
        'More than 8 km': 'more_eight',
        '3 - 5 km': 'two_five',
        '6 - 8 km': 'six_eight',
    },
    'waiting_group/register_time': {
        'More than 4 hours': 'more_four',
        '1 - 2 hours': 'one_two',
        'Less than 1 hour': 'under_one',
        '2 - 3 hours': 'two_three',
        '3 - 4 hours': 'three_four',
        'More than 4 hours3 - 4 hours': 'n/a',
        'More than 4 hoursLess than 1 hour': 'n/a',
    },
    'waiting_group/professional_time': {
        'More than 4 hours': 'more_four',
        '1 - 2 hours': 'one_two',
        'Less than 1 hour': 'under_one',
        '2 - 3 hours': 'two_three',
        '3 - 4 hours': 'three_four',
        '2 - 3 hours1 - 2 hours': 'n/a',
        '3 - 4 hours2 - 3 hours1 - 2 hours': 'n/a',
        '2 - 3 hoursLess than 1 hour': 'n/a',
    },
    'waiting_group/medicine_time': {
        'More than 4 hours': 'more_four',
        '1 - 2 hours': 'one_two',
        'Less than 1 hour': 'under_one',
        '2 - 3 hours': 'two_three',
        '3 - 4 hours': 'three_four',
        'More than 4 hours3 - 4 hours': 'n/a',
        'More than 4 hoursLess than 1 hour': 'n/a',
    },
    'yes_no_group/safety': {
        'Yes': 'yes',
        'No': 'no',
        'YesNo': 'n/a',
    },
    'yes_no_group/examined_private': {
        'Yes': 'yes',
        'No': 'no',
        'YesNo': 'n/a',
    },
    'yes_no_group/consent': {
        'Yes': 'yes',
        'No': 'no',
        'YesNo': 'n/a',
    },
    'yes_no_group/all_medication': {
        'Yes': 'yes',
        'No': 'no',
        'YesNo': 'n/a',
    },
    'yes_no_group/complaint': {
        'Yes': 'yes',
        'No': 'no',
        'YesNo': 'n/a',
    },
    'yes_no_group/complaint_response': {
        'Yes': 'yes',
        'No': 'no',
        'YesNo': 'n/a',
    },
    'distance': {
        'Yes': 'yes',
        'No': 'no',
    },
    'performance_group/clean': {
        'Very poor': '1',
        'Poor': '2',
        'Not good.not bad': '3',
        'Good': '4',
        'Excellent': '5',
        'Not good.not badGood': 'n/a',
        'PoorGood': 'n/a',
    },
    'performance_group/queues': {
        'Excellent': '5',
        'Good': '4',
        'GoodExcellent': 'n/a',
        'Not good.not bad': '3',
        'Poor': '2',
        'PoorGood': 'n/a',
        'Very poor': '1',
        'Very poorExcellent': 'n/a',
        'Very poorGood': 'n/a',
        'Very poorPoor': 'n/a',
    },
    'performance_group/respect_admin': {
        'Excellent': '5',
        'Good': '4',
        'Not good.not bad': '3',
        'Not good.not badExcellent': 'n/a',
        'Poor': '2',
        'PoorGood': 'n/a',
        'Very poor': '1',
        'Very poorGood': 'n/a',
    },
    'performance_group/respect_professionals': {
        'Excellent': '5',
        'Good': '4',
        'GoodExcellent': 'n/a',
        'Not good.not bad': '3',
        'Not good.not badExcellent': 'n/a',
        'Poor': '2',
        'Very poor': '1',
        'Very poorExcellent': 'n/a',
        'Very poorGood': 'n/a',
        'Very poorNot good.not bad': 'n/a',
    },
    'performance_group/ambulance': {
        'Excellent': '5',
        'Good': '4',
        'Not good.not bad': '3',
        'Not good.not badExcellent': 'n/a',
        'Poor': '2',
        'PoorGood': 'n/a',
        'Very poor': '1',
        'Very poorExcellent': 'n/a',
        'Very poorPoorExcellent': 'n/a',
    },
    'performance_group/equipment': {
        'Excellent': '5',
        'Good': '4',
        'Not good.not bad': '3',
        'Poor': '2',
        'PoorExcellent': 'n/a',
        'Very poor': '1',
        'Very poorExcellent': 'n/a',
    },
    'clinic_committee': {
        'Yes': 'yes',
        'No': 'no',
        'Don\'t know': 'unsure',
    },
    'clinic_committee_function': {
        'Yes': 'yes',
        'No': 'no',
        'Don\'t know': 'n/a',
    },
    'demographics_group/gender': {
        'Male': 'male',
        'Female': 'female',
    },
    'demographics_group/age': {
        '19 - 40 years old': '19_40',
        '41 - 60 years old': '40_60',
        'Older than 60 years': 'older_60',
        'Under 18 years old': 'under_18',
    },
    'demographics_group/disability': {
        'No': 'no',
        'Yes': 'yes',
    },
    'demographics_group/income': {
        'Government grant': 'gov_grant',
        'I do not earn income': 'none',
        'Permanent employment': 'perm_employ',
        'Temporary employment': 'temp_employ',
        'Small scale vendor (no employees)': 'small_vendor',
        'Own business (with employees)': 'own_business',
    },
}

device_replacements = {
    'MAVCEC1': {
        'facility': {
            'Thabong Clinic': 'thabong',
            'Thabong': 'thabong',
        },
    },
    'MAVCEC4': {
        'facility': {
            'Port St Johns': 'port_st_johns',
        },
    },
    'MAVCJHB5': {
        'facility': {
            'Soshoanguve Block X Clinic': 'tshwane',
            'Soshanguve Block X Clinic': 'tshwane',
            'Clinic': 'tshwane',
            'ufvh': 'tshwane',
            'ju5huh': 'tshwane',
            'Soshoanguve': 'tshwane',
        },
    },
    'MAVCKZN2': {
        'facility': {
            'siphosethu nzoyi': 'umlazi',
            'Q clinic': 'umlazi',
            'D': 'umlazi',
        },
    },
    'MAVCKZN5': {
        'facility': {
            'Clinic': 'folweni',
            'Folweni Clinic': 'folweni',
        },
    },
}

device_files = {
    'MAVCEC1': 'Health Citizen Survey MAVCEC1 - Data.csv',
    'MAVCEC4': 'Health Citizen Survey MAVCEC4 - Data.csv',
    'MAVCJHB5': 'Health Citizen Survey MAVCJHB5 - Data.csv',
    'MAVCKZN2': 'Health Citizen Survey MAVCKZN2 - Data.csv',
    'MAVCKZN5': 'Health Citizen Survey MAVCKZN5 - Data.csv'
}


# [c for c in df2.columns if c.startswith("visit_reason")]
select_all_that_applies_columns = {
    'visit_reason': ['accompanying',
                     'emergency',
                     'not_well',
                     'other',
                     'pregnant',
                     'regular_collection']
}

def run():
    return umibukela.cycle1_2.run(columns, device_files, device_replacements, select_all_that_applies_columns)
