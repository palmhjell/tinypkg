import numpy as np
import pandas as pd

import tinypkg.general_utils as utils

######################
# check_df_col()
######################

df = pd.DataFrame({
    'foo' : range(0, 3),
    'bar' : range(0, 3)
})

def test_col_exists():
    
    utils.check_df_col(df, 'foo')
    
def test_col_does_not_exist():
    
    try:
        utils.check_df_col(df, 'baz')
        
        # If it gets past that, we need to raise an error
        exists = True
    
    except AssertionError:
        exists = False
    
    assert exists is False
    
    
######################
# check_replicates()
######################

np.random.seed(42)

df_no_reps = pd.DataFrame({
    'variable' : ['1', '2', '3'],
    'value' : np.random.rand(3)
})

def test_no_reps():
    replicates, _ = utils.check_replicates(df_no_reps, 'variable', 'value', None)
    assert replicates is False
    
df_reps = pd.DataFrame({
    'variable' : ['1', '2', '3']*2,
    'value' : np.random.rand(6)
})
    
def test_reps():
    replicates, _ = utils.check_replicates(df_reps, 'variable', 'value', None)
    assert replicates is True
    
df_mean_is_2 = pd.DataFrame({
    'variable' : ['1', '2', '3']*2,
    'value' : [1, 1, 1, 3, 3, 3]
})
    
def test_replicate_mean():
    replicates, df_mean = utils.check_replicates(df_mean_is_2, 'variable', 'value', None)
    assert all(df_mean['Mean of value'] == [2]*6)