import umibukela.cycle1_2


"""
|    _  |  /~
|_()(_(||  \_|()\/

 - one "select all that apply" - visit_reason
   - map valid answers to new columns val True/False
 - remaining columns
   - map known responses to cycle2 values
   - map known responses to 'other' if in cycle2, otherwise n/a
"""

"""
tracking no
ward
municipality
province
monitor
date
1. What is your MAIN organisational affiliation?
2. Have you attended a meeting with municipal officials or councillors in the last 6 months?
3. If yes, what type of meeting was it?
4. If yes, Please answer yes or no to these questions about the meeting:
- Was it easy for you to attend the meeting (time and place)?
- Were you notified about the meeting in good time?
- Did you receive all the relevant documents and information in good time before the meeting?
- Did you understand the documents and information?
- Was any information kept away from you?
-Did the municipality make sure that all participants could understand what was being discussed at the meeting?
- Did the meeting provide people with the opportunity to ask questions and express their views freely?
- In your opinion, were women and other vulnerable groups sufficiently represented at the meeting?
5. In your experience, please rate how well you think the municipality performs the following:
- Does the municipality communicate its annual plans in a clear and simple way?
- Does the municipality communicate with citizens in their own language?
- Does the municipality give citizens the opportunity to give input on plans and decisions that affect them?
- Does the municipality consider peoples views before they take important decisions?
- Does the municipality respond to feedback from citizens?
6. Do you think that it is worth spending time and effort to engage with the municipality?
7. What changes would you most like to see in the way the municipality engages with citizens in this municipality??
8. Sex
9. Age
10. How would you descrive the type of house that you live in? Choose the closest option
"""

# In alphabetical order of the original column names according to pandas
#
# 'waiting_group/medicine_time',
columns = ['meeting_group/questions',
           'meeting_group/discussion_understood',
           'meeting_group/documentation',
           'meeting_group/doc_understood',
           'performance_group/clear_communication',
           'performance_group/own_lang',
           'performance_group/citizen_decisions',
           'performance_group/citizen_input',
           'performance_group/citizen_feedback',
           'meeting_group/vulnerable_groups',
           'device_id',
           'performance_group/engagement',
           'performance_group/engagement_changes',
           'demographics_group/gender',
           'demographics_group/age',
           'demographics_group/house',
           'ward',
           'municipality',
           'province',
           'surveyor',
           'today',
           'affiliation',
           'previous_meeting',
           'meeting_type',
           'meeting_group/info_witheld',
           'meeting_group/ease',
           'meeting_group/notification']


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
    'affiliation': {
        'CBO/NGO': 'ngo',
        'CWP': 'other',
        'Civic association member': 'civic_member',
        'Civilians': 'other',
        'Councillor': 'other',
        'EMATU': 'other',
        'Education': 'other',
        'Faith-based organisation': 'faith_based',
        'General Worker.': 'other',
        'Health': 'other',
        'Member of local business association': 'bus_association',
        'Member of ratepayer association': 'ratepayer',
        'None': 'none',
        'Political party': 'political',
        'Residential': 'other',
        'SAMU': 'other',
        'Sports association': 'sports',
        'Student': 'other',
        'Taxi association': 'taxi',
        'Unemployment Workers Union': 'other',
        'Ward committee member': 'ward_member',
        'justice': 'other',
        'womans group': 'other',
        'yes': 'n/a',
    },
    'demographics_group/age': {
        '': 'n/a',
        '18 years and under': 'under_19',
        '19 -35  years old': '19_35',
        '36 - 60 years old': '36_60',
        'Older than 60 years': 'over_60',
    },
    'demographics_group/gender': {
        'Female': 'female',
        'Male': 'male',
    },
    'demographics_group/house': {
        'Informal housing.': 'informal',
        'Own your own house.': 'owner',
        'Structure in backyard of house .': 'backyard_structure',
        'Tenant in council or government property.': 'tenant_gov',
        'Tenant in private property.': 'tenant_pvt',
    },
    'meeting_group/discussion_understood': {
        '': 'n/a',
        'NO': 'no',
        'YES': 'yes',
    },
    'meeting_group/doc_understood': {
        '': 'n/a',
        'YES': 'yes',
        'NO': 'no',
    },
    'meeting_group/documentation': {
        '': 'n/a',
        'NO': 'no',
        'YES': 'yes',
        'YESNO': 'n/a',
    },
    'meeting_group/ease': {
        '': 'n/a',
        'YES': 'yes',
        'NO': 'no',
    },
    'meeting_group/info_witheld': {
        '': 'n/a',
        'NO': 'no',
        'YES': 'yes',
        'YESNO': 'n/a',
    },
    'meeting_group/notification': {
        '': 'n/a',
        'NO': 'no',
        'YES': 'yes',
    },
    'meeting_group/questions': {
        '': 'n/a',
        'NO': 'no',
        'YES': 'yes',
        'YESNO': 'n/a',
    },
    'meeting_group/vulnerable_groups': {
        '': 'n/a',
        'YES': 'yes',
        'NO': 'no',
    },
    'meeting_type': {
        '': 'n/a',
        'A council meeting.': 'council_meeting',
        'A ward meeting.': 'ward_meeting',
        'Development meetings': 'other_meeting',
        'General public meeting/Imbizo': 'other_meeting',
        'IGG': 'other_meeting',
        'IGR': 'other_meeting',
        'To give input into IDP and budget': 'input',
        'To petition or complain about services': 'petition',
        'budget meetings': 'budget_meeting',
        'education': 'other_meeting',
        'igr': 'other_meeting',
        'meeting': 'other_meeting',
        'no': 'n/a',
        'sport and recreation': 'other_meeting',
        'yes': 'n/a',
    },
    'performance_group/citizen_decisions': {
        '': 'n/a',
        'No, only a little.': '2',
        'No, they do this very badly.': '1',
        'Not sure': '3',
        'Yes ,they o this very well': '5',
        'Yes,but could improve ': '4',
    },
    'performance_group/citizen_feedback': {
        '': 'n/a',
        'No, only a little.': '2',
        'No, they do this very badly.': '1',
        'Not sure': '3',
        'Yes ,they o this very well': '5',
        'Yes,but could improve ': '4',
    },
    'performance_group/citizen_input': {
        '': 'n/a',
        'No, only a little.': '2',
        'No, they do this very badly.': '1',
        'Not sure': '3',
        'Yes ,they o this very well': '5',
        'Yes,but could improve ': '4',
    },
    'performance_group/clear_communication': {
        '': 'n/a',
        'No, only a little.': '2',
        'No, they do this very badly.': '1',
        'Not sure': '3',
        'Yes ,they o this very well': '5',
        'Yes,but could improve ': '4',
    },
    'performance_group/engagement': {
        'Mostly not': 'mostly_not',
        'Not at all': 'not_at_all',
        'Not sure': 'not_sure',
        'Yes sometimes': 'yes_sometimes',
        'Yes,defintely': 'yes_definitely',
    },
    'performance_group/own_lang': {
        '': 'n/a',
        'No, only a little.': '2',
        'No, they do this very badly.': '1',
        'Not sure': '3',
        'Yes ,they o this very well': '5',
        'Yes,but could improve ': '4',
    },
    'previous_meeting': {
        'NO': 'no',
        'YES': 'yes',
    },
}

#     'MAVCEC1': {
#         'facility': {
#             'Thabong Clinic': 'thabong',
device_replacements = {
    'EC': {
        'office_name': {
            r'.*': 'office2',
        },
    },
    'WC': {
        'office_name': {
            r'.*': 'office1',
        },
    },
}

#    'MAVCEC1': 'Health Citizen Survey MAVCEC1 - Data.csv',
device_files = {
    'EC': 'Participatory Govt Assessment Tool - EC - Data.csv',
    'WC': 'Participatory Govt Assessment Tool - WC - Data.csv',
}


# [c for c in df2.columns if c.startswith("visit_reason")]
#
#    'visit_reason': ['accompanying',
select_all_that_applies_columns = {}


def run():
    return umibukela.cycle1_2.run(columns, replacements_all, device_files, device_replacements, select_all_that_applies_columns)
