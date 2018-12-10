import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath,categories_filepath):
    """
    Loads data from the .csv files for messages and categories and merge 
    the two datasets into one DataFrame. Returns the merged DataFrame
    """
    messages = pd.read_csv(messages_filepath)
    messages = messages.drop_duplicates()   
    messages = messages[np.logical_not(messages['message'].duplicated())]
    
    categories = pd.read_csv(categories_filepath)
    categories = categories.drop_duplicates()
    categories = categories[np.logical_not(categories['id'].duplicated())]
    
    df = pd.merge(messages, categories, how = 'left', on = 'id')
    return df


def clean_data(df):
    """
    Creates category columns and extracts the boolean values for each columns.
    Cleans the DataFrame and returns the DataFrame with the new catetory columns.
    """
    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(';', expand=True)
    
    # select the first row of the categories dataframe
    row = categories.iloc[0]

    # use this row to extract a list of new column names for categories.
    # one way is to apply a lambda function that takes everything 
    # up to the second to last character of each string with slicing
    category_colnames = row.apply(lambda s: s[:-2])
    
    # rename the columns of `categories`
    categories.columns = category_colnames   
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
        # convert column from string to numeric
        categories[column] = categories[column].astype('int32')
        # Replace values greater than 1 with 1
        categories[column].loc[categories[column] > 1] = 1
        
    # drop the original categories column from `df`
    df = df.drop("categories", axis = 1)  
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis = 1)
    
    return df


def save_data(df, database_name):
    """
    Save the DataFrame into a SQLite database.
    """
    engine = create_engine('sqlite:///'+ database_name)
    df.to_sql("table1", engine, index=False)  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_name= sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)
        
        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_name))
        save_data(df, database_name)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')
              


if __name__ == '__main__':
    main()