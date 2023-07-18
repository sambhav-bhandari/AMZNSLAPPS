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
    category_cols = [col for col in df.columns if col.startswith('Category')]
    select_cols = [
        'ASIN',
        'Account Title',
        'Market Place',
        'Active',
        *category_cols,
        'Currency',
        'Price',
        'Sales Rank',
        'Title',
    ]
    df = df[select_cols]
    df = df.sort_values(by=['Account Title', 'Category 0 Sales Rank'])
    df['Date'] = date
    return df