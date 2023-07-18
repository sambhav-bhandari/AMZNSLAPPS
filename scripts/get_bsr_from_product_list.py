import pandas as pd
import re

def extract_categories(row):
    lines =  str(row['Sales Rank']).split('\n')
    for i, line in enumerate(lines):
        match = re.search(r'(\d+)in\s(.+)', line)
        if match:
            row[f'Category {i} Sales Rank'] = int(match.group(1))
            row[f'Category {i}'] = match.group(2)
    return row

def get_bsr(df, date):
    df = df.apply(extract_categories, axis=1)
    df = df[
        [
            'ASIN',
            'Account Title',
            'Market Place',
            'Active',
            'Category 0',
            'Category 0 Sales Rank',
            'Category 1',
            'Category 1 Sales Rank',
            'Category 2',
            'Category 2 Sales Rank',
            'Category 3',
            'Category 3 Sales Rank',
            'Currency',
            'Price',
            'Sales Rank',
            'Title'
            ]
        ]
    df = df.sort_values(by=['Account Title', 'Category 0 Sales Rank'])
    df['Date'] = date
    return df