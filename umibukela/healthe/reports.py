from __future__ import division

from csv import DictWriter
from copy import copy
import os.path
from cStringIO import StringIO
from collections import Counter
from itertools import groupby

from xlsxwriter.workbook import Workbook
import requests
from django.conf import settings

from umibukela.healthe.utils import MEDS, PROVINCES, DISTRICTS


HEADINGS_WHITE = ['Date', 'Province', 'District', 'Clinic Name', 'Clinic Contact', 'Latitute', 'Longitude', 'Monitor Name', 'Medicine Name', ]
HEADINGS_GREEN = ['In Stock?', ]
HEADINGS_BLUE = ['No Stock - Not used at PHC', 'No Stock - Ordered per Patient', 'No Stock - Ordered at Depot', 'No Stock - Ordered per patient, ordered at Depot', ]
HEADINGS_ORANGE = ['No Stock - Order Date', 'No Stock - Depot out of Stock']


def write_rows(fname, rows, fields=None):
    print "Writing %s" % fname
    if fields is None:
        fields = sorted(set(k for r in rows for k in r.keys()))

    with open(fname, 'w') as f:
        writer = DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def decorate(rows):
    for r in rows:
        # fold in clinic name
        if r['facility_details/facility'] == 'other':
            r['facility_details/facility'] = r['facility_details/facility_other']

        # province
        r['facility_details/province'] += ' - ' + PROVINCES[r['facility_details/province']]
        r['facility_details/district'] += ' - ' + DISTRICTS[r['facility_details/district']]

        r['date'] = r['end'].split('T', 2)[0]


def generate_report(rows):
    decorate(rows)

    fields = ['date', 'facility_details/province', 'facility_details/district', 'facility_details/facility',
              'facility_details/contact', 'basics/_gps_latitude', 'basics/_gps_longitude', 'basics/monitor',
              'medicine', 'in_stock', 'no stock - not_used_phc', 'no stock - per_patient', 'no stock - depot_order',
              'no stock - per_patient_depot_order', 'date_ordered']

    output = [{f: r.get(f) for f in fields} for r in rows]
    return output, fields


def process_survey(rows):
    result = []

    for r in rows:
        template = copy(r)

        # recognise medicine codes
        meds = [k.split('/')[0] for k in template.keys() if k.endswith('-in_stock')]

        # remove medicines from template
        for code in meds:
            for k in template.keys():
                # eg. aba/aba-in_stock
                if k.startswith(code + '/'):
                    del template[k]

        # flatten values that are arrays
        for key in template.iterkeys():
            val = template[key]
            if isinstance(val, list):
                template[key] = '; '.join(str(v) for v in val)

        # transfrom medicine results from columns into rows
        for code, name in MEDS.iteritems():
            # not all submissions have all the same medicines
            if code not in meds:
                continue

            row = copy(template)
            row['medicine'] = name

            for k, v in r.iteritems():
                if k.startswith(code + '/'):
                    # eg. aba/aba-in_stock - > in_stock
                    after = k[len(code) * 2 + 2:]
                    row[after] = v

            # add extra columns for stockout details
            if row['in_stock'] != 'yes':
                row['no stock - %s' % row['stockout_reason']] = 'yes'

            result.append(row)

    return result


def build_xlsx(period_rows, report_rows, report_fields):
    """
    See http://stackoverflow.com/questions/32205927/xlsxwriter-and-libreoffice-not-showing-formulas-result
    """
    output = StringIO()
    workbook = Workbook(output)
    heading = workbook.add_format({
        'bold': True,
        'bottom': 1,
        'text_wrap': True,
        'font_name': 'Arial',
        'font_size': 10,
    })
    count = workbook.add_format({
        'bold': True,
        'top': 1,
        'font_name': 'Arial',
        'font_size': 10,
    })
    percent = workbook.add_format({
        'bold': True,
        'num_format': '0%',
        'font_name': 'Arial',
        'font_size': 10,
    })
    common = workbook.add_format({
        'font_name': 'Arial',
        'font_size': 10,
    })
    heading_green = workbook.add_format({
        'bold': True,
        'bottom': 1,
        'text_wrap': True,
        'font_name': 'Arial',
        'bg_color': 'b6d7a8',
        'font_size': 10,
    })
    heading_blue = workbook.add_format({
        'bold': True,
        'bottom': 1,
        'text_wrap': True,
        'font_name': 'Arial',
        'bg_color': '9fc5e8',
        'font_size': 10,
    })
    heading_orange = workbook.add_format({
        'bold': True,
        'bottom': 1,
        'text_wrap': True,
        'font_name': 'Arial',
        'bg_color': 'f9cb9c',
        'font_size': 10,
    })

    report_sheet = workbook.add_worksheet('Report')
    data_sheet = workbook.add_worksheet('Data')

    # Column headings
    offset = 0
    for c, label in enumerate(HEADINGS_WHITE):
        report_sheet.write(0, offset + c, label, heading)
    offset += len(HEADINGS_WHITE)
    for c, label in enumerate(HEADINGS_GREEN):
        report_sheet.write(0, offset + c, label, heading_green)
    offset += len(HEADINGS_GREEN)
    for c, label in enumerate(HEADINGS_BLUE):
        report_sheet.write(0, offset + c, label, heading_blue)
    offset += len(HEADINGS_BLUE)
    for c, label in enumerate(HEADINGS_ORANGE):
        report_sheet.write(0, offset + c, label, heading_orange)
    # adjust widths and height
    report_sheet.set_row(0, 65)
    report_sheet.set_column('A:B', 13)
    report_sheet.set_column('C:D', 25)
    report_sheet.set_column('E:E', 20)
    report_sheet.set_column('F:G', 11)
    report_sheet.set_column('H:H', 20)
    report_sheet.set_column('I:I', 80)
    report_sheet.set_column('J:P', 15)

    # Freeze first row
    report_sheet.freeze_panes(1, 0)

    # Worsheet data
    for r, row in enumerate(report_rows, 1):
        for key, val in row.iteritems():
            report_sheet.write(r, report_fields.index(key), val, common)
    # Data copy
    data_fields = sorted(set(k for r in period_rows for k in r.keys()))
    for col, field_name in enumerate(data_fields):
        data_sheet.write(0, col, field_name, common)
    for r, row in enumerate(period_rows, 1):
        for key, val in row.iteritems():
            data_sheet.write(r, data_fields.index(key), val, common)

    # Totals
    total_row0 = len(report_rows) + 1
    formula = '=COUNTA('+colalpha(8)+'2:'+colalpha(8)+str(len(report_rows))+')'
    report_sheet.write_formula(total_row0, 8, formula, count)
    for col in range(9, 14):
        yes_count_cell(report_sheet, len(report_rows), total_row0, col, count)
    yes_count_cell(report_sheet, len(report_rows), total_row0, 15, count)
    formula = '='+colalpha(9)+str(total_row0+1)+'/'+colalpha(8)+str(total_row0+1)
    report_sheet.write_formula(total_row0+1, 9, formula, percent)

    workbook.close()
    output.seek(0)
    return output.read()


def yes_count_cell(sheet, rows, row, col, cellformat):
    formula = '=COUNTIF('+colalpha(col)+'2:'+colalpha(col)+str(rows)+', "=yes")'
    sheet.write_formula(row, col, formula, cellformat)


def colalpha(n):
    return chr(n + ord('a'))


def make_fname(fname, suffix, ext=None):
    base, current_ext = os.path.splitext(fname)
    ext = ext or current_ext
    return ''.join([base, '-', suffix, ext])


def get_submissions(start_date, end_date, fmt=None):
    """ Load the raw submissions for this date range.
    """
    fmt = fmt or 'json'
    filters = '{"$and": [{"_submission_time": {"$gte": "%sT00:00:00Z"}}, {"_submission_time": {"$lte": "%sT23:59:59Z"}}]}' % (
        start_date.isoformat(),
        end_date.isoformat())

    resp = requests.get('https://kc.kobotoolbox.org/api/v1/data/25889', params={
        'format': fmt,
        'query': filters,
    }, auth=(settings.KOBO_USERNAME, settings.KOBO_PASSWORD))
    resp.raise_for_status()

    if fmt == 'json':
        return resp.json()
    else:
        return resp.content


def build_stockout_xlsx(start_date, end_date):
    """ Grab the data for this report and return a string
    with the raw XLSX data in it.
    """
    rows = get_submissions(start_date, end_date, 'json')
    period_rows = process_survey(rows)

    report_rows, fields = generate_report(period_rows)
    return build_xlsx(period_rows, report_rows, fields)


def summary_stats(rows):
    # count of stockouts by medicine
    stockings = [(k.split("/")[0], r[k] == u'yes') for r in rows for k in r if k.endswith('-in_stock')]
    instock = Counter([m[0] for m in stockings if m[1]])
    stockouts = Counter([m[0] for m in stockings if not m[1]])

    def yearmonth(row):
        # YYYY-MM[-DD]
        return row['today'][:7]

    # availability by month
    by_month = {}
    for month, group in groupby(sorted(rows, key=yearmonth), yearmonth):
        group = list(group)
        n_instock = sum(1 for r in group for k in r if k.endswith('-in_stock') and r[k] == u'yes')
        n_outstock = sum(1 for r in group for k in r if k.endswith('-in_stock') and r[k] == u'no')
        by_month[month] = n_instock / (n_instock + n_outstock) * 100

    return {
        'medicine_stockouts': dict(stockouts),
        'medicine_instock': dict(instock),
        'monthly_availability': by_month,
    }


def stockout_stats(rows):
    def facility(row):
        if row['facility_details/facility'] == u'other':
            return row['facility_details/facility_other']
        else:
            return row['facility_details/facility']

    # count facilities
    info = {
        'total_clinics': len(set(facility(r) for r in rows)),
        'country_stats': summary_stats(rows),
        'provinces': [],
        'medicines': MEDS,
    }

    # provinces
    provinces = set(r['facility_details/province'] for r in rows)
    for code in provinces:
        info['provinces'].append({
            'code': code,
            'name': PROVINCES[code],
            'stats': summary_stats([r for r in rows if r['facility_details/province'] == code]),
        })

    return info
