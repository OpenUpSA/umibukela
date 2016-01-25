import pandas as pd
import json

df = pd.read_csv('DOH-Citizen-Survey_2016_01_25_04_22_15.csv', sep=',', encoding='latin-1')
site = df[df['facility'] == 'folweni']


form_file = open('DOH-Citizen-Survey.json')
form = json.loads(form_file.read())

results = {'questions': {}}


def print_item(indent, children, path):
    for child in children:
        deeper_path = path + [child['name']]
        if deeper_path in [['facility'], ['demographics_group', 'gender']]:
            pass
        elif ('type' in child) and child['type'] == 'select one':
            print("%s SELECTONE [%s] (%s) %s" % (indent, '/'.join(deeper_path), calc_leaf(deeper_path), child['label']))
            print_item(indent + '\t', child['children'], deeper_path)
        elif ('type' in child) and child['type'] == 'group' and child['name'] == 'meta':
            pass
        elif ('type' in child) and child['type'] == 'group':
            print("%s GROUP %s" % (indent, child['name']))
            print_item(indent + '\t', child['children'], deeper_path)
        elif ('type' in child) and child['type'] == 'select all that apply':
            print("%s SELECTALL [%s] %s" % (indent, '/'.join(deeper_path), child['label']))
            print_item(indent + '\t', child['children'], deeper_path)
        elif ('type' not in child):
            print("%s OPTION [%s] %s" % (indent, '/'.join(deeper_path), child['label']))
        else:
            # print("%s UNKNOWN %s" % (indent, child))
            pass

def calc_leaf(path):
    cols = ['facility', 'demographics_group/gender', '/'.join(path)]
    #print cols
    question_table = site.loc[:, cols]
    question_counts = question_table.groupby(['demographics_group/gender', '/'.join(path)]).count()
    #q1groupcount.loc['female','no']
    return question_counts

print_item('', form['children'], [])
