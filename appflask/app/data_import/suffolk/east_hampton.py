import re
from datetime import datetime
from pathlib import Path

import pandas as pd
import pdftotext

from app.data_import.suffolk.riverhead import make_output_path


def get_parcel_and_assessment(records):
    locked = False
    captured = {}
    result = []
    for record in records:
        parcel_re = re.search(r"\d{3}\.\d{3}-\d{4}-\d{3}\.\d{3}",
                              record)
        if locked:
            assessed_re = re.search(r'ITEM NO\s+\d+\.\d+\s+', record)
            if assessed_re:
                captured['assessed'] = record.split(assessed_re.group())[1].split(' ')[0]
                result.append(captured)
                locked = False
                captured = {}
        if parcel_re:
            # lock to extract assessed in the next loop
            captured['parcel'] = parcel_re.group()
            locked = True
            pass
    return pd.DataFrame(result)


def process_east_hampton_pdf(town_name, file_name):
    target_path = Path.cwd().parent / 'src' / 'suffolk' / town_name / f'{file_name}.pdf'

    with open(target_path, 'rb') as f:
        pdf = pdftotext.PDF(f)

    output_df = pd.DataFrame()
    page = 0
    for foo in pdf:
        records = foo.splitlines()
        result_df = get_parcel_and_assessment(records)

        date = re.search(r'\s[0-9]+\/[0-9]{2}\/[0-9]{4}\s',
                         records[-1]).group()
        # result_df['assessment_date'] = date.strip()
        month = datetime.strptime(date.strip(), '%m/%d/%Y').month

        if month > 4:
            result_df['assessment_type'] = 'final'
        else:
            result_df['assessment_type'] = 'tent'

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
    # process_east_hampton_pdf('Assessment Roll')
    # process_east_hampton_pdf('Assessment-Roll-4-26-2019')
    # process_east_hampton_pdf('Assessment Roll_2')
    process_east_hampton_pdf('Assessment Roll Final')
