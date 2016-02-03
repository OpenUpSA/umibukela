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

from logging import getLogger


# These are used for grouping. Trying to count them and group by them
# at the same time doesn't work.
SKIP_QUESTIONS = [['_uuid'], ['demographics_group', 'gender']]
GENDER_COLUMN = 'demographics_group/gender'

log = getLogger(__name__)


class Element(object):
    def __init__(self, element, path):
        self.label = element['label']
        self.name = element['name']
        self.path = path + [element['name']]
        self.pathstr = pathstr(self.path)

    def __str__(self):
        return "%s %s" % (self.__class__, self.pathstr)


class MultipleChoice(Element):
    def __init__(self, question, path, group_labels):
        super(MultipleChoice, self).__init__(question, path)
        self.options = [Option(o, self.path) for o in question['children']]
        self.group_labels = group_labels


class Option(Element):
    pass


class SelectOne(MultipleChoice):
    pass


class SelectAllThatApply(MultipleChoice):
    pass


def count_submissions(submissions):
    results = {}
    # per-gender counts
    cols = ['_uuid', GENDER_COLUMN]
    question_table = submissions.loc[:, cols]
    gender_counts = question_table.groupby(
        [GENDER_COLUMN]
    ).count()
    results['female'] = int(gender_counts.loc['female'])
    results['male'] = int(gender_counts.loc['male'])
    results['total'] = int(submissions.loc[:, ['_uuid']].count())

    return results


def count_options(submissions, children, path=None, group_labels=None, results=None):
    """
    returns nested dicts where the keys are the names of the XForm element
    branches to each question and each option of a question. Only multiple
    choice questions are supported.
    """
    path = path or []  # list of names in structure leading to current element
    group_labels = group_labels or []  # list of labels in groups in path
    results = results or {}  # results nested dict under construction
    for child in children:
        deeper_path = path + [child['name']]
        if deeper_path in SKIP_QUESTIONS:
            pass
        elif child.get('type') == 'group' and child['name'] == 'meta':
            pass
        elif child.get('type') == 'group':
            deeper_group_labels = group_labels + [child['label']]
            results = count_options(submissions, child['children'],
                                    deeper_path, deeper_group_labels, results)
        elif child.get('type') == 'select one':
            question = SelectOne(child, path, group_labels)
            results = count_select_one(submissions, question, results)
        elif child.get('type') == 'select all that apply':
            question = SelectAllThatApply(child, path, group_labels)
            results = count_select_all_that_apply(submissions, question, results)
        else:
            pass
    return results


def count_select_one(submissions, q, results):
    option_counts = count_select_one_options(submissions, q.path)
    results = deep_set(results, [q.pathstr, 'label'], q.label)
    results = deep_set(results, [q.pathstr, 'group_labels'], q.group_labels)
    for idx in range(len(q.options)):
        opt = q.options[idx]
        results = deep_set(results, [q.pathstr, 'options', opt.name, 'label'], opt.label)
        results = deep_set(results, [q.pathstr, 'options', opt.name, 'idx'], idx)
        results = set_select_one_option_counts(q.path, opt.name, results, option_counts)
    return results


def count_select_all_that_apply(submissions, q, results):
    results = deep_set(results, [q.pathstr, 'label'], q.label)
    results = deep_set(results, [q.pathstr, 'group_labels'], q.group_labels)
    for idx in range(len(q.options)):
        opt = q.options[idx]
        option_counts = count_select_all_that_apply_options(submissions, opt.path)
        results = deep_set(results, [q.pathstr, 'options', opt.name, 'label'], opt.label)
        results = deep_set(results, [q.pathstr, 'options', opt.name, 'idx'], idx)
        results = set_select_all_that_apply_option_counts(q.path, opt.name, results, option_counts)
    return results


def count_select_one_options(submissions, questionpath):
    cols = ['_uuid', GENDER_COLUMN, pathstr(questionpath)]
    question_table = submissions.loc[:, cols]
    question_counts = question_table.groupby(
        [GENDER_COLUMN, pathstr(questionpath)]
    ).count()
    return question_counts


def count_select_all_that_apply_options(submissions, optionpath):
    option_col = pathstr(optionpath)
    cols = [GENDER_COLUMN, option_col]
    option_table = submissions.loc[:, cols]
    option_chosen_table = option_table.where(submissions[option_col] == 'True')
    option_counts = option_chosen_table.groupby([GENDER_COLUMN]).count()
    return option_counts


def set_select_all_that_apply_option_counts(path, option_name, results, option_table):
    for gender in ['male', 'female']:
        val = int(option_table.loc[gender])
        results = deep_set(results, [pathstr(path), 'options', option_name, 'count', gender], val)
    return results


def set_select_one_option_counts(path, option_name, results, option_table):
    for gender in ['male', 'female']:
        try:
            val = int(option_table.loc[gender, option_name])
        except KeyError:
            # values that aren't counted because they don't occur in the
            # results for this question won't be indexes in the counts
            log.debug("Question %s option %s %s not found in counts DataFrame %s",
                      pathstr(path), gender, option_name, option_table)
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
