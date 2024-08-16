import pandas as pd
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None
import datetime
import numpy as np
import schemdraw
from schemdraw.flow import *

def read_files(dart=None):
    # read sheets of excel files
    practice_df = pd.read_excel('train_data.xlsx',sheet_name='practice')
    game_df = pd.read_excel('train_data.xlsx',sheet_name='games')
    target_df = pd.read_excel('train_data.xlsx',sheet_name='targets')

    if dart!=None:
        practice_df = practice_df[practice_df['Dart']==dart].copy()
        game_df = game_df[game_df['Dart']==dart].copy()


    return practice_df, game_df, target_df

def create_dfs(practice_df, game_df, rolling_practice=0, rolling_game=20):
    # uses training data to create data frames for each KPI - using the user-defined rolling windows

    # create triple dataframe
    trip_df = practice_df[practice_df['Type']=='Triple']
    # triples
    trip_df['trip_pct'] = trip_df['Triples']/trip_df['Darts']
    trip_df['trip_r'] = trip_df['trip_pct'].rolling(rolling_practice).mean()
    # trip singles
    trip_df['trip_single_pct'] = (trip_df['Hits']-trip_df['Triples'])/trip_df['Darts']
    trip_df['trip_single_r'] = trip_df['trip_single_pct'].rolling(rolling_practice).mean()
    # trip miss
    trip_df['trip_miss_pct'] = (trip_df['Darts']-trip_df['Hits'])/trip_df['Darts']
    trip_df['trip_miss_r'] = trip_df['trip_miss_pct'].rolling(rolling_practice).mean()
    # uncapped MPR
    trip_df['uncapped_mpr'] = (trip_df['trip_pct']*3+trip_df['trip_single_pct'])*3
    trip_df['uncapped_mpr_r'] = trip_df['uncapped_mpr'].rolling(rolling_practice).mean()

    # create single dataframe
    single_df = practice_df[practice_df['Type']=='Single'].copy()
    # singles
    single_df['single_pct'] = single_df['Hits']/single_df['Darts']
    single_df['single_r'] = single_df['single_pct'].rolling(rolling_practice).mean()

    # create bull dataframe
    bull_df = practice_df[practice_df['Type']=='Bull'].copy()
    # singles
    bull_df['bull_pct'] = bull_df['Hits']/bull_df['Darts']
    bull_df['bull_r'] = bull_df['bull_pct'].rolling(rolling_practice).mean()

    # create double dataframe
    double_df = practice_df[practice_df['Type']=='Double'].copy()
    # singles
    double_df['double_pct'] = double_df['Hits']/double_df['Darts']
    double_df['double_r'] = double_df['double_pct'].rolling(rolling_practice).mean()

    # create minn dataframe
    minn_df = practice_df[practice_df['Activity']=='Minn']
    minn_df['minn_r'] = minn_df['Darts'].rolling(rolling_practice).mean()

    # create cricket dataframe
    cricket_game_df = game_df[game_df['Game']=='Cricket']
    # calculate MPR
    cricket_game_df['mpr_r'] = cricket_game_df['MPR'].rolling(rolling_game).mean()
    # calculate first 9 MPR
    cricket_game_df['first_9_mpr_r'] = cricket_game_df['First 9 MPR'].rolling(rolling_game).mean()
    # daily df
    cricket_day_df = cricket_game_df.groupby('Date').agg({'mpr_r':'last','first_9_mpr_r':'last'}).reset_index()

    # create 501 dataframe
    x01_game_df = game_df[game_df['Game']==501]
    # calculate PPR
    x01_game_df['ppr_r'] = x01_game_df['PPR'].rolling(rolling_game).mean()
    # calculate first 9 PPR
    x01_game_df['first_9_ppr_r'] = x01_game_df['First 9 PPR'].rolling(rolling_game).mean()
    # daily df
    x01_day_df = x01_game_df.groupby('Date').agg({'ppr_r':'last','first_9_ppr_r':'last'}).reset_index()

    return trip_df, single_df, bull_df, double_df, minn_df, cricket_day_df, x01_day_df

def build_daily_df(target_df, trip_df, single_df, bull_df, double_df, minn_df, cricket_day_df, x01_day_df, start_date, end_date):
    # build a daily dataframe that tracks performance on all KPIs as of each daily snapshot

    datelist = pd.date_range(start_date,end_date-datetime.timedelta(days=1),freq='d')

    daily_df = pd.DataFrame({'Date':datelist})

    # add targets
    for column in target_df.columns:
        daily_df[column] = target_df[column].values[0]

    # add actuals
    daily_df = pd.merge(daily_df,trip_df[['Date','trip_r','trip_single_r','trip_miss_r','uncapped_mpr_r']],how='left',on='Date')
    daily_df = pd.merge(daily_df,single_df[['Date','single_r']],how='left',on='Date')
    daily_df = pd.merge(daily_df,bull_df[['Date','bull_r']],how='left',on='Date')
    daily_df = pd.merge(daily_df,double_df[['Date','double_r']],how='left',on='Date')
    daily_df = pd.merge(daily_df,minn_df[['Date','minn_r']],how='left',on='Date')
    daily_df = pd.merge(daily_df,cricket_day_df[['Date','mpr_r','first_9_mpr_r']],how='left',on='Date')
    daily_df = pd.merge(daily_df,x01_day_df[['Date','ppr_r','first_9_ppr_r']],how='left',on='Date')

    # fill na values with forward fill (except for days prior to first value, which are backfilled)
    for column in daily_df.columns:
        daily_df[column] = daily_df[column].fillna(method='ffill').fillna(method='bfill')

    return daily_df

def calculate_progress(daily_df):
    # calculate KPI ratios (X% to goal)
    daily_df['01. MPR'] = daily_df['mpr_r']/daily_df['MPR']
    daily_df['02. First 9 MPR'] = daily_df['first_9_mpr_r']/daily_df['First 9 MPR']
    daily_df['03. Bull'] = daily_df['bull_r']/daily_df['Bull']
    daily_df['04. Uncapped MPR'] = daily_df['uncapped_mpr_r']/daily_df['Uncap MPR']
    daily_df['05. Single'] = daily_df['single_r']/daily_df['Single']
    daily_df['06. Triple'] = daily_df['trip_r']/daily_df['Triple']
    daily_df['07. Triple Single'] = daily_df['trip_single_r']/daily_df['Trip Single']
    daily_df['08. Triple Miss'] = daily_df['Trip Miss']/daily_df['trip_miss_r'] # reversed since lower value is better
    daily_df['09. PPR'] = daily_df['ppr_r']/daily_df['PPR']
    daily_df['10. First 9 PPR'] = daily_df['first_9_ppr_r']/daily_df['First 9 PPR']
    daily_df['11. Double'] = daily_df['double_r']/daily_df['Double']
    daily_df['12. Minn'] = daily_df['Minn']/daily_df['minn_r'] # reversed since lower value is better

    return daily_df

def get_daily_kpi_dfs(daily_df,start_date,end_date):
    # calculates daily snapshot of which KPI was the best/worst

    datelist = pd.date_range(start_date,end_date-datetime.timedelta(days=1),freq='d')

    min_kpi_df = pd.DataFrame({'Date':datelist})
    max_kpi_df = pd.DataFrame({'Date':datelist})

    # add targets
    for column in daily_df.iloc[:,25:].columns:
        min_kpi_df[column] = np.nan
        max_kpi_df[column] = np.nan

    for i in range(len(daily_df)):
        min_val = daily_df.iloc[i,25:].min()
        max_val = daily_df.iloc[i,25:].max()
        daily_min_kpi = daily_df.iloc[i,25:][daily_df.iloc[i,25:]==min_val].index.values[0]
        daily_max_kpi = daily_df.iloc[i,25:][daily_df.iloc[i,25:]==max_val].index.values[0]
        min_kpi_df[daily_min_kpi].iloc[i] = min_val
        max_kpi_df[daily_max_kpi].iloc[i] = max_val

    return min_kpi_df, max_kpi_df
