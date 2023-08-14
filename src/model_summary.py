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

def load_model_results(dirn, 
             models=['reading-basic_demographics-multiple-classifiers-models'],
             diagnosis_name='Specific Learning Disorder with Impairment in Reading',
             all_diagnoses=['Depressive Disorders', 'Anxiety Disorders', 'Autism Spectrum Disorder', 'No Diagnosis Given', 'ADHD'],
             diagnosis_file='Clinical_Diagnosis_Demographics.csv',
             save=True
            ):

    # hard code model diretory
    df_all = pd.DataFrame()
    for model in models:
        df = check_models(dirn=os.path.join(dirn, 'models'), 
                    diagnosis_file=os.path.join(dirn, diagnosis_file),
                    filter=f'*{model}/*')
        # assign new columns
        df['participant_group'] = df['sex'] + '_' + df['age']
        df['category_new'] = df['category'].str.replace(f'{diagnosis_name}_', '').str.replace(f'_{diagnosis_name}', '')
        df.loc[~df['category_new'].isin(all_diagnoses), 'category_new'] = 'All Other Diagnoses'
        df['model_name'] = model
        df_all = pd.concat([df_all, df])

        # save model summary to disk
        if save:
            fpath = os.path.join(dirn, 'models', model + '.csv')
            df.to_csv(os.path.join(fpath), index=False)

    return df_all


def filter_model_results(dataframe,
                       model_names=['reading-basic_demographics-multiple-classifiers-models'],
                       sex=['all'],
                       data=['data'],
                       assessment=['Parent Measures'],
                       category_new=['Depressive Disorders'],
                       clf=['DecisionTreeClassifier'],
                       ages=None
                       ):
    
    # filter dataframe
    if ages is None:
        df = dataframe[(dataframe['model_name'].isin(model_names)) &
                     (dataframe['sex'].isin(sex)) &
                     (dataframe['data'].isin(data)) &
                     (dataframe['assessment'].isin(assessment)) &
                     (dataframe['clf'].isin(clf)) &
                     (dataframe['category_new'].isin(category_new))
                    ].reset_index(drop=True)
    else:
        df = dataframe[(dataframe['model_name'].isin(model_names)) &
             (dataframe['sex'].isin(sex)) &
             (dataframe['data'].isin(data)) &
             (dataframe['assessment'].isin(assessment)) &
             (dataframe['clf'].isin(clf)) &
             (dataframe['category_new'].isin(category_new)) &
             (dataframe['age'].isin(ages)
             )
            ].reset_index(drop=True)
    
    return df


def plot_model_results(dataframe, 
                       x='category_new', 
                       y='roc_auc_score', 
                       hue=None, 
                       split=False,
                       title=''
                      ):
    ax = sns.violinplot(x=x, y=y, hue=hue, split=split, data=dataframe)
    plt.xticks(rotation=45, ha='right')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(title)
    plt.axhline(y=0.5, color='k', linestyle='--')
    ax.set_ylim([0.4, 1.])
    plt.show()

    
    
def check_models(dirn,
                diagnosis_file,
                filter='*2023*'):

    models = glob.glob(os.path.join(dirn, filter))

    # load in clinical diagnosis
    dx = pd.read_csv(diagnosis_file)

    model_name =  'classifier-all-phenotypic-models-performance.csv'
    feature_name = 'classifier-feature_importance.csv'

    df_all = pd.DataFrame()
    # loop over models
    for model_dir in models:
        try:
            # load models
            df = pd.read_csv(os.path.join(model_dir, model_name))

            # make participants dataframe
            participants = df['participants'].loc[0].split("-")
            df_part = pd.DataFrame(participants, columns=['Identifiers'])

            # get target
            target = df['target'].unique().tolist()

            # merge participants with diagnosis and sex
            diagnoses = dx.merge(df_part, on=['Identifiers'])['DX_01'].unique().tolist()
            category = dx.merge(df_part, on=['Identifiers'])['DX_01_Cat_new'].unique().tolist()
            sex = dx.merge(df_part, on=['Identifiers'])['Sex'].unique().tolist()
            age = dx.merge(df_part, on=['Identifiers'])['Age'].round().unique().astype(int)
    
            # make into str
            if len(age)>1:
                min_age = min(age); max_age = max(age)
                age = f'{min_age:02d}-{max_age:02d}'
            else:
                age = f'{age[0]:02d}'
            
            if len(sex)>1:
                sex = 'all'
            else:
                sex = sex[0]
            
            # add new columns to dataframe
            df['diagnoses'], df['category'], df['sex'], df['age'] = '_'.join(diagnoses), '_'.join(category), sex, age
            df['data'] = df['data'].map({'model-data': 'null', 'model-null': 'data'})
            
            # print out models
            #print(f'{Path(model_dir).name}: {diagnoses}: {target}: {sex}: {age}')
            
            # concat dataframes
            df_all = pd.concat([df_all, df])

        except:
            pass
            print(f'{model_name} does not exist for {model_dir}, run `run_second_level.sh`')
        
    return df_all

