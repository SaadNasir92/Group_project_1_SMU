import pandas as pd
import os
def get_feature_description(col_name:str):
    """Takes in a column name and prints the description of the column. 

    Args:
        col_name (str): _description_
    """
    df = pd.read_csv('datasets/lending_club_info.csv')
    pd.set_option('display.max_colwidth', 300)

    print(df.loc[df['LoanStatNew'] == col_name, ['Description']])
    