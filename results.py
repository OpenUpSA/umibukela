import pandas as pd
import json
import pprint

df = pd.read_csv('DOH-Citizen-Survey_2016_01_25_04_22_15.csv', sep=',', encoding='latin-1')
site_submissions = df[df['facility'] == 'folweni']


form_file = open('DOH-Citizen-Survey.json')
form = json.loads(form_file.read())



def calc_q_results(indent, children, path, question_results, leaf_results):
    for child in children:
        deeper_path = path + [child['name']]
        if deeper_path in [['facility'], ['demographics_group', 'gender']]:
            pass
        elif ('type' in child) and child['type'] == 'group' and child['name'] == 'meta':
            pass
        elif ('type' in child) and child['type'] == 'group':
            print("%sGROUP %s" % (indent, child['name']))
            question_results = calc_q_results(indent + '\t', child['children'], deeper_path, question_results, leaf_results)
        elif ('type' in child) and child['type'] == 'select one':
            leaf_results['/'.join(deeper_path)] = calc_leaf(site_submissions, deeper_path)
            print("%sSELECTONE [%s] %s" % (indent, '/'.join(deeper_path), child['label']))
            question_results = calc_q_results(indent + '\t', child['children'], deeper_path, question_results, leaf_results)
        elif ('type' in child) and child['type'] == 'select all that apply':
            leaf_results['/'.join(deeper_path)] = calc_leaf(site_submissions, deeper_path)
            print("%sSELECTALL [%s] %s" % (indent, '/'.join(deeper_path), child['label']))
            question_results = calc_q_results(indent + '\t', child['children'], deeper_path, question_results, leaf_results)
        elif ('type' not in child):
            print("%sOPTION [%s] %s" % (indent, '/'.join(deeper_path), child['label']))
            question_results = set_leaf_results(path, child['name'], question_results, leaf_results)
        else:
            # print("%s UNKNOWN %s" % (indent, child))
            pass
    return question_results


def calc_leaf(site_submissions, path):
    cols = ['facility', 'demographics_group/gender', '/'.join(path)]
    question_table = site_submissions.loc[:, cols]
    question_counts = question_table.groupby(['demographics_group/gender', '/'.join(path)]).count()
    #q1groupcount.loc['female','no']
    return question_counts


def set_leaf_results(path, leaf_key, results, leaf_results):
    # print leaf_results
    if '/'.join(path) in leaf_results:
        for gender in ['male', 'female']:
            leaf_table = leaf_results['/'.join(path)]
            try:
                val = int(leaf_table.loc[gender, leaf_key])
            except KeyError:
                val = 0
            # print("set_leaf_results path=%s gender=%s leaf=%s val=%s" % ('/'.join(path), gender, leaf_key, val))
            results = deep_dict_set(results, val, path + ['count', gender, leaf_key])
            #results = deep_dict_set(results, 0, path + ['count', gender])
    return results


def deep_dict_set(deep_dict, value, layers):
    layer = layers[0]
    # print("deep_dict_set dict=%s layers=%s value=%s" % (deep_dict, layers, value))
    if layers[1:]:
        if layer in deep_dict:
            deep_dict[layer] = deep_dict_set(deep_dict[layer], value, layers[1:])
        else:
            deep_dict[layer] = deep_dict_set({}, value, layers[1:])
    else:
        deep_dict[layer] = value

    return deep_dict

question_results = calc_q_results('', form['children'], [], {}, {})

pprint.pprint(question_results)
