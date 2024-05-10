import pandas as pd
import numpy as np

def get_feature_description(col_name:str):
    """Takes a column name, reads the description csv and returns a print statement per the columns associated description.

    Args:
        col_name (str): column name as string. 
    """
    df = pd.read_csv('datasets/lending_club_info.csv')
    pd.set_option('display.max_colwidth', 300)

    print(df.loc[df['LoanStatNew'] == col_name, ['Description']])
    

def cliffs_delta(x, y):
    """
        Calculate Cliff's Delta, a measure of effect size that quantifies the amount of difference
        between two groups of observations beyond p-value significance levels. It provides a measure
        of how often the values in one distribution are larger than the values in the second distribution.

        Parameters:
        x (list, array, or series): Numeric data representing the first group.
        y (list, array, or series): Numeric data representing the second group.

        Returns:
        float: The calculated Cliff's Delta value. The value ranges from -1 to 1, where:
            - 1 indicates all values in x are greater than all values in y,
            - -1 indicates all values in y are greater than all values in x,
            - 0 indicates the distributions are identical.

        Methodology:
        - n_x: Number of observations in the first group. Using numpy array to reduce loops and increase run-time
        - n_y: Number of observations in the second group. Using numpy array to reduce loops and increase run-time
        - n_total: Total number of comparisons (n_x multiplied by n_y).
        - n_greater: Count of cases where an element in x is greater than an element in y.
        - n_less: Count of cases where an element in x is less than an element in y.
        
        The formula used is: (n_greater - n_less) / n_total, which quantifies the probability of a value
        from x exceeding a value from y minus the probability of a value from y exceeding a value from x.
    """
    
    x, y = np.array(x), np.array(y)
    n_x, n_y = len(x), len(y)
    n_total = n_x * n_y
    n_greater = np.sum(np.greater.outer(x, y))
    n_less = np.sum(np.less.outer(x, y))
    return (n_greater - n_less) / n_total