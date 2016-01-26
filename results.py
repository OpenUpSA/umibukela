import pandas as pd
import json
import pprint

df = pd.read_csv('DOH-Citizen-Survey_2016_01_25_04_22_15.csv', sep=',', encoding='latin-1')
site_submissions = df[df['facility'] == 'folweni']


form_file = open('DOH-Citizen-Survey.json')
form = json.loads(form_file.read())


def calc_q_results(children, path, question_results, leaf_results):
    """
    returns nested dicts where the keys are the names of the XForm element
    branches to each question and each option of a question. Only multiple
    choice questions are supported.
    """
    for child in children:
        deeper_path = path + [child['name']]
        if deeper_path in [['facility'], ['demographics_group', 'gender']]:
            pass
        elif child_is_type(child, 'group') and child['name'] == 'meta':
            pass
        elif child_is_type(child, 'group'):
            question_results = calc_q_results(
                child['children'],
                deeper_path,
                question_results,
                leaf_results)
        elif (child_is_type(child, 'select one')
              or child_is_type(child, 'select all that apply')):
            leaf_results['/'.join(deeper_path)] = calc_leaf(
                site_submissions, deeper_path
            )
            question_results = deep_dict_set(
                question_results,
                child['label'],
                [pathstr(deeper_path), 'label']
            )
            question_results = calc_q_results(
                child['children'],
                deeper_path,
                question_results,
                leaf_results
            )
        elif ('type' not in child):
            question_results = deep_dict_set(
                question_results,
                child['label'],
                [pathstr(path), 'options', child['name'], 'label']
            )
            question_results = set_leaf_results(
                path,
                child['name'],
                question_results,
                leaf_results
            )
        else:
            pass
    return question_results


def child_is_type(child, type):
    return ('type' in child) and child['type'] == type


def calc_leaf(site_submissions, path):
    cols = ['facility', 'demographics_group/gender', '/'.join(path)]
    question_table = site_submissions.loc[:, cols]
    question_counts = question_table.groupby(
        ['demographics_group/gender', pathstr(path)]
    ).count()
    return question_counts


def set_leaf_results(path, leaf_key, results, leaf_results):
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

            results = deep_dict_set(
                results,
                val,
                [pathstr(path), 'options', leaf_key, 'count', gender]
            )
    return results


def pathstr(path):
    return '/'.join(path)


def deep_dict_set(deep_dict, value, layers):
    layer = layers[0]
    if layers[1:]:
        if layer in deep_dict:
            deep_dict[layer] = deep_dict_set(
                deep_dict[layer],
                value,
                layers[1:]
            )
        else:
            deep_dict[layer] = deep_dict_set({}, value, layers[1:])
    else:
        deep_dict[layer] = value

    return deep_dict

question_results = calc_q_results(form['children'], [], {}, {})

pprint.pprint(question_results)
