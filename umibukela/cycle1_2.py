import csv
import pandas as pd


def set_select_all_that_apply_columns(dict, q_key, possible_vals):
    for val in possible_vals:
        dict['/'.join([q_key, val])] = 'False'
    for val in dict[q_key].split(','):
        dict['/'.join([q_key, val])] = 'True'
    del dict[q_key]
    return dict


def run(columns, device_files, device_replacements, select_all_that_applies_columns):
    dicts = []

    # Read in each device file and do the per-device replacements
    for id, filename in device_files.iteritems():
        f = open('cycle1/' + filename)
        r = csv.DictReader(f, delimiter=',', quotechar='"')
        df = pd.DataFrame(list(r))
        df.columns = columns
        df.replace(to_replace=device_replacements[id], inplace=True)
        dicts += df.T.to_dict().values()

    df = pd.DataFrame(dicts)
    df.replace(to_replace=replacements_all, inplace=True)
    dicts = df.T.to_dict().values()
    for column, vals in select_all_that_applies_columns.iteritems():
        dicts = map(
            lambda x: set_select_all_that_apply_columns(x, column, vals),
            dicts
        )
    return dicts
