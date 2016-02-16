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
    'visit_reason': {
        'State Old Age Grant': 'old_age',
        'Disability Grant': 'disability',
        'Child-Support Grant': 'child_support',
        'Social relief of distress': 'social_relief',
        'Foster Child Grant': 'foster_child',
        'Care Dependency Grant': 'care_dependency',
        'War-Veteran\'s Grant': 'war_veterans',
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
    'performance_group/information': {
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
    'performance_group/service_satisfaction': {
        'Very poor': '1',
        'Poor': '2',
        'OK': '3',
        'Good': '4',
        'Excellent': '5',
        'Not applicable': 'n/a',
    },
    'service': {
        '': 'other',
        'Appeal against a previous decision not to pay you a grant': 'appeal',
        'Apply for a new grant': 'apply',
        'Changing of payment': 'other',
        'Come for a new card': 'other',
        'Come to fetch my Sassa grant card.': 'other',
        'Complain about bad service that you received': 'service_complaint',
        'Enquire about deductions from your grant or short payments': 'deductions_enquiry',
        'Fetch Sassa child\'s card for grant': 'other',
        'General inquiry or get information about grants': 'general_enquiry',
        'Get a "life certificate"': 'live_certificate',
        'Grant in Aid': 'other',
        'Hand in grant forms.': 'other',
        'Lost Sassa grant card.': 'other',
        'Lost card now came to make a new one.': 'other',
        'Lost the child\'s card now coming to make a new one': 'other',
        'Make a  new Sassa grant card': 'other',
        'Make a new card': 'other',
        'Make a new card.': 'other',
        'Report lost card': 'other',
        'Sort out a problem with an existing grant': 'existing_grant_issue',
        'Transfer money to grandmother.': 'other',
        'Transfer of child\'s grant': 'other',
        'Transfer of grant to me': 'other',
        'Transfer': 'other',
        'Waiting for a Sassa pay card.': 'other',
        'adding child': 'other',
        'adding': 'other',
        'aplication for cancelling child support grant': 'other',
        'application for lost card': 'other',
        'application of cancelling for child support grant': 'other',
        'card block': 'other',
        'card lost': 'other',
        'change grant from mother to grandma': 'other',
        'come to change the money to be transferred to me': 'other',
        'for fingerprints': 'other',
        'get the last grant': 'other',
        'i lost my sassa card so im ere for the new one': 'other',
        'im her to renew my grant': 'other',
        'im here for doctors appointment': 'other',
        'im here for the result of my application': 'other',
        'im here to add another child': 'other',
        'im here to renew my grant': 'other',
        'lost card': 'other',
        'make a new card': 'other',
        'no answer': 'n/a',
        'pick many': 'n/a',
        'proof of pension': 'other',
        'renew my grant': 'other',
        'renw my grant': 'other',
        't0 add another child': 'other',
        'to add another child': 'other',
        'to book doctor appointment': 'other',
        'to bring doctors letter': 'other',
        'to cancell child support grant': 'other',
        'to change the grant': 'other',
        'to make a sassa card': 'other',
        'to make sassa card': 'other',
    },
    'transport_amount': {
        'R11 - R25': 'eleven_twentyfive',
        'Nothing': 'nothing',
        'R26 - R50': 'twentysix_fifty',
        'Less than R10': 'under_ten',
        'R51 - R75': 'fiftyone_seventyfive',
        'More than R75': 'more_seventyfive',
    },
    'visit_frequency': {
        'This is my second visit for this same issue': 'first',
        'This is my first visit for this issue': 'second',
        'This is my 3rd or more visit for the same issue': 'third_mode',
    },
    'waiting_time': {
        '30 minutes - 1 hour': 'thirty_one',
        '1 - 2 hours': 'one_two',
        '2 - 4 hours': 'two_four',
        '4 - 6 hours': 'four_six',
        'Less than 30 minutes': 'under_thirty',
        'More than 6 hours': 'more_four',
    },
    'yes_no_group/alt_id': {
        'Yes': 'yes',
        'No': 'no',
        '': 'n/a',
    },
    'yes_no_group/bribe': {
        'Yes': 'yes',
        'No': 'no',
        '': 'n/a',
    },
    'yes_no_group/documents': {
        'Yes': 'yes',
        'No': 'no',
        '': 'n/a',
    },
    'yes_no_group/nametag': {
        'Yes': 'yes',
        'No': 'no',
        '': 'n/a',
    },
}

#     'MAVCEC1': {
#         'facility': {
#             'Thabong Clinic': 'thabong',
device_replacements = {
    'MAVCCT4': {  # gugulethu
        'facility': {
            r'.*': 'gugulethu',
        },
    },
    'MAVCKZN3': {  # utrecht
        'facility': {
            r'.*': 'utrecht',
        },
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
    'visit_reason': [
        'old_age',
        'disability',
        'child_support',
        'social_relief',
        'foster_child',
        'care_dependency',
        'war_veterans',
    ],
}


def run():
    return umibukela.cycle1_2.run(columns, replacements_all, device_files, device_replacements, select_all_that_applies_columns)
