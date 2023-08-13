## libraries to install ##
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from matplotlib.gridspec import GridSpec
from tabulate import tabulate
from pathlib import Path
import glob

import warnings
warnings.filterwarnings('ignore')

def plotting_style():
    plt.style.use('seaborn-poster') # ggplot
    params = {'axes.labelsize': 30,
            'axes.titlesize': 25,
            'legend.fontsize': 25,
            'xtick.labelsize': 25,
            'ytick.labelsize': 25,
           # 'figure.figsize': (10,8),
            'font.weight': 'regular',
            # 'font.size': 'regular',
            'font.family': 'sans-serif',
            'lines.markersize': 20,
            'font.serif': 'Helvetica Neue',
            'lines.linewidth': 4,
            'axes.grid': False,
            'axes.spines.top': False,
            'axes.spines.right': False}
    plt.rcParams.update(params)
    sns.set_context(rc={'lines.markeredgewidth': 0.1})
    np.set_printoptions(formatter={'float_kind':'{:f}'.format})


def load_data(
    fdir,
    assessments=['Parent', 'Child', 'Teacher'],
    data_type='preprocessed'
    ):
    """loads all response data for healthy brain network
    Args:
        assessments (list of str): default is all assessments ['Parent', 'Child', 'Teacher']
        data_type (str): default is 'preprocessed'. other option is 'raw'
    Returns:
        df_data_all (pd dataframe): all response data;
        df_diagnosis (pd dataframe): diagnosis data for each participant
    """
    
    # get data
    df_data_all = pd.DataFrame()
    for assessment in assessments:
        # load csv
        df_data = pd.read_csv(os.path.join(fdir, f'{assessment}-features-{data_type}.csv'))
        df_data.columns = df_data.columns.str.replace('numeric__', '')
        df_data_all = pd.concat([df_data, df_data_all], axis=1)

    # delete duplicate columns
    data = df_data_all.loc[:,~df_data_all.columns.duplicated()].copy()
    
    return data


def load_diagnosis(fdir):
    demo_dict = {
                'Identifiers': 'Identifiers',
                'Sex': 'Sex',
                'Age': 'Age', 
                'PreInt_Demos_Fam,Child_Race_cat': 'Race',
                'PreInt_Demos_Fam,Child_Ethnicity_cat': 'Ethnicity',
                'Enroll_Year': 'Enroll_Year',
                'Site': 'Site',
                'comorbidities': 'comorbidities',
                }

    # get clinical diagnosis
    diagnosis = pd.read_csv(os.path.join(fdir, 'Clinical_Diagnosis_Demographics.csv'))

    # get columns to filter dataframe
    cols = []
    for num in range(1,11):

        num_str = str(num).zfill(2)
        col_1 = f'DX_{num_str}_Cat_new'
        col_2 = col_1.replace('_Cat_new', '')
        cols.extend([col_1, col_2])

    cols_to_keep = list(demo_dict.values())
    cols_to_keep.extend(cols)

    diagnosis = diagnosis.rename(columns=demo_dict)[cols_to_keep]   
    diagnosis['Category'] = diagnosis['DX_01_Cat_new']
    diagnosis['Diagnosis'] = diagnosis['DX_01']
    
    return diagnosis


def filter_data(
    data, 
    diagnosis, 
    remove_demos=False, 
    col_to_filter='Category_raw', 
    val_to_filter=['ADHD'],
    drop_identifiers=True
    ):
    """filters `data` based on information in `diagnosis`
    
    Args:
        data (pd dataframe): `data` output from `load_data`
        diagnosis (pd dataframe): `diagnosis` output from `load_data`
        remove_demos (bool): optionally remove columns corresponding to demographic information (e.g., Sex, Race, Age) and just leave questionnaire response data
        col_filter (str or None): filter `data` using `col_to_filter`(e.g., column name)
        val_to_filter (list of str or None): filter `data` using `val_to_filter` (eg., value in column) from `diagnosis`
        drop_identifiers (bool): drop 'Identifiers' column
    """
    
    for col in diagnosis.columns:
        if col != "Identifiers":
          diagnosis = diagnosis.rename(columns={col: f'{col}_raw'})
    
    df_data_diagnosis = data.merge(diagnosis, on='Identifiers')
    
    # filter based on some conditional
    col_to_filter_raw = f'{col_to_filter}_raw'
    if (col_to_filter_raw is not None) and (val_to_filter is not None):
        data_out = df_data_diagnosis[df_data_diagnosis[col_to_filter_raw].isin(val_to_filter)].reset_index(drop=True)
    else:
        data_out = df_data_diagnosis.reset_index(drop=True)

    # optionally remove demographic data (sex, age, comorbidities etc.)
    demo_cols = [col for col in diagnosis.columns if 'Identifiers' not in col]
    if remove_demos:
        # exclude demo variables from dataset
        demo_cols_stripped = [col.replace('_raw', '') for col in demo_cols]
        data_out = data_out[data_out.columns[~data_out.columns.isin(demo_cols_stripped)]]
    
    # optionally drop identifiers
    if drop_identifiers:
        data_out = data_out[[col for col in data_out.columns if 'Identifiers' not in col]]

    # columns to include in the modeling process (only response data)
    cols_to_keep = [col for col in data_out.columns if '_raw' not in col]
    cols_to_keep.remove('Identifiers')

    return data_out, cols_to_keep


def get_comorbidities(dataframe, comorbid_disorders=['Anxiety Disorders', 'Depressive Disorders', 'ADHD', 'Autism Spectrum Disorder']):

    vals = []; categories = []; diagnoses = []; percent_all=[]
    for num in np.arange(1,11):
        for disorder in comorbid_disorders:

            num_str = str(num).zfill(2)
            disorder_num = f'DX_{num_str}_Cat_new'

            val = np.nansum(dataframe[disorder_num].str.contains(disorder))
            percent = (val / dataframe.shape[0]) *100
            vals.append(val)
            percent_all.append(percent)
            diagnoses.append(disorder)
            categories.append(disorder_num)

    # make dataframe
    df_co = pd.DataFrame()
    df_co['Diagnosis'] = diagnoses
    df_co['Count'] = vals
    df_co['Percent'] = percent_all
    df_co['Category'] = categories
    df_co['Diagnosis Categories'] = df_co['Category'].str.extract('(\d+)')

    return df_co


def count_all_diagnoses(dataframe, diagnosis='ADHD'):

    count_all = []; diagnosis_categories=[]
    for idx in range(1,11):

        num_str = str(idx).zfill(2)
        disorder_str = f'DX_{num_str}_Cat_new'

        count = sum(dataframe[disorder_str]==diagnosis)

        diagnosis_categories.append(disorder_str)
        count_all.append(count)

    df = pd.DataFrame()
    df['count'] = count_all
    df['diagnosis_categories'] = diagnosis_categories
    df['primary_diagnosis'] = diagnosis

    return df


def shorten_diagnosis_name(dataframe, old_name, new_name):
    # replace `old_name` with `new_name` to make visualization easier
    for num in range(1,11):
        num_str = str(num).zfill(2)
        disorder_str = f'DX_{num_str}_Cat_new'

        dataframe[disorder_str] = dataframe[disorder_str].replace(old_name, new_name) # make easier for visualization

    return dataframe
