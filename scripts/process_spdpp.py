import pandas as pd
import numpy as np

columns_agg = {
     'Is Parent':'last',
     'Internal Name':'last',
     'Tags':'last',
     'Active':'last',
     'Orders':'sum',
     'Canceled Orders':'sum',
     'Units':'sum',
     'Shipped':'sum',
     'Refunded':'sum',
     'Refund %':'sum',
     'Promo Units':'sum',
     'Non Promo Units':'sum',
     'Promo Revenue':'sum',
     'Non Promo Revenue':'sum',
     'Ordered Product Sales':'sum',
     'Customer Pays':'sum',
     'Revenue':'sum',
     'Per Unit Revenue':'sum',
     'FBA Fees':'sum',
     'Commissions':'sum',
     'Promo Amount':'sum',
     'COGS':'sum',
     'Shipping Cost':'sum',
     'Miscellaneous Cost':'sum',
     'OOE':'sum',
     'Internal Tax/VAT':'sum',
     'Remitting Tax':'sum',
     'Net Profit':'sum',
     'Net Margin':'sum',
     'Net ROI':'sum',
     'PPC Orders':'sum',
     'PPC Impressions':'sum',
     'PPC Clicks':'sum',
     'PPC Sales':'sum',
     'PPC Cost':'sum',
     'PPC Conv':'sum',
     'Page Views':'sum',
     'Sessions':'sum',
     'Unit Session %':'sum',
     'PPC Product Sales':'sum',
     'PPC Product Cost':'sum',
     'PPC Product Clicks':'sum',
     'PPC Product Impressions':'sum',
     'PPC Video Sales':'sum',
     'PPC Video Cost':'sum',
     'PPC Video Clicks':'sum',
     'PPC Video Impressions':'sum',
}

def aggregate(df, include_sku=False):
    groupby = ['YearMonth','Account Title','Market Place','ASIN']
    if include_sku:
        groupby.append('SKU')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['YearMonth'] = df['Date'].map(lambda dt: dt.replace(day=1))
    groupedDF = df.groupby(groupby).agg(columns_agg).reset_index()
    groupedDF['Refund %'] = groupedDF['Refunded']/groupedDF['Orders']
    groupedDF['Per Unit Revenue'] = groupedDF['Revenue']/groupedDF['Units']
    groupedDF['Net Margin'] = groupedDF['Net Profit']/groupedDF['Revenue']
    groupedDF['PPC Conv'] = groupedDF['PPC Orders']/groupedDF['PPC Clicks']
    groupedDF['Unit Session %'] = groupedDF['Orders']/groupedDF['Sessions']
    groupedDF = groupedDF.replace([np.inf, -np.inf], np.nan)
    groupedDF = groupedDF.rename(columns={'YearMonth': 'Date'})
    return groupedDF

def aggregate2(df, include_sku=False):
    groupby = ['YearMonth','Account Title','Market Place','ASIN']
    if include_sku:
        groupby.append('SKU')
    df['Date'] = pd.to_datetime(df['Date'])
    df['YearMonth'] = df['Date'].map(lambda dt: dt.replace(day=1))
    groupedDF = df.groupby(groupby).agg(columns_agg).reset_index()
    groupedDF['Refund %'] = groupedDF['Refunded']/groupedDF['Orders']
    groupedDF['Per Unit Revenue'] = groupedDF['Revenue']/groupedDF['Units']
    groupedDF['Net Margin'] = groupedDF['Net Profit']/groupedDF['Revenue']
    groupedDF['PPC Conv'] = groupedDF['PPC Orders']/groupedDF['PPC Clicks']
    groupedDF['Unit Session %'] = groupedDF['Orders']/groupedDF['Sessions']
    groupedDF = groupedDF.replace([np.inf, -np.inf], np.nan)
    groupedDF = groupedDF.rename(columns={'YearMonth': 'Date'})
    return groupedDF


def filter(df, colname='Market Place', values=['US']):
    df = df[df[colname].isin(values)]
    return df

def split_by_brand(df):
    df['Brand'] = df['Account Title'].apply(lambda account_title: account_title.split(' (')[0])
    brands = df['Brand'].unique().tolist()

    dfs = []
    for brand in brands:
        brand_df = df[df['Brand'] == brand]
        dfs.append((brand, brand_df))
    return dfs