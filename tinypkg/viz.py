import numpy as np
import pandas as pd

import holoviews as hv
hv.extension('bokeh')
import bokeh.palettes

import tinypkg.general_utils as utils


def plot_timecourse(df, variable, value, condition=None, split=None, sort=None, cmap='default', show_all=False,
                    show_points='default', legend=False, height=350, width=500, additional_opts={}):
        
    """
    Converts a tidy DataFrame containing timecourse-like data into a plot,
    taking care to show all the data. A line is computed as the average of each
    set of points (grouped by the condition and split, if present), and the actual data
    points are overlaid on top.
    
    Inputs
    -----------------------------
    df : A tidy pandas DataFrame, containing columns with the following names:
    
        variable : The timecourse-like variable, plotted on the x-axis
        value : The quantitative value, plotted on the y-axis
        condition : The way the data is grouped for a single chart. Defaults to None.
        split :  The way the data is grouped between different charts. Defaults to None.
        sort : Which column is used to determine the sorting of the data. Defaults to None, and will
               sort by the condition column (alphabetical) if present, otherwise variable.
               
    cmap : The colormap to use. Any Holoviews/Bokeh colormap is fine. Defaults to viridis if possible.
    show_all : If split is not None, whether or not to use a drop-down or to show all the plots (layout).
               Note that this can be pretty buggy from Holoview's layout system. There is usually a way to
               show all the info you want, in a nice way. Just play around.
    show_points : Shows all the data points. I don't even know why this is an argument. Default will
                  show points if there are multiple replicates. Unless you have a real good reason, don't
                  change this.
    legend : First controls whether or not the legend is shown, then its position. Defaults to False, though
             'top' would be a good option, or 'top_left' if using split.
    height : int; the height of the chart.
    width : int; the width of the chart.
    additional_opts : A dictionary to pass additional Holoviews options to the chart. Flexible; will try all
                      options and only use the ones that did not raise an exception. Not verbose.
                      
    Returns
    ----------------------------
    chart : the final Holoviews chart
    """

    # Check columns
    utils.check_df_col(df, variable, name='variable')
    utils.check_df_col(df, value, name='value')
    utils.check_df_col(df, condition, name='condition')
    utils.check_df_col(df, split, name='split')
    utils.check_df_col(df, sort, name='sort')

    # Decide colormap
    if cmap == 'default':
        if conditions is None:
            cmap = None
        else:
            number = len(df[condition].unique())
            try:
                cmap = getattr(bokeh.palettes, 'viridis')(number+3)[1:-1]
            except NameError:
                try:
                    import bokeh.palettes
                    cmap = getattr(bokeh.palettes, 'viridis')(number+3)[1:-1]
                except ImportError:
                    cmap = None

    # Check for replicates; aggregate df
    groups = [grouping for grouping in (condition, split) if grouping is not None]
    if groups == []:
        groups = None
    replicates, df = utils.check_replicates(df, variable, value, groups)

    # Pull out available encodings (column names)
    encodings = [*list(df.columns)]

    # Set options        
    base_opts = dict(
        height=height,
        width=width,
        padding=0.1,
    )
    
    if legend is not False:
        base_opts.update(dict(show_legend=True))
        if legend is not True:
            additional_opts.update(dict(legend_position=legend))
    
    line_opts = base_opts
    scat_opts = dict(size=6, fill_alpha=0.75, tools=['hover'])
    scat_opts.update(base_opts)

    # Now, start to actually make the chart
    points = hv.Scatter(
        df,
        variable,
        [value, *encodings],
    ).opts(**scat_opts)
    
    lines = hv.Curve(
        df,
        variable,
        [('Mean of ' + str(value), value), *encodings], 
    ).opts(**line_opts)
    
    if groups is not None:
        points = points.groupby(groups).opts(**scat_opts)
        lines = lines.groupby(groups).opts(**line_opts)
        
    # Output chart as desired
    if show_points == 'default':
        if replicates is True:
            chart = lines*points
        else:
            chart = lines
    elif show_points is True:
        chart = lines*points
    else:
        chart = lines
        
    # Overlay each line plot
    if condition is not None:
        chart = chart.overlay(condition)

    # Split among different charts
    if split is not None:
        
        # If split, show as side-by-side, or dropdown
        # Note, this is pretty buggy; on Holoviews' end.
        if show_all is True:
            chart = chart.layout(split)
        
    # Assign the additional options, as allowed
    if additional_opts != {}:
        try:
            chart = chart.options(**additional_opts)
        except ValueError:
            good_opts = {}
            bad_opts = {}
            
            for opt in additional_opts.keys():
                try:
                    test = chart.options(additional_opts[opt])
                    good_opts[opt] = additional_opts[opt]
                except ValueError:
                    bad_opts[opt] = additional_opts[opt]
                    
                chart = chart.options(**good_opts)

    # Assign color
    if cmap is not None:
        chart = chart.opts({'Scatter' : {'color' : cmap}, 'Curve' : {'color' : cmap}})

    return chart