Reading Impairment in children recruited as part of the Healthy Brain Network initiative
==============================

First Steps
------------

* Clone Repo
> Clone the repo to your local path
```
git clone git@github.com:maedbhk/hbn_reading.git`
```

* Activate Virtual Environment
In this project, we're using [**conda**](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) for virtual environment and python package management

* To install and activate conda environment, run the following commands in the top-level directory of your cloned repo
```
# navigate to top-level directory of repo
$ cd ../hbn_reading

# create conda environment using .yml file
$ conda env create -f environment.yml 

# activate the conda virtual environment
$ conda activate hbn_reading # each virtual env has its own unique name (look inside the environment.yml file)

# install editable package (make sure virtual env is activated) so that you can access `src` packages
$ pip install -e .
```

* Activate jupyter notebook kernel
> To run jupyter notebook using modules installed in virtual env, run the following command in top-level directory of repo
```
# make sure you are in top-level directory of repo
$ cd ../hbn_reading

# create kernel (virtual env for jupyter notebook)
$ ipython kernel install --name "reading" --user # you can assign any name
```

Notebooks
------------
* Main results are stored here: **notebooks/figures-Reading_Impairment.ipynb**
> To access this jupyter notebook, run the following commands
```
# first, make sure your virtual environment is activated
$ conda activate hbn-reading

# navigate to the notebooks directory
$ cd ../hbn_reading/notebooks

# open the jupyter notebook
$ jupyter notebook figures-Reading_Impairment.ipynb

# once you have opened the notebook, make sure you choose the correct kernel "hbn" as it contains all of the python packages for this project
```

Project Organization
------------

### Data
> Note: **hbn_reading** data folder is stored on Google Drive: 
> I suggest downloading the google drive folder (it's not that big) and work locally OR there are python plugins that allow you to access google drive folders from jupyter notebooks

    ├── data
    │   ├── Child-features-preprocessed.csv   <- All features (preprocessed) for Child questionnaires
    │   ├── Child-features-raw.csv            <- All features (raw) for Child questionnaires
    │   ├── Parent-features-preprocessed.csv  <- All features (preprocessed) for Parent questionnaires
    │   ├── Parent-features-raw.csv           <- All features (raw) for Parent questionnaires
    │   ├── Teacher-features-preprocessed.csv <- All features (preprocessed) for Teacher questionnaires
    │   ├── Teacher-features-raw.csv          <- All features (raw) for Teacher questionnaires
    │   ├── item-names-cleaned.csv            <- Dictionary linking questionnaire columns to question keys
    │   └── models                            <- Top-level folder containing model output

### Code 

    ├── README                                <- The top-level README for developers using this project
    ├── environment.yml                       <- Required python libraries
    ├── notebooks                             <- Notebooks folder
    │   ├── figures-Reading_Impairment.ipynb  <- Example notebook
    ├── references                            <- Project-relevant materials
    │   ├── Assessment_List_Jan2019.xlsx      <- List of all assessments administered by healthy brain network
    │   ├── Data_Dictionaries.zip             <- Zipped folder containing data dictionaries (i.e. itemized breakdown of questions)
    ├── src                                   <- src folder (customized python scripts)
    │   ├── topic_modeling.py                 <- Some functions for doing topic modeling (used in `topic_modeling_HBN.ipynb`)

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
