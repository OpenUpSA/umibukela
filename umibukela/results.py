"""
survey response summary calculation
"""

import pdb


def count_submissions(submissions):
    results = {}
    # per-gender counts
    cols = ['facility', 'demographics_group/gender']
    question_table = submissions.loc[:, cols]
    gender_counts = question_table.groupby(
        ['demographics_group/gender']
    ).count()
    for gender in ['female', 'male']:
        results = deep_dict_set(
            results,
            int(gender_counts.loc[gender]),
            [gender]
        )

    # total count
    results = deep_dict_set(
        results,
        int(submissions.loc[:, ['facility']].count()),
        ['total']
    )
    return results


def count_options(
        submissions,
        children,
        path=[],
        question_results={},
        current_option_counts={}):
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
            question_results = count_options(
                submissions,
                child['children'],
                deeper_path,
                question_results,
                {})
        elif (child_is_type(child, 'select one')
              or child_is_type(child, 'select all that apply')):
            # multiple choice questions
            current_option_counts = count_question_options(
                submissions,
                deeper_path
            )
            question_results = deep_dict_set(
                question_results,
                child['label'],
                [pathstr(deeper_path), 'label']
            )
            question_results = count_options(
                submissions,
                child['children'],
                deeper_path,
                question_results,
                current_option_counts
            )
        elif ('type' not in child):
            # option in multiple choice question
            question_results = deep_dict_set(
                question_results,
                child['label'],
                [pathstr(path), 'options', child['name'], 'label']
            )
            question_results = set_option_counts(
                path,
                child['name'],
                question_results,
                current_option_counts
            )
        else:
            pass
    return question_results


def child_is_type(child, type):
    return ('type' in child) and child['type'] == type


def count_question_options(site_submissions, path):
    cols = ['facility', 'demographics_group/gender', pathstr(path)]
    question_table = site_submissions.loc[:, cols]
    question_counts = question_table.groupby(
        ['demographics_group/gender', pathstr(path)]
    ).count()
    return question_counts


def set_option_counts(path, option_name, results, current_option_counts):
    for gender in ['male', 'female']:
        option_table = current_option_counts
        # keys that can be int are known as int indexes to the DataFrame
        try:
            option_name_as_idx = int(option_name)
        except:
            option_name_as_idx = option_name

        try:
            val = int(option_table.loc[gender, option_name_as_idx])
        except KeyError:
            # values that aren't counted because they don't occur in the
            # results for this question won't be indexes in the counts
            val = 0

        results = deep_dict_set(
            results,
            val,
            [pathstr(path), 'options', option_name, 'count', gender]
        )
    return results


def pathstr(path):
    """ / separated path from array of strings"""
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


def questions_dict_to_array(question_dict):
    """
    Turn the question-name-keyed dict into an array of questions and options
    """
    questions = []
    for q_key in question_dict.keys():
        question = question_dict[q_key]
        options_dict = question['options']
        options = []
        for o_key in options_dict.keys():
            option = options_dict[o_key]
            option['key'] = o_key
            options.append(option)
        question['options'] = options  # overwrite
        question['key'] = q_key
        questions.append(question)
    return questions


def calc_q_percents(questions, site_totals):
    #pdb.set_trace()
    """
    updates and returns a questions dict with percentages for option counts
    """
    for q_key in questions.keys():
        for o_key in questions[q_key]['options'].keys():
            for gender in ['female', 'male']:
                o_count = questions[q_key]['options'][o_key]['count'][gender]
                g_count = site_totals[gender]
                pct = (float(o_count)/float(g_count))*100
                deep_dict_set(
                    questions,
                    pct,
                    [q_key, 'options', o_key, 'pct', gender]
                )
    return questions
