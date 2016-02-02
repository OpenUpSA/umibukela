"""
Survey response summary calculation

Calculation builds up a nested dict structure which makes referencing columns
and specific values easy. This is converted to an array structure for Django
Template Language to be able to put it on the screen.

The results nested dict looks something like
{u'demographics_group/age': {
     'label': u'How old are you?',
     'options': {
         u'under_25': {'count': {'female': 53,
                            'male': 11},
                       'idx': 0,
                       'key': ,
                       'label': u'Under 25 years old',
                       'pct': {'female': 26.903553299492383,
                               'male': 10.2803738317757}},
                       {'count': {'female': 101,
                                  'male': 56},
                        'idx': 1,
                        'key': u'26_40',
                        'label': u'26 - 40 years old',
                        'pct': {'female': 51.26903553299492,
                                'male': 52.336448598130836}},
where the keys are group path names then the q name separated by /
and options are under the options field keyed on option name.

The results array looks something like
[{'key': u'demographics_group/age',
  'label': u'How old are you?',
  'options': [{'count': {'female': 53,
                         'male': 11},
               'idx': 0,
               'key': u'under_25',
               'label': u'Under 25 years old',
               'pct': {'female': 26.903553299492383,
                       'male': 10.2803738317757}},
where questions are in an array and each question's options are
in an array under the question's options field.
"""


# These are used for grouping. Trying to count them and group by them
# at the same time doesn't work.
SKIP_QUESTIONS = [['facility'], ['demographics_group', 'gender']]


class Element(object):
    def __init__(self, element, path):
        self.label = element['label']
        self.name = element['name']
        self.path = path
        self.pathstr = pathstr(path)


class MultipleChoice(Element):
    def __init__(self, question, path):
        super(MultipleChoice, self).__init__(question, path)
        self.options = question['children']


class Option(Element):
    pass


class SelectOne(MultipleChoice):
    pass


class SelectAllThatApply(MultipleChoice):
    pass


def count_submissions(submissions):
    results = {}
    # per-gender counts
    cols = ['facility', 'demographics_group/gender']
    question_table = submissions.loc[:, cols]
    gender_counts = question_table.groupby(
        ['demographics_group/gender']
    ).count()
    for gender in ['female', 'male']:
        results = deep_set(
            results,
            [gender],
            int(gender_counts.loc[gender])
        )

    # total count
    results = deep_set(
        results,
        ['total'],
        int(submissions.loc[:, ['facility']].count())
    )
    return results


def count_options(submissions, children, path=None, results=None):
    """
    returns nested dicts where the keys are the names of the XForm element
    branches to each question and each option of a question. Only multiple
    choice questions are supported.
    """
    path = path or []
    results = results or {}
    for child in children:
        deeper_path = path + [child['name']]
        if deeper_path in SKIP_QUESTIONS:
            pass
        elif child.get('type') == 'group' and child['name'] == 'meta':
            pass
        elif child.get('type') == 'group':
            results = count_options(submissions, child['children'], deeper_path, results)
        elif child.get('type') == 'select one':
            question = SelectOne(child, deeper_path)
            results = count_select_one(submissions, question, results)
        elif child.get('type') == 'select all that apply':
            question = SelectAllThatApply(child, deeper_path)
            results = count_select_all_that_apply(submissions, question, results)
        else:
            pass
    return results


def count_select_one(submissions, q, results):
    option_counts = count_select_one_options(submissions, q.path)
    results = deep_set(results, [q.pathstr, 'label'], q.label)
    for idx in range(len(q.options)):
        opt = Option(q.options[idx], q.path)
        results = deep_set(results, [q.pathstr, 'options', opt.name, 'label'], opt.label)
        results = deep_set(results, [q.pathstr, 'options', opt.name, 'idx'], idx)
        results = set_option_counts(q.path, opt.name, results, option_counts)
    return results


def count_select_all_that_apply(submissions, q, results):
    option_counts = count_select_one_options(submissions, q.path)
    results = deep_set(results, [q.pathstr, 'label'], q.label)
    for idx in range(len(q.options)):
        opt = Option(q.options[idx], q.path)
        results = deep_set(results, [q.pathstr, 'options', opt.name, 'label'], opt.label)
        results = deep_set(results, [q.pathstr, 'options', opt.name, 'idx'], idx)
        results = set_option_counts(q.path, opt.name, results, option_counts)
    return results


def count_select_one_options(site_submissions, path):
    cols = ['facility', 'demographics_group/gender', pathstr(path)]
    question_table = site_submissions.loc[:, cols]
    question_counts = question_table.groupby(
        ['demographics_group/gender', pathstr(path)]
    ).count()
    return question_counts


def count_select_all_that_apply_options():
    # df.loc[:,['facility', 'demographics_group/gender', 'visit_reason/emergency']].where((df['facility']=='folweni') & (df['visit_reason/pregnant'] == True)).groupby(['facility', 'demographics_group/gender']).count()
    pass


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

        results = deep_set(results, [pathstr(path), 'options', option_name, 'count', gender], val)
    return results


def pathstr(path):
    """ / separated path from array of strings"""
    return '/'.join(path)


def deep_set(deep_dict, path, value):
    key = path[0]
    if path[1:]:
        if key in deep_dict:
            deep_dict[key] = deep_set(deep_dict[key], path[1:], value)
        else:
            deep_dict[key] = deep_set({}, path[1:], value)
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
                deep_set(option, ['pct', gender], pct)
    return questions
