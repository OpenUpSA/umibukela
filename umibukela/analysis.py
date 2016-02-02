"""
survey response summary calculation
"""


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
            [gender],
            int(gender_counts.loc[gender])
        )

    # total count
    results = deep_dict_set(
        results,
        ['total'],
        int(submissions.loc[:, ['facility']].count())
    )
    return results


def count_options(
        submissions,
        children,
        path=None,
        question_results=None,
        current_option_counts=None):
    """
    returns nested dicts where the keys are the names of the XForm element
    branches to each question and each option of a question. Only multiple
    choice questions are supported.
    """
    path = path or []
    question_results = question_results or {}
    idx = 0  # The index of the child in the form in its array of siblings
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
                None)
        elif (child_is_type(child, 'select one')
              or child_is_type(child, 'select all that apply')):
            # multiple choice questions
            current_option_counts = count_question_options(
                submissions,
                deeper_path
            )
            question_results = deep_dict_set(
                question_results,
                [pathstr(deeper_path), 'label'],
                child['label']
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
                [pathstr(path), 'options', child['name'], 'label'],
                child['label']
            )
            question_results = deep_dict_set(
                question_results,
                [pathstr(path), 'options', child['name'], 'idx'],
                idx
            )
            question_results = set_option_counts(
                path,
                child['name'],
                question_results,
                current_option_counts
            )
        else:
            pass
        idx += 1
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

        try:
            val = int(option_table.loc[gender, option_name])
        except KeyError:
            # values that aren't counted because they don't occur in the
            # results for this question won't be indexes in the counts
            print("########################################")
            print(path, gender, option_name)
            print(option_table)
            val = 0

        results = deep_dict_set(
            results,
            [pathstr(path), 'options', option_name, 'count', gender],
            val
        )
    return results


def pathstr(path):
    """ / separated path from array of strings"""
    return '/'.join(path)


def deep_dict_set(deep_dict, path, value):
    key = path[0]
    if path[1:]:
        if key in deep_dict:
            deep_dict[key] = deep_dict_set(
                deep_dict[key],
                path[1:],
                value
            )
        else:
            deep_dict[key] = deep_dict_set({}, path[1:], value)
    else:
        deep_dict[key] = value

    return deep_dict


def questions_dict_to_array(question_dict):
    """
    Turn the question-name-keyed dict into an array of questions and options
    """
    questions = []
    for q_key, question in question_dict.iteritems():
        options_dict = question['options']
        options = [None] * len(options_dict)
        for o_key, option in options_dict.iteritems():
            option = options_dict[o_key]
            option['key'] = o_key
            options[option['idx']] = option
        question['options'] = options  # overwrite
        question['key'] = q_key
        questions.append(question)
    return questions


def calc_q_percents(questions, site_totals):
    """
    updates and returns a questions dict with percentages for option counts
    """
    for q_key, question in questions.iteritems():
        for o_key, option in question['options'].iteritems():
            for gender in ['female', 'male']:
                o_count = option['count'][gender]
                g_count = site_totals[gender]
                pct = (float(o_count)/float(g_count))*100
                deep_dict_set(
                    option,
                    ['pct', gender],
                    pct
                )
    return questions
