# author: Matilda Schauf

# import modules
import pandas as pd
import numpy as np

### FUNCTIONS ###
# defined outside of the class because they are not directly related to syntactic complexity and do not need to be imported
# the class for the syntactic complexity measures is defined below these functions

def make_final_list(mean_mes: list):
    """
    Function that takes a list in which syntactic complexity measure results are collected for each individual text, and stores the results in a final list where they are assigned to years and their yearly average is calculated.

    Input:
        1. mean_mes (list): List containing lists of the form [year (int), text number (int), text value (float)]
    Output:
        1. final_list (list): List containing lists of the form [year (int), year value (float), student values (list of float)"""

    final_list = list()

    # load list into data frame with columns for year, text number, text value
    df_data = pd.DataFrame(mean_mes, columns=["YEAR", "NO", "VALUE"])

    for year in set(df_data.YEAR):
        # save all text (student) values from the year in a list
        student_vals = list(df_data[df_data["YEAR"] == year].VALUE)
        # save the mean of the student values as year value
        year_val = np.mean(np.array(student_vals))
        # add values to final list
        final_list.append([year, year_val, student_vals])
    
    return final_list

def make_final_df(final_list: list):
    """
    Function that creates a dataframe from list of the form [year, year value, student values] and sorts by years.

    Input:
        1. final_list (list): List containing lists of the form [year (int), year value (float), student values (list of float)]
    Output:
        1. final_df (Pandas.DataFrame): Dataframe with the columns [year (int), year value (float), student values (list of float)], sorted by years"""
    
    # load final list into data frame
    final_df = pd.DataFrame(final_list, columns=["YEAR", "YEAR_VAL", "STUDENT_VALS"])
    
    # sort data frame by year, starting with the lowest number
    final_df = final_df.sort_values(by="YEAR", ignore_index=True)

    # add columns for standard deviation (sample) and mean
    final_df["STUDENT_STD"] = final_df.STUDENT_VALS.apply(np.std, ddof=1)
    final_df["YEARS_MEAN"] = final_df.YEAR_VAL.mean()
    final_df["YEARS_STD"] = final_df.YEAR_VAL.std()

    # safe data frame with different order of the columns
    final_df = final_df[["YEAR", "YEAR_VAL", "STUDENT_VALS", "STUDENT_STD", "YEARS_MEAN", "YEARS_STD"]]

    return final_df


### CLASS ###

class SynComplMeas:
    """
    A class to represent our syntactic complexity measures.

    Attributes
    ----------
    name : str
        Name for the class
    df_dict : dict
        Dictionary that contains data frames with corpus annotation data for several connlup files
    sent_lens : Pandas.DataFrame
        Results for feature "Mean Sentence Length in Tokens"
    tok_embeds : Pandas.DataFrame
        Results for feature "Mean Token Embedding Depth"
    max_sent_embeds : Pandas.DataFrame
        Results for feature "Mean Maximum Embedding Depth per Sentence"
    simpx_s : Pandas.DataFrame
        Results for feature "Simplex Clauses per Sentence"
    subc_s : Pandas.DataFrame
        Results for feature "Dependent Clauses per Sentence"
    relc_s : Pandas.DataFrame
        Results for feature "Relative Clauses per Sentence"
    parac_s : Pandas.DataFrame
        Results for feature "Paratactic Clause Constructions per Sentence"
    clauses_s : Pandas.DataFrame
        Results for feature "Clauses per Sentence"
    verbx_s : Pandas.DataFrame
        Results for feature "Verb Phrases per Sentence"
    vc_s : Pandas.DataFrame
        Results for feature "Verb Complexes per Sentence"
    nx_s : Pandas.DataFrame
        Results for feature "Noun Phrases per Sentece"
    simpx_c : Pandas.DataFrame
        Results for feature "Simplex Clause Ratio"
    subc_c : Pandas.DataFrame
        Results for feature "Dependent Clause Ratio"
    relc_c : Pandas.DataFrame
        Results for feature "Relative Clause Ratio"
    parac_c : Pandas.DataFrame
        Results for feature "Paratactic Clause Construction Ratio"
    clause_lens : Pandas.DataFrame
        Results for feature "Mean Clause Length in Tokens"
    simpx_lens : Pandas.DataFrame
        Results for feature "Mean Simplex Clause Length in Tokens"
    relc_lens : Pandas.DataFrame
        Results for feature "Mean Relative Clause Length in Tokens"
    nx_lens : Pandas.DataFrame
        Results for feature "Mean Noun Phrase Length"
    px_lens : Pandas.DataFrame
        Results for feature "Mean Prepositional Phrase Length"
    vf_lens : Pandas.DataFrame
        Results for feature "Mean Initial Field (Vorfeld) Length"
    mf_lens : Pandas.DataFrame
        Results for feature "Mean Middle Field (Mittelfeld) Length"
    nf_lens : Pandas.DataFrame
        Results for feature "Mean Final Field (Nachfeld) Lenght"
    vv_nn : Pandas.DataFrama
        Results for feature "Verb/Noun Ratio"

    Methods
    -------
    count_pattern(df: Pandas.DataFrame, regex: str):
        Counts pattern in the syntax column of a text.
    get_tok_embeds(df: Pandas.DataFrame, replace_RE: str):
        Calculates feature "Mean Token Embedding Depth" for a text.
    get_max_embeds(df: Pandas.DataFrame, replace_RE: str, sent_count: int):
        Calculates feature "Mean Maximum Embedding Depth per Sentence" for a text.
    get_clause_lens(df: Pandas.DataFrame, regex: str):
        Takes regular expression of a clause's node label and calculates the mean clause length in a text.
    get_phrase_lens(df: Pandas.DataFrame, regex: str):
        Takes regular expression of a phrase's node label and calculates the mean phrase length in a text.
    """
    def __init__(self, name, df_dict):
        """
        Constructs all the necessary attributes for the syntactic complexity measures object.

        Parameters
        ----------
            name : str
                Name for the class
            df_dict : dict
                Dictionary that contains data frames with corpus annotation data for several connlup files
        """
        self.name = name
        self.df_dict = df_dict

        # syntactic complexity feature names
        self.feature_names = ["sent_lens", "tok_embeds", "max_sent_embeds", "simpx_s", "subc_s", "relc_s", "parac_s", "clauses_s", "verbx_s", "vc_s", "nx_s", "simpx_c",
        "subc_c", "relc_c", "parac_c", "clause_lens", "simpx_lens", "relc_lens", "nx_lens", "px_lens", "vf_lens", "mf_lens", "nf_lens", "vv_nn"]

        ### calculate features ###

        # regular expression that matches all topological field node tags (needed later for some features)
        top_fields_RE = r"""(?x)    # flag verbose
                        \|          # beginning hyphen
                        (
                        ([BIE]-)?   # optional: B- or I- or E-
                         (
                         [VMN]FE?   # VF or MF or NF or MFE
                         |
                         L[KV]      # LK or LV
                         |
                         F?KOORD    # FKOORD or KOORD
                         |
                         PARORD
                         |
                         V?CE?      # VC or VCE or C
                         |
                         FKONJ
                         )
                        )
                        (?= $|\|)   # lookahead: should be there but won't be replaced
                        """

        # initialize empty dictionary for saving the results of the different features later
        # key = variable for the feature (str); value = list of lists [year, text number, text value] for each text
        feat_lists = dict()

        for feat_name in self.feature_names:
            # initialize empty list for each feature
            feat_lists[feat_name] = list()
        
        # iterate over dictionary containing data frames with corpus annotations for every text
        for year, no in self.df_dict:

            ### save variables
            
            df = self.df_dict[(year, no)]
            tok_count = len(df)

            # sent count = value of column SENT_ID in the last row plus 1 (as sent id starts with 0)
            sent_count = int(df[-1:].SENT_ID)+1

            # count all patterns that will be needed and save them
            simpx_count = self.count_pattern(df, r"(^|\|)(B-)?SIMPX")
            subc_count = self.count_pattern(df, r"(^|\|)(B-)?C($|\|)")
            relc_count = self.count_pattern(df, r"(^|\|)(B-)?R-?SIMPX")
            parac_count = self.count_pattern(df, r"(^|\|)(B-)?P-?SIMPX")
            clauses_count = self.count_pattern(df, r"(^|\|)(B-)?[PR]?-?SIMPX")
            verbx_count = self.count_pattern(df, r"(^|\|)(B-)?VXF?INF?")
            vc_count = self.count_pattern(df, r"(^|\|)(B-)?VCE?")
            nx_count = self.count_pattern(df, r"(^|\|)(B-)?NX")
            vv_count = self.count_pattern(df, r"VV.*", col="xpos")
            nn_count = self.count_pattern(df, r"NN", col="xpos")


            ### calculate syntactic complexity features

            ## 1: Mean Sentence Length in Tokens
            sent_lens = tok_count/sent_count
            # append result list to dictionary for saving results
            feat_lists["sent_lens"].append([year, no, sent_lens])

            ## 2: Mean Token Embedding Depth
            # perform method
            tok_embeds = self.get_tok_embeds(df, top_fields_RE)
            # append result list to dictionary for saving results
            feat_lists["tok_embeds"].append([year, no, tok_embeds])

            ## 3: Mean Maximum Embedding Depth per Sentence
            # perform method
            max_embeds = self.get_max_embeds(df, top_fields_RE, sent_count)
            # append result list to dictionary for saving results
            feat_lists["max_sent_embeds"].append([year, no, max_embeds])

            ## 4: Clause-sentence or phrase-sentence ratios
            # save counts of clauses/phrases in list
            total_counts = [simpx_count, subc_count, relc_count, parac_count, clauses_count, verbx_count, vc_count, nx_count]
            # also save variable names as strings in list (needed for defining dictionary keys later)
            total_counts_names = ["simpx_count", "subc_count", "relc_count", "parac_count", "clauses_count", "verbx_count", "vc_count", "nx_count"]

            # iterate over counts and variable names
            for count, count_name in zip(total_counts, total_counts_names):
                count_sent_ratio = count/sent_count
                # define first part of the key string
                key1 = count_name.split("_")[0]
                # append result list to dictionary for saving results
                feat_lists[key1 + "_s"].append([year, no, count_sent_ratio])

            ## 5: clause-clause or phrase-clause ratios
            # remove "clauses_count" from the total counts and total counts names lists as it is only needed for normalizing from now on
            # also remove "verbx_count", "vc_count", "nx_count" as we do not examine their per clause ratio
            for i in range(4):
                total_counts.pop(4)
                total_counts_names.pop(4)

            # iterate over counts and variable names
            for count, count_name in zip(total_counts, total_counts_names):
                count_clause_ratio = count/clauses_count
                # define first part of the key string
                key1 = count_name.split("_")[0]
                # append result list to dictionary for saving results
                feat_lists[key1 + "_c"].append([year, no, count_clause_ratio])

            ## 6: lengths of clauses/phrases
            # perform method for getting clause lengths and save values
            # mean_clause_lens = self.get_clause_lens(df, r"[PR]?-?SIMPX")
            # mean_simpx_lens = self.get_clause_lens(df, r"SIMPX")
            # mean_relc_lens = self.get_clause_lens(df, r"R-?SIMPX")
            mean_clause_lens = self.get_phrase_lens(df, r"[PR]?-?SIMPX")
            mean_simpx_lens = self.get_phrase_lens(df, r"SIMPX")
            mean_relc_lens = self.get_phrase_lens(df, r"R-?SIMPX")

            # perform method for getting phrase lengths and save values
            mean_nx_lens = self.get_phrase_lens(df, r"NX")
            mean_px_lens = self.get_phrase_lens(df, r"PX")
            mean_vf_lens = self.get_phrase_lens(df, r"VF")
            mean_mf_lens = self.get_phrase_lens(df, r"MF")
            mean_nf_lens = self.get_phrase_lens(df, r"NF")

            # save values + variable names as strings in lists
            len_vals = [mean_clause_lens, mean_simpx_lens, mean_relc_lens, mean_nx_lens, mean_px_lens, mean_vf_lens, mean_mf_lens, mean_nf_lens]
            len_vals_names = ["mean_clause_lens", "mean_simpx_lens", "mean_relc_lens", "mean_nx_lens", "mean_px_lens", "mean_vf_lens", "mean_mf_lens", "mean_nf_lens"]

            # iterate over values and value variable names
            for len_val, len_val_name in zip(len_vals, len_vals_names):
                # define first part of key string
                key1 = len_val_name.split("_")[1]
                # append result list to dictionary for saving results
                feat_lists[key1 + "_lens"].append([year, no, len_val])

            ## 7: NN/VV.* ratio
            vv_nn = vv_count/nn_count
            feat_lists["vv_nn"].append([year, no, vv_nn])
            
            #### end of over data frames iterating for-loop
        
        ### RESULTS ###

        # initialize dictionary that saves results as data frames
        results_dict = dict()

        # iterate over dictionary that has results saved in lists
        for key_name in feat_lists:
            # perform function that assigns results to the respective years, calculates year value, and saves it in final list
            final_list = make_final_list(feat_lists[key_name])
            # perform function that makes a data frame out of it and adds standard deviations etc.
            results_dict[key_name] = make_final_df(final_list)

        # get results from resutls dict and save them as class atributes
        self.sent_lens = results_dict["sent_lens"]
        self.tok_embeds = results_dict["tok_embeds"]
        self.max_sent_embeds = results_dict["max_sent_embeds"]
        self.simpx_s = results_dict["simpx_s"]
        self.subc_s = results_dict["subc_s"]
        self.relc_s = results_dict["relc_s"]
        self.parac_s = results_dict["parac_s"]
        self.clauses_s = results_dict["clauses_s"]
        self.verbx_s = results_dict["verbx_s"]
        self.vc_s = results_dict["vc_s"]
        self.nx_s = results_dict["nx_s"]
        self.simpx_c = results_dict["simpx_c"]
        self.subc_c = results_dict["subc_c"]
        self.relc_c = results_dict["relc_c"]
        self.parac_c = results_dict["parac_c"]
        self.clause_lens = results_dict["clause_lens"]
        self.simpx_lens = results_dict["simpx_lens"]
        self.relc_lens = results_dict["relc_lens"]
        self.nx_lens = results_dict["nx_lens"]
        self.px_lens = results_dict["px_lens"]
        self.vf_lens = results_dict["vf_lens"]
        self.mf_lens = results_dict["mf_lens"]
        self.nf_lens = results_dict["nf_lens"]
        self.vv_nn = results_dict["vv_nn"]
    

    ### METHODS ####

    def count_pattern(self, df: pd.DataFrame, regex: str, col="syn"):
        """
        Takes data frame and regular expression and returns the amount of times the pattern occurs in the syntax column of the data frame.
        
        Input:
            1. df (Pandas.DataFrame): Data frame with corpus annotations for a text
            2. regex (str): Regular expression for a pattern
            3. col (str): Keyword for the column in which the pattern will be counted. It can be "syn" or "xpos".
                            The default value is "syn" as most patterns are counted in the SYNTAX column
        Output:
            1. pattern_count (int): Number of how often the pattern occured"""
        
        if col=="syn":
            # count pattern in every row for the syntax column, calculate sum
            pattern_count = df.SYNTAX.str.count(regex).sum()
        if col=="xpos":
            # alternatively, count in XPOS-column
            pattern_count = df.XPOS.str.count(regex).sum()

        return pattern_count

    def get_tok_embeds(self, df: pd.DataFrame, replace_RE: str):
        """
        Calculates the mean token embedding depth in node tagsof a text. The embedding depth for a token is the path from the root node to the terminal node.

        Input:
            1. df (Pandas.DataFrame): Data frame with corpus annotations for a text
            2. replace_RE (str): Regular expression for removing topological field node tags
        Output:
            1. tok_embeds (float): Mean token embedding depth for the text"""

        # remove topological field node tags, split at "/", apply function len() to each row in the syntax column, and save Series
        nodes = df.SYNTAX.str.replace(replace_RE, '', regex=True).str.split("|").apply(len)

        # mean of the series = mean token embedding depth
        tok_embeds = nodes.mean()

        return tok_embeds

    def get_max_embeds(self, df: pd.DataFrame, replace_RE: str, sent_count: int):
        """
        Calculates the mean maximum embedding depth per sentence of a text.

        Input:
            1. df (Pandas.DataFrame): Data frame with corpus annotations for a text
            2. replace_RE (str): Regular expression for removing topological field node tags
        Output:
            1. max_embeds (float): Mean maximum embedding depth per sentence"""

        # create temporary column TEMP with length of the path from terminal node to root node for each token
        df["TEMP"] = df.SYNTAX.str.replace(replace_RE, '', regex=True).str.split("|").apply(len)

        # list comprehension - iterate over sentences, save maximum embedding depth (value of column TEMP) of each sentence in list
        max_lens = [np.max(np.array(df[df["SENT_ID"]==i].TEMP)) for i in range(sent_count)]

        # delete column TEMP as it is not needed anymore
        df.drop(labels=["TEMP"], axis=1, inplace=True)

        # mean maximum embedding depth per sentence = mean of list with maximum embedding depths
        max_embeds = np.mean(np.array(max_lens))

        return max_embeds
    
    def get_clause_lens(self, df: pd.DataFrame, regex: str):
        """
        Calculates mean clause lengths in tokens of a text by normalizing the number of tokens inside of a clause with the number of clauses.

        Input:
            1. df (Pandas.DataFrame): Data frame with corpus annotations for a text
            2. regex (str): Regular expression that matches all node tags of the respective clause
        Output:
            1. clause_len (float): Length of the respective clause in tokens"""

        # number of tokens inside the clause = length of the dataframes only with tokens that are tagged with the clause's node tags
        tok_count = len(df[df.SYNTAX.str.contains(r"[BIE]-" + regex)])

        # number of clauses = number of node tags that mark the beginning of the clause
        c_count = df.SYNTAX.str.count(r"(^|\|)(B-)?" + regex).sum()

        clause_len = tok_count/c_count

        return clause_len
    
    def get_phrase_lens(self, df: pd.DataFrame, regex: str):
        """
        Calculates the mean phrase or field length in node tags or tokens by normalizing the number of node tags inside of a phrase/field with the number of phrases/fields.

        Input:
            1. df (Pandas.DataFrame): Data frame with corpus annotations for a text
            2. regex (str): Regular expression that matches all node tags of the respective phrase/field
        Output:
            1. phrase_len (float): Length of the phrase/field in node tags or tokens"""

        # number of node tags in phrase/field = sum of all phrase/field node tags in the syntax column
        phrase_tag_count = df.SYNTAX.str.count(r"(^|\|)([BIE]-)?" + regex).sum()

        # number of phrases/fields = sum of all node tags that mark the beginning of a phrase/field
        phrase_count = df.SYNTAX.str.count(r"(^|\|)(B-)?" + regex).sum()

        phrase_len = phrase_tag_count/phrase_count

        return phrase_len
