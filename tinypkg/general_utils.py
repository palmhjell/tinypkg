import numpy as np
import pandas as pd


def check_df_col(df, column, name=None):
    """
    Checks for the presence of a column (or columns) in a tidy DataFrame with an 
    informative error message. Passes silently, otherwise raises error.
    """
    if column is not None:
        
        if type(column) != list:
            
            column = [column]
            
        for col in column:

            if name is None:
                error_message = "The value '" + str(col) + "' is not present in any of the columns of your DataFrame.\n"\

            else:
                error_message = "Your " + str(name) + " value '" + str(col) + \
                "' is not present in any of the columns of your DataFrame.\n"\

            error_message += "\n"\
                "You may be looking for:\n"\
                "\n"\
                +str(list(df.columns))

            assert col in df.columns, error_message

        
def check_replicates(df, variable, value, grouping):
    """
    Checks for the presence of replicates in the values of a dataset, given
    some experimental conditions. Returns True if the standard deviation of the 
    values of each group (if more than one exists) is >0, indicating that replicates
    were performed under the given criteria.
    
    Inputs
    ------------------------
    df : A tidy pandas DataFrame, contianing columns with the following names:
        
        variable : The independent variable, indicating a specific experimental condition.
        value: The dependent variable, indicating an experimental observation.
        group: Indicates how the data should be split. Can be a list.
        
    Returns
    ------------------------
    replicates : boolean
    df : the DataFrame containing averaged 'variable' values, if replicates is True.
         Otherwise returns the original DataFrame.
    """
    
    # Unpack the experimental conditions into a single list of arguments
    if type(grouping) != list:
        grouping = [grouping]
    args = [elem for elem in [variable, *grouping] if elem != None]

    # Get stdev of argument groups
    grouped = df.groupby(args)[value]
    group_stdevs = grouped.std().reset_index()
    group_stdev = group_stdevs[value].mean()

    # Determine if there are replicates (mean > 0)
    if group_stdev > 0:
        replicates = True
    else:
        replicates = False
        
    # Average the values and return
    if replicates is True:
        df_mean = grouped.mean().reset_index()
        df_mean.columns = list(df_mean.columns[:-1]) + ['Mean of ' + str(value)]
        df = df.merge(df_mean)
        
    return replicates, df