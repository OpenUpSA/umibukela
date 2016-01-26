import pandas as pd
import json
import pprint

df = pd.read_csv('DOH-Citizen-Survey_2016_01_25_04_22_15.csv', sep=',', encoding='latin-1')
site_submissions = df[df['facility'] == 'folweni']


form_file = open('DOH-Citizen-Survey.json')
form = json.loads(form_file.read())

# returns nested dicts where the keys are the names of the XForm element
# branches to each question and each option of a question. Only multiple
# choice questions are supported.

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
            question_results = deep_dict_set(question_results, child['label'], [pathstr(deeper_path), 'label'])
            question_results = calc_q_results(indent + '\t', child['children'], deeper_path, question_results, leaf_results)
        elif ('type' in child) and child['type'] == 'select all that apply':
            leaf_results['/'.join(deeper_path)] = calc_leaf(site_submissions, deeper_path)
            print("%sSELECTALL [%s] %s" % (indent, '/'.join(deeper_path), child['label']))
            question_results = deep_dict_set(question_results, child['label'], [pathstr(deeper_path), 'label'])
            question_results = calc_q_results(indent + '\t', child['children'], deeper_path, question_results, leaf_results)
        elif ('type' not in child):
            print("%sOPTION [%s] %s" % (indent, '/'.join(deeper_path), child['label']))
            question_results = deep_dict_set(question_results, child['label'], [pathstr(path), 'options', child['name'], 'label'])
            question_results = set_leaf_results(path, child['name'], question_results, leaf_results)
        else:
            # print("%s UNKNOWN %s" % (indent, child))
            pass
    return question_results


def calc_leaf(site_submissions, path):
    cols = ['facility', 'demographics_group/gender', '/'.join(path)]
    question_table = site_submissions.loc[:, cols]
    question_counts = question_table.groupby(['demographics_group/gender', pathstr(path)]).count()
    return question_counts


def set_leaf_results(path, leaf_key, results, leaf_results):
    # print leaf_results
    if '/'.join(path) in leaf_results:
        for gender in ['male', 'female']:
            leaf_table = leaf_results[pathstr(path)]
            # keys that can be int are known as int indexes to the DataFrame
            try:
                leaf_key_as_idx = int(leaf_key)
            except:
                leaf_key_as_idx = leaf_key

            try:
                val = int(leaf_table.loc[gender, leaf_key_as_idx])
            except KeyError:
                # values that aren't counted because they don't occur in the
                # results for this question won't be indexes in the counts
                val = 0

            results = deep_dict_set(results, val, [pathstr(path), 'options', leaf_key, 'count', gender])
    return results


def pathstr(path):
    return '/'.join(path)


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

question_results = calc_q_results('', form['children'], [], {}, {})

pprint.pprint(question_results)
