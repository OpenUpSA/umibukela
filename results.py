import pandas as pd
import json

# df = pd.read_csv('DOH-Citizen-Survey_2016_01_25_04_22_15.csv', sep=',', encoding='latin-1')
# folweni = df[df['facility'] == 'folweni']
# cols = ['facility', 'demographics_group/gender', 'yes_no_group/all_medication']
# q1 = folweni.loc[:,cols]
# q1groupcount = q1.groupby(['demographics_group/gender', 'yes_no_group/all_medication']).count()
# q1groupcount.loc['female','no']


form_file = open('DOH-Citizen-Survey.json')
form = json.loads(form_file.read())


def print_item(indent, children):
    for child in children:
        if ('type' in child) and child['type'] == 'select one':
            print("%s SELECTONE %s" % (indent, child['name']))
            print_item(indent + '\t', child['children'])
        elif ('type' in child) and child['type'] == 'group':
            print("%s GROUP %s" % (indent, child['name']))
            print_item(indent + '\t', child['children'])
        elif ('type' in child) and child['type'] == 'select all that apply':
            print("%s SELECTALL %s" % (indent, child['name']))
            print_item(indent + '\t', child['children'])

        elif ('type' not in child):
            print("%s OPTION %s" % (indent, child['name']))
        else:
            #print("%s UNKNOWN %s" % (indent, child))
            pass

print_item('', form['children'])
