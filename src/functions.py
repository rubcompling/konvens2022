# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 19:29:14 2022

@author: matif
"""

# import modules
import pandas as pd
import numpy as np

def get_filenames(filenames_categorized: str, test: bool):
    """
    Function that takes .csv-File with the filenames that have been categorized into dev or test files and returns either the filenames for the development data or the filenames for the test data.
        
        Input:
            1. filenames_categorized (str): Filename of the file with the filenames and their categories
            2. test (bool): True when test filenames should be returned, False when development filenames should be returned
        Output:
            1. filenames (list): List of the wanted conllup filenames (str)"""
    
    # read filename into dataframe with the columns "filename" and "test_or_dev"
    df = pd.read_csv(filenames_categorized, sep="\t", header=None, names=["filename", "test_or_dev"])
    
    # save filenames according to their category in the "test_or_dev" column
    if test:
        filenames = list(df[df["test_or_dev"] == "test"].filename)
    else:
        filenames = list(df[df["test_or_dev"] == "dev"].filename)

    return filenames


######################################
def make_df_dict(path: str, filenames: list):
    """
    Function that takes a list of filenames, loads the conllup files into a data frame, and saves them in a dictionary with the key tuples (year, text number).

        Input:
            1. path (str): Path to the files on the computer
            2. filenames (list): List with the filenames of the conllup files (str)
        Output:
            1. dfs_dict (dict): Dictionary with key = tuple (year, text number) and value = data frame"""
    
    # load filenames into data frame with one column
    df_files = pd.DataFrame(filenames, columns=["filenames"])

    # create year column with regex
    df_files["year"] = df_files.filenames.str.extract(r"^(\d{4})_")

    # make set of years
    years = set(df_files.year)

    # initialize dictionary for saving data frames
    dfs_dict = dict()

    for year in years:
        # save filenames of the "current" year in list
        filenames = list(df_files.filenames[df_files["year"] == year])

        for i, filename in enumerate(filenames):

            # open connlup file and use first line for saving the column names for data frame
            with open(path+filename, "r", encoding="UTF-8") as file:
                column_names = file.readline().replace("# global.columns =", "").strip().split()

            # load connlup file into data frame
            df = pd.read_csv(path+filename, comment="#", sep="\t", quoting=3, header=None, names=column_names)

            # convert all headline column values into strings
            df = df.astype({"UEBERSCHRIFT": "string"})
            # delete rows that are headlines
            df = df[df.UEBERSCHRIFT == "0"]
            # reset index
            df.reset_index(drop=True, inplace=True)

            # add column "SENT_ID" with sent IDs, starting from 0
            df.loc[[0],["ID"]] = 1
            df["SENT_ID"] = df.ID.eq(1).cumsum() - 1

            # delete rows with no words
            df = df[~df.FORM.str.contains("EMPTY")]
            # delete superfluous rows for only one word
            df = df[~df.FORM.str.contains(r"<[IE]->")]
            # reset index
            df.reset_index(drop=True, inplace=True)

            # only keep columns that are needed
            keep = ["SENT_ID", "SYNTAX", "XPOS"]
            df = df[keep]
            
            # add data frame to dictionary with key (year, text number)
            dfs_dict[(int(year), i+1)] = df

    return dfs_dict
