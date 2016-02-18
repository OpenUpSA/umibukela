import umibukela.importer.cycle1_2


"""
  _________   _____    _________ _________   _____
 /   _____/  /  _  \  /   _____//   _____/  /  _  \
 \_____  \  /  /_\  \ \_____  \ \_____  \  /  /_\  \
 /        \/    |    \/        \/        \/    |    \
/_______  /\____|__  /_______  /_______  /\____|__  /   PAYPOINT
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
columns = [
    'yes_no_group/money_lenders',
    'yes_no_group/bribe',
    'performance_group/queues',
    'performance_group/respect',
    'performance_group/assistance',
    'deductions_agree',
    'yes_no_group/safety',
    'yes_no_group/documents',
    'yes_no_group/complaint',
    'yes_no_group/response',
    'performance_group/access',
    'ease_access',
    'transport_amount',
    'waiting_time',
    'personal_comment',
    'clinic_feedback',
    'improvements_comment',
    'demographics_group/gender',
    'demographics_group/age',
    'town_village',
    'local_office',
    'district',
    'monitor',
    'today',
    'visit_reason/care_dependency',
    'visit_reason/child_support',
    'visit_reason/disability',
    'visit_reason/foster_child',
    'visit_reason/social_relief',
    'visit_reason/old_age',
    'visit_reason/war_veterans',
    'yes_no_group/deductions',
    'performance_group/clean',
]


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
    'visit_reason/care_dependency': {
        '': 'False',
        'Care Dependency Grant': 'True',
    },
    'visit_reason/child_support': {
        '': 'False',
        'Child-Support Grant': 'True',
    },
    'visit_reason/disability': {
        '': 'False',
        'Disability Grant': 'True',
    },
    'visit_reason/foster_child': {
        '': 'False',
        'Foster Child Grant': 'True',
    },
    'visit_reason/social_relief': {
        '': 'False',
        'Social relief of distress': 'True',
    },
    'visit_reason/old_age': {
        '': 'False',
        'State Old Age Grant': 'True',
    },
    'visit_reason/war_veterans': {
        '': 'False',
        'War-Veteran\'s Grant': 'True',
    },
    'clinic_feedback': {
        'Yes': 'yes',
        'No': 'no',
        'Maybe': 'maybe',
    },
    'demographics_group/age': {
        '26 - 40 years old': '26_40',
        '41 - 60 years old': '40_60',
        'Older than 60 years': 'older_60',
        'Under 25 years old': 'under_25',
    },
    'demographics_group/gender': {
        'Male': 'male',
        'Female': 'female',
    },
    'performance_group/clean': {
        'Very poor': '1',
        'Poor': '2',
        'OK': '3',
        'Good': '4',
        'Excellent': '5',
        'Not applicable': 'n/a',
        '': 'n/a',
    },
    'performance_group/queues': {
        'Very poor': '1',
        'Poor': '2',
        'OK': '3',
        'Good': '4',
        'Excellent': '5',
        'Not applicable': 'n/a',
        '': 'n/a',
    },
    'performance_group/respect': {
        'Very poor': '1',
        'Poor': '2',
        'OK': '3',
        'Good': '4',
        'Excellent': '5',
        'Not applicable': 'n/a',
        '': 'n/a',
    },
    'performance_group/access': {
        'Very poor': '1',
        'Poor': '2',
        'OK': '3',
        'Good': '4',
        'Excellent': '5',
        'Not applicable': 'n/a',
        '': 'n/a',
    },
    'performance_group/assistance': {
        'Very poor': '1',
        'Poor': '2',
        'OK': '3',
        'Good': '4',
        'Excellent': '5',
        'Not applicable': 'n/a',
        '': 'n/a',
    },
    'transport_amount': {
        'R11 - R25': 'eleven_twentyfive',
        'Nothing': 'nothing',
        'R26 - R50': 'twentysix_fifty',
        'Less than R10': 'under_ten',
        'R51 - R75': 'fiftyone_seventyfive',
        'More than R75': 'more_seventyfive',
        '': 'n/a',
    },
    'waiting_time': {
        '30 minutes - 1 hour': 'thirty_one',
        '1 - 2 hours': 'one_two',
        '2 - 4 hours': 'two_four',
        '4 - 6 hours': 'four_six',
        'Less than 30 minutes': 'under_thirty',
    },
    'yes_no_group/bribe': {
        'Yes': 'yes',
        'No': 'no',
        'Not applicable': 'n/a',
    },
    'yes_no_group/documents': {
        'Yes': 'yes',
        'No': 'no',
        'Not applicable': 'n/a',
    },
    'yes_no_group/money_lenders': {
        'Yes': 'yes',
        'No': 'no',
        'Not applicable': 'n/a',
    },
    'yes_no_group/complaint': {
        'Yes': 'yes',
        'No': 'no',
        'Not applicable': 'n/a',
    },
    'yes_no_group/safety': {
        'Yes': 'yes',
        'No': 'no',
        'Not applicable': 'n/a',
        'YesNo': 'n/a',
    },
    'yes_no_group/response': {
        'Yes': 'yes',
        'No': 'no',
        'Not applicable': 'n/a',
        'YesNo': 'n/a',
    },
    'yes_no_group/deductions': {
        'Yes': 'yes',
        'No': 'no',
        'Not applicable': 'n/a',
        'NoNot applicable': 'n/a',
    },
    'deductions_agree': {
        'Yes': 'yes',
        'No': 'no',
        'Not applicable': 'n/a',
    },
    'ease_access': {
        'Easy': 'easy',
        'Difficulto': 'difficult',
        'Very difficult': 'very_difficult',
    },
    'clinic_feedback': {
        'Yes': 'yes',
        'No': 'no',
        'Maybe': 'maybe',
    },
}

#     'MAVCEC1': {
#         'facility': {
#             'Thabong Clinic': 'thabong',
device_replacements = {
    'MAVCCT5': {
        'facility': 'montagu',
    },
    'MAVCCT1': {
        'facility': 'kaigarib',
    },
}

#    'MAVCEC1': 'Health Citizen Survey MAVCEC1 - Data.csv',
device_files = {
    'MAVCCT5': 'SASSA Citizen Survey Pay Point MAVCCT5 - Data.csv',
    'MAVCCT1': 'NEW SASSA Citizen Survey Pay Point MAVCCT1 - Data.csv',
}


# [c for c in df2.columns if c.startswith("visit_reason")]
#
#    'visit_reason': ['accompanying',
select_all_that_applies_columns = {
}


def run():
    return umibukela.importer.cycle1_2.run(columns, replacements_all, device_files, device_replacements, select_all_that_applies_columns)
