import pandas as pd

def get_feature_description(col_name:str):
    """Takes a column name, reads the description csv and returns a print statement per the columns associated description.

    Args:
        col_name (str): column name as string. 
    """
    df = pd.read_csv('datasets/lending_club_info.csv')
    pd.set_option('display.max_colwidth', 300)

    print(df.loc[df['LoanStatNew'] == col_name, ['Description']])
    