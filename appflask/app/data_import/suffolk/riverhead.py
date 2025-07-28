import re
from pathlib import Path

import pandas as pd
import pdftotext


def get_parcel_and_assessment(records):
    locked = False
    captured = {}
    result = []
    count = 0
    for record in records:
        count += 1
        parcel_re = re.search(r'(?<=\*{20}\s)(\d+\..*\d)(?=\s\*)',
                              record)

        if captured.get('parcel') and locked:
            if record.find(captured.get('parcel')) != -1:
                count = 1
        if locked and count == 3:
            assessed = record[60:].strip().split(' ')[0]
            captured['assessed'] = assessed.strip()
            result.append(captured)
            locked = False
            captured = {}
            count = 0

        if parcel_re:
            # lock to extract assessed in the next loop
            captured['parcel'] = parcel_re.group()
            locked = True

    return pd.DataFrame(result)


def get_assessent_type(row):
    doo = row.split('A S S E S S M E N T   R O L L')[0]
    year_re = re.search(r'\s\d\s\d\s\d\s\d\s', doo)
    if year_re:
        assessment_type = doo.split(year_re.group())[1].strip()
        assessment_type_ = ''.join(assessment_type.split(' ')).lower()
        return 'final' if 'final' in assessment_type_ else 'tent'
    return 'undefined'


def make_output_path(town_name, file_name):
    output_folder = Path.cwd().parent / 'output' / 'suffolk' / town_name
    output_folder.mkdir(parents=True, exist_ok=True)
    return output_folder / f'{file_name}.csv'


def process_pdf(town_name, file_name):
    target_path = Path.cwd().parent / 'src' / 'suffolk' / town_name / f'{file_name}.pdf'

    with open(target_path, 'rb') as f:
        pdf = pdftotext.PDF(f)

    output_df = pd.DataFrame()
    page = 0
    for foo in pdf:
        if not foo:
            continue
        records = foo.splitlines()
        result_df = get_parcel_and_assessment(records)
        # date_row = records[1].split('VALUATION DATE-')
        result_df['assessment_type'] = get_assessent_type(records[0])
        # result_df['assessment_date'] = date_row[1] \
        #     if len(date_row) > 1 else None
        output_df = output_df.append(result_df,
                                     ignore_index=True,
                                     sort=False)
        page += 1
        if page == 100:
            break
        print(f'processing page...{page}')

    output_path = make_output_path(town_name, file_name)
    output_df.to_csv(output_path, index=None)


if __name__ == '__main__':
    process_pdf('riverhead',
                '2019-20FinalRollRevised09092019957085442091019AM')
