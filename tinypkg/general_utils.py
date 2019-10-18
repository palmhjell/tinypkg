import numpy as np
import pandas as pd


def check_df_col(df, column, name=None):
    """
    Checks for the presence of a column (or columns) in a tidy
    DataFrame with an informative error message. Passes silently,
    otherwise raises error.
    """
    if column is not None:

        if type(column) != list:

            column = [column]

        for col in column:
            if name is None:
                error_message = f"The value '{col}' is not present in any of the columns of your DataFrame."
            else:
                error_message = f"Your {name} value '{col}' is not present in any of the columns of your DataFrame."
            error_message += "\nYou may be looking for:\n  " + str(list(df.columns))

            assert col in df.columns, error_message


def check_replicates(df, variable, value, grouping):
    """Checks for the presence of replicates in the values of a dataset,
    given some experimental conditions. Returns True if the standard
    deviation of the values of each group (if more than one exists) is
    greater than, indicating that replicates were performed under the
    given criteria.

    Parameters
    ----------
    df : Pandas DataFrame in tidy format
        The data set to be checked for replicates
    variable : immutable object
        Name of column of data frame for the independent variable,
        indicating a specific experimental condition.
    value : immutable object
        Name of column of data frame for the dependent variable,
        indicating an experimental observation.
    group : immutable object of list of immutable objects
        Column name or list of column names that indicates how the
        data set should be split.

    Returns
    -------
    replicates : boolean
        True if replicates are present.
    df_out : the DataFrame containing averaged 'variable' values, if
        replicates is True. Otherwise returns the original DataFrame.
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
    replicates = bool(group_stdev > 0)

    # Average the values and return
    if replicates:
        df_mean = grouped.mean().reset_index()
        df_mean.columns = list(df_mean.columns[:-1]) + ['Mean of ' + str(value)]
        df_return = df.merge(df_mean)

    return replicates, df_return