import pandas as pd
import os
import re

# define the folder containing the csv files
folder_name = "./raw data/"

# create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


# function to read all csv files in a folder and concatenate them into a single dataframe
def read_csv_files_and_concatenate(folder_path):
    # get a list of all the files in the folder
    files = os.listdir(folder_path)

    # filter the list to include only csv files
    csv_files = [file for file in files if file.endswith('.csv')]

    # initialize an empty dataframe to store the concatenated data
    combined_df = pd.DataFrame()

    # iterate through the csv files
    for csv_file in csv_files:
        # construct the file path for the current csv file
        file_path = os.path.join(folder_path, csv_file)

        # read the csv file into a pandas dataframe
        df = pd.read_csv(file_path)

        # concatenate the current dataframe with the combined dataframe
        combined_df = pd.concat([combined_df, df], axis=0)

    return combined_df

# function to convert camel case to snake case
def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# call the function to read csv files and concatenate them into a single dataframe
combined_df = read_csv_files_and_concatenate(folder_name)
print(combined_df)

# apply the camel_to_snake function to each column name and replace 'iuCount' with 'insured_units'
new_column_names = [camel_to_snake(column) if column != 'iuCount' else 'insured_units' for column in combined_df.columns]

# update the dataframe column names
combined_df.columns = new_column_names

# remove unrequired columns
combined_df = combined_df.drop(columns=['updated_at'])


# print the updated dataframe and check if correct data types exist:


print(combined_df)
print(combined_df.dtypes)
combined_df['state_name'] = combined_df['state_name'].astype(str)

# save csv
folder_name = "./cleaned data/"

# create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

combined_df.to_csv(os.path.join(folder_name, "combined_data.csv"), index=False)
print("consolidated file saved")
