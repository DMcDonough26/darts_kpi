import pandas as pd
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None
import datetime
import numpy as np
import schemdraw
from schemdraw.flow import *


def plot_cricket_1(daily_df, rolling_practice, rolling_game):
    # MPR
    fig, ax = plt.subplots(figsize=(20,5))

    ax.plot('Date','MPR',data=daily_df,ls='--')
    ax.plot('Date','mpr_r',data=daily_df[daily_df['mpr_r'].isna()==False],ls='--')
    ax.set_title('Target MPR vs. Actual from Practice Games (Rolling '+str(rolling_game)+')')
    ax.set_ylim([1.5,3.5])
    ax.legend(['Target','Actual'])

    plt.show()

def plot_cricket_2(daily_df, rolling_practice, rolling_game):
    # First 9 MPR and Bull
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20,5))

    ax1.plot('Date','Uncap MPR',data=daily_df,ls='--')
    ax1.plot('Date','first_9_mpr_r',data=daily_df[daily_df['first_9_mpr_r'].isna()==False],ls='--')
    ax1.set_ylim([1.8,4])
    ax1.set_title('Target Uncapped MPR vs. Actual First 9 MPR from Practice Games (Rolling '+str(rolling_game)+')')

    ax2.plot('Date','Bull',data=daily_df,ls='--')
    ax2.plot('Date','bull_r',data=daily_df[daily_df['bull_r'].isna()==False],ls='--')
    ax2.set_ylim([.18,.40])
    ax2.set_title('Target Bull% vs. Actual from Practice (Rolling '+str(rolling_practice)+')')

    plt.show()

def plot_cricket_3(daily_df, rolling_practice, rolling_game):
    # Uncapped MPR and Single
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20,5))

    ax1.plot('Date','Uncap MPR',data=daily_df,ls='--')
    ax1.plot('Date','uncapped_mpr_r',data=daily_df[daily_df['uncapped_mpr_r'].isna()==False],ls='--')
    ax1.set_ylim([1.8,4])
    ax1.set_title('Target Uncapped MPR vs. Actual from Practice (Rolling '+str(rolling_practice)+')')

    ax2.plot('Date','Single',data=daily_df,ls='--')
    ax2.plot('Date','single_r',data=daily_df[daily_df['single_r'].isna()==False],ls='--')
    ax2.set_ylim([.40,.80])
    ax2.set_title('Target Single% vs. Actual from Practice (Rolling '+str(rolling_practice)+')')

    plt.show()

def plot_cricket_4(daily_df, rolling_practice, rolling_game):
    # Triple Outcomes
    fig, axs = plt.subplots(2,2,figsize=(20,10))

    axs[0][0].plot('Date','Triple',data=daily_df,ls='--')
    axs[0][0].plot('Date','trip_r',data=daily_df[daily_df['trip_r'].isna()==False],ls='--')
    axs[0][0].set_ylim([.06,.25])
    axs[0][0].set_title('Target Triple% vs. Actual from Practice (Rolling '+str(rolling_practice)+')')

    axs[0][1].plot('Date','Trip Single',data=daily_df,ls='--')
    axs[0][1].plot('Date','trip_single_r',data=daily_df[daily_df['trip_single_r'].isna()==False],ls='--')
    axs[0][1].set_ylim([.40,.60])
    axs[0][1].set_title('Target Trip Single% vs. Actual from Practice (Rolling '+str(rolling_practice)+')')

    axs[1][0].plot('Date','Trip Miss',data=daily_df,ls='--')
    axs[1][0].plot('Date','trip_miss_r',data=daily_df[daily_df['trip_miss_r'].isna()==False],ls='--')
    axs[1][0].set_ylim([.30,.50])
    axs[1][0].set_title('Target Trip Miss% vs. Actual from Practice (Rolling '+str(rolling_practice)+')')

    plt.show()


def plot_x01_1(daily_df, rolling_practice, rolling_game):
    # PPR
    fig, ax = plt.subplots(figsize=(20,5))

    ax.plot('Date','PPR',data=daily_df,ls='--')
    ax.plot('Date','ppr_r',data=daily_df[daily_df['ppr_r'].isna()==False],ls='--')
    ax.set_ylim([35,70])
    ax.set_title('Target PPR vs. Actual from Practice Games (Rolling '+str(rolling_game)+')')

    plt.show()

def plot_x01_2(daily_df, rolling_practice, rolling_game):
    # First 9 PPR and Double
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(20,5))

    ax1.plot('Date','First 9 PPR',data=daily_df,ls='--')
    ax1.plot('Date','first_9_ppr_r',data=daily_df[daily_df['first_9_ppr_r'].isna()==False],ls='--')
    ax1.set_ylim([40,80])
    ax1.set_title('Target First 9 PPR vs. Actual First 9 PPR from Practice Games (Rolling '+str(rolling_game)+')')

    ax2.plot('Date','Double',data=daily_df,ls='--')
    ax2.plot('Date','double_r',data=daily_df[daily_df['double_r'].isna()==False],ls='--')
    ax2.set_ylim([.08,.25])
    ax2.set_title('Target Double% vs. Actual from Practice (Rolling '+str(rolling_practice)+')')

    plt.show()

def plot_x01_3(daily_df, rolling_practice, rolling_game):
    # Triple Outcomes

    fig, axs = plt.subplots(2,2,figsize=(20,8))

    axs[0][0].plot('Date','Uncap MPR',data=daily_df,ls='--')
    axs[0][0].plot('Date','uncapped_mpr_r',data=daily_df[daily_df['uncapped_mpr_r'].isna()==False],ls='--')
    axs[0][0].set_ylim([1.8,4])
    axs[0][0].set_title('Target Uncapped MPR vs. Actual from Practice (Rolling '+str(rolling_practice)+')')

    target = 19

    # target points from trips
    axs[0][1].plot(daily_df['Date'],daily_df['Triple']*9*target*3,ls='--')
    axs[0][1].plot(daily_df[daily_df['trip_r'].isna()==False]['Date'],daily_df[daily_df['trip_r'].isna()==False]['trip_r']*9*target*3,ls='--')
    axs[0][1].set_ylim([target,target*3*3])
    axs[0][1].set_title('Target Triple Points per Target vs. Inferred from Practice (Rolling '+str(rolling_practice)+')')

    # target points from single
    axs[1][0].plot(daily_df['Date'],daily_df['Single']*9*target,ls='--')
    axs[1][0].plot(daily_df[daily_df['single_r'].isna()==False]['Date'],daily_df[daily_df['single_r'].isna()==False]['single_r']*9*target,ls='--')
    axs[1][0].set_ylim([50,150])
    axs[1][0].set_title('Target Single Points per Target vs. Inferred from Practice (Rolling '+str(rolling_practice)+')')

    # target points from miss
    axs[1][1].plot(daily_df['Date'],(daily_df['First 9 PPR']*3) - (daily_df['Triple']*9*target*3) - (daily_df['Single']*9*target),ls='--')
    axs[1][1].plot(daily_df['Date'],(daily_df['first_9_ppr_r'].fillna(method='ffill').fillna(method='bfill')*3) -\
    (daily_df['trip_r'].fillna(method='ffill').fillna(method='bfill')*9*target*3) -\
    (daily_df['single_r'].fillna(method='ffill').fillna(method='bfill')*9*target),ls='--')
    axs[1][1].set_ylim([0,50])
    axs[1][1].set_title('Target Miss Points per Target vs. Inferred from Practice (Rolling '+str(rolling_practice)+')')

    plt.show()

def plot_min_daily(min_kpi_df):
    # Daily Worst plot
    fig, ax = plt.subplots(figsize=(20,5))

    for column in min_kpi_df.columns[1:]:
        if min_kpi_df[column].sum() >0:
            # ax.scatter('Date',column,data=min_kpi_df)
            ax.plot('Date',column,data=min_kpi_df,ls='--')

    ax.legend()
    ax.set_ylim([0.4,1.2])
    ax.set_title('Lowest KPI and Value by Day')

    plt.show()

def plot_max_daily(max_kpi_df):
    # Daily Best plot
    fig, ax = plt.subplots(figsize=(20,5))

    for column in max_kpi_df.columns[1:]:
        if max_kpi_df[column].sum() >0:
            # ax.scatter('Date',column,data=max_kpi_df)
            ax.plot('Date',column,data=max_kpi_df,ls='--')

    ax.legend()
    ax.set_ylim([0.4,1.2])
    ax.set_title('Highest KPI and Value by Day')

    plt.show()


def kpi_values(daily_df,target,actual,order,percent):
    tar = daily_df.iloc[-1:,:][target].values[0]
    if actual in ['minn_r','ppr_r','first_9_ppr_r']:
        act = int(daily_df.iloc[-1:,:][actual].values[0].round(0))
    elif percent == True:
        act = daily_df.iloc[-1:,:][actual].values[0].round(2)
    else:
        act = daily_df.iloc[-1:,:][actual].values[0].round(1)
    if order == True:
        kpi = round(act/tar*100)
    else:
        kpi = round(tar/act*100)
    if percent == True:
        text = str(target)+'\nTarget: '+str(int(tar*100))+'%\nActual: '+str(int(act*100))+'%\n'+str(kpi)+'%'
    else:
        text = str(target)+'\nTarget: '+str(tar)+'\nActual: '+str(act)+'\n'+str(kpi)+'%'

    if kpi < 70:
        color = 'Red'
    elif kpi < 80:
        color = 'Yellow'
    else:
        color = 'Green'

    return color, text

def plot_diagram(daily_df):
    with schemdraw.Drawing() as d:
        d.config(fontsize=13, unit=1)

        # mpr
        color, text = kpi_values(daily_df,'MPR','mpr_r',True,False)
        d+= (MPR := Process(fill=color).label(text))

        # first 9
        d+= Arrow().theta(225).at(MPR.S)
        color, text = kpi_values(daily_df,'First 9 MPR','first_9_mpr_r',True,False)
        d+= (First_9_MPR := Process(fill=color).label(text))

        # bull
        d+= Arrow().theta(-45).at(MPR.S)
        color, text = kpi_values(daily_df,'Bull','bull_r',True,True)
        d+= (Bull := Process(fill=color).label(text))

        # Uncapped
        d+= Arrow().theta(225).at(First_9_MPR.S)
        color, text = kpi_values(daily_df,'Uncap MPR','uncapped_mpr_r',True,False)
        d+= (Uncap_MPR := Process(fill=color).label(text))

        # Single
        d+= Arrow().theta(-45).at(First_9_MPR.S)
        color, text = kpi_values(daily_df,'Single','single_r',True,True)
        d+= (Single := Process(fill=color).label(text))

        # Triple
        d+= Arrow(unit=3).theta(225).at(Uncap_MPR.S)
        color, text = kpi_values(daily_df,'Triple','trip_r',True,True)
        d+= (Triple := Process(fill=color).label(text))

        # Triple Single
        d+= Arrow(unit=2.15).down().at(Uncap_MPR.S)
        color, text = kpi_values(daily_df,'Trip Single','trip_single_r',True,True)
        d+= (Triple_Single := Process(fill=color).label(text))

        # Triple Miss
        d+= Arrow(unit=3).theta(-45).at(Uncap_MPR.S)
        color, text = kpi_values(daily_df,'Trip Miss','trip_miss_r',False,True)
        d+= (Triple_Miss := Process(fill=color).label(text))

        # Minnesota
        color, text = kpi_values(daily_df,'Minn','minn_r',False,False)
        d+= (Minn := Process(fill=color).label(text)).at((-8,1))

        # PPR
        color, text = kpi_values(daily_df,'PPR','ppr_r',True,False)
        d+= (PPR := Process(fill=color).label(text)).at((9,1))

        # First 9 PPR
        d+= Arrow().theta(225).at(PPR.S)
        color, text = kpi_values(daily_df,'First 9 PPR','first_9_ppr_r',True,False)
        d+= (First_9_PPR := Process(fill=color).label(text))

        # Double
        d+= Arrow().theta(-45).at(PPR.S)
        color, text = kpi_values(daily_df,'Double','double_r',True,True)
        d+= (Double := Process(fill=color).label(text))

def build_number_df(practice_df, type):
    # standardize naming
    val_dict = {'Single':'Hits','Double':'Hits','Triple':'Triples'}
    val = val_dict[type]

    # build data for chart
    temp_df = practice_df[(practice_df['Type']==type)].groupby('Number')[val].mean().astype(int).reset_index()
    temp_df['Average'] = temp_df[val].mean()
    temp_df.columns = ['Number','Percent','Average']

    return temp_df

def plot_numbers(practice_df):

    single_df = build_number_df(practice_df,'Single')
    double_df = build_number_df(practice_df,'Double')
    triple_df = build_number_df(practice_df,'Triple')

    fig, axs = plt.subplots(2,2,figsize=(20,8))

    # single
    axs[0][0].bar('Number','Percent',data=single_df)
    axs[0][0].plot('Number','Average',data=single_df,color='orange',ls='--',lw=1.5)
    axs[0][0].set_ylim([40,80])
    axs[0][0].set_title('Singles Hit Rate')
    axs[0][0].legend()

    # double
    axs[0][1].bar('Number','Percent',data=double_df)
    axs[0][1].plot('Number','Average',data=double_df,color='orange',ls='--',lw=1.5)
    axs[0][1].set_ylim([8,25])
    axs[0][1].set_title('Doubles Hit Rate')
    axs[0][1].legend()

    # triple
    axs[1][0].bar('Number','Percent',data=triple_df)
    axs[1][0].plot('Number','Average',data=triple_df,color='orange',ls='--',lw=1.5)
    axs[1][0].set_ylim([6,25])
    axs[1][0].set_title('Triples Hit Rate')
    axs[1][0].legend()
    plt.show()
