import pandas as pd
import os
import json
import argparse
from abc import ABC, abstractmethod

class Validator(ABC):
    """
    Abstract base class for config validation.
    """
    def __init__(self, config_file, data_folder):
        self.config_file = config_file
        self.data_folder = data_folder
    @abstractmethod
    def final_config(self):
        pass

class ConfigValidator(Validator):
    def strip_comma_from_text_list(self,orig_list):
        res = []
        for val in orig_list:
            # if ',' in val:
            if ';' in val:
                # Split the string by comma
                strip_list = [item.strip() for item in val.split(';') if item.strip()]
                res = res + strip_list
            else:
                # If no commas, keep the string as is
                res.append(val)
        return res

    def is_columns_in_datasets(self, df, col_list):
        cols_not_in_dataset = list(set(col_list) - set(df.columns))
        assert len(cols_not_in_dataset) == 0, f"In the list provided, {cols_not_in_dataset} are not found in the given dataset"

    def read_dataframe(self, file_path):
        """
        Read a DataFrame from a CSV or TSV file.

        Args:
        - file_path (str): Path to the file.

        Returns:
        - pandas.DataFrame: DataFrame containing the data from the file.
        """
        if file_path.endswith('.csv'):
            # Read CSV file
            df = pd.read_csv(file_path, encoding_errors='replace')
        elif file_path.endswith('.tsv'):
            # Read TSV file
            df = pd.read_csv(file_path, sep='\t')
        else:
            # Unsupported file type
            raise ValueError("Unsupported file type. Only CSV and TSV files are supported.")

        return df

    def read_and_prepare_config(self, filepath):
        """Reads the configuration CSV file and prepares the dataframe."""
        # df_config = pd.read_csv(filepath, sep=';', encoding="utf-8")
        df_config = pd.read_csv(filepath, encoding="utf-8")
        df_config = df_config.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df_config['label_name_definition'] = df_config['label_name_definition'].apply(lambda x: json.loads(x))
        return df_config

    def verify_file_integrity(self, df_config, folder_path):
        """Checks if all files listed in config are present in the folder."""
        folder_path_file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        config_file_names = self.strip_comma_from_text_list(df_config['dataset_file_name'].tolist())
        assert len(config_file_names) <= len(folder_path_file_names), \
            f"Number of datasets listed in Config ({len(config_file_names)}) exceeds that in the folder {len(folder_path_file_names)}."
        difference_datasets = set(config_file_names) - set(folder_path_file_names)
        assert len(difference_datasets) == 0, f"Dataset(s) {difference_datasets} not found in 'data' folder"
        print("Filename integrity check complete!")

    def validate_datasets(self, df_config, folder_path):
        """Validates that each dataset contains the required columns."""
        for idx, row in df_config.iterrows():
            datasets = self.strip_comma_from_text_list([row['dataset_file_name']])
            for dataset in datasets:
                df = self.read_dataframe(os.path.join(folder_path, dataset))
                col_list = list(row['label_name_definition'].keys()) + [row['text']]
                if not row['language'].startswith('@'):
                    col_list.append(row['language'])
                if isinstance(row['source'], str):
                    if not row['source'].startswith('@'):
                        col_list.append(row['source'])

                self.is_columns_in_datasets(df, col_list)

    def final_config(self):
        df_config = self.read_and_prepare_config(self.config_file)
        self.verify_file_integrity(df_config, self.data_folder)
        self.validate_datasets(df_config, self.data_folder)
        return df_config

# def strip_comma_from_text_list(orig_list):
#     res = []
#     for val in orig_list:
#         # if ',' in val:
#         if ';' in val:
#             # Split the string by comma
#             strip_list = [item.strip() for item in val.split(';') if item.strip()]
#             res = res + strip_list
#         else:
#             # If no commas, keep the string as is
#             res.append(val)
#     return res
#
#
# def is_columns_in_datasets(df, col_list):
#     cols_not_in_dataset = list(set(col_list) - set(df.columns))
#     assert len(cols_not_in_dataset) == 0, f"In the list provided, {cols_not_in_dataset} are not found in the given dataset"
#
#
def read_dataframe(file_path):
    """
    Read a DataFrame from a CSV or TSV file.

    Args:
    - file_path (str): Path to the file.

    Returns:
    - pandas.DataFrame: DataFrame containing the data from the file.
    """
    if file_path.endswith('.csv'):
        # Read CSV file
        df = pd.read_csv(file_path, encoding_errors='replace')
    elif file_path.endswith('.tsv'):
        # Read TSV file
        df = pd.read_csv(file_path, sep='\t')
    else:
        # Unsupported file type
        raise ValueError("Unsupported file type. Only CSV and TSV files are supported.")

    return df
#
#
# def read_and_prepare_config(filepath):
#     """Reads the configuration CSV file and prepares the dataframe."""
#     # df_config = pd.read_csv(filepath, sep=';', encoding="utf-8")
#     df_config = pd.read_csv(filepath, encoding="utf-8")
#     df_config = df_config.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
#     df_config['label_name_definition'] = df_config['label_name_definition'].apply(lambda x: json.loads(x))
#     return df_config
#
# def verify_file_integrity(df_config, folder_path):
#     """Checks if all files listed in config are present in the folder."""
#     folder_path_file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
#     config_file_names = strip_comma_from_text_list(df_config['dataset_file_name'].tolist())
#     assert len(config_file_names) <= len(folder_path_file_names), \
#         f"Number of datasets listed in Config ({len(config_file_names)}) exceeds that in the folder {len(folder_path_file_names)}."
#     difference_datasets = set(config_file_names) - set(folder_path_file_names)
#     assert len(difference_datasets) == 0, f"Dataset(s) {difference_datasets} not found in 'data' folder"
#     print("Filename integrity check complete!")
#
#
# def validate_datasets(df_config, folder_path):
#     """Validates that each dataset contains the required columns."""
#     for idx, row in df_config.iterrows():
#         datasets = strip_comma_from_text_list([row['dataset_file_name']])
#         for dataset in datasets:
#             df = read_dataframe(os.path.join(folder_path, dataset))
#             col_list = list(row['label_name_definition'].keys()) + [row['text']]
#             if not row['language'].startswith('@'):
#                 col_list.append(row['language'])
#             if isinstance(row['source'], str):
#                 if not row['source'].startswith('@'):
#                     col_list.append(row['source'])
#
#             is_columns_in_datasets(df, col_list)

def validate_config(config_path, data_folder):
    validator = Validator(config_path, data_folder)
    return validator.final_config()


# config_path = "config.csv"
config_path = "../../../Archive/config_new.csv"
data_folder = "./data"
# aaa = final_config(config_path, data_folder)

def main():
    parser = argparse.ArgumentParser(description= "Command line checking config legitimacy")
    parser.add_argument("--config_path", type=str, required=True, help="Path to config file")
    parser.add_argument("--data_folder_path", type=str, required=True, help="Path to data folder")
    args = parser.parse_args()

    validate_config(args.config_path, args.data_folder_path)
# To convert .parquet to .csv
# import datasets 
# dataset = datasets.load_dataset('ucberkeley-dlab/measuring-hate-speech', 'binary')   
# df = dataset['train'].to_pandas()
# df.describe()
# df.to_csv('measuring-hate-speech.csv', index = False)




# df_config =  pd.read_csv("config.csv", sep=';',encoding= "utf-8").apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# df_config


# folder_path = "./data"
# folder_path_file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
# folder_path_file_names

if __name__ == "__main__":
    '''
    CommandLine:
    python validator.py --config_path config_new.csv --data_folder_path ./data
    '''
    main()

# config_file_name_value = df_config.dataset_file_name.tolist()

# config_file_names =  strip_comma_from_text_list(config_file_name_value)
# config_file_names


# assert len(config_file_names) <= len(folder_path_file_names), f"Number of datasets listed in Config ({len(config_file_names)}) exceeds that in the folder {len(df_config)}."

# difference_datasets = set(config_file_names) - set(folder_path_file_names)
# assert len(difference_datasets) == 0, f"Dataset(s) {difference_datasets} not found in 'data' folder"
# df_config.label_name_definition = df_config.label_name_definition.apply(lambda x: json.loads(x))
# print("Filename integrity check complete!")


# for idx, row in df_config.iterrows():
#     datasets = strip_comma_from_text_list([row.dataset_file_name])
#     for dataset in datasets:
#         df = read_dataframe(folder_path + '/' + dataset)
#         col_list = list(row.label_name_definition.keys()) + [row.text]
#         if row.language.startswith('@') == False:
#             col_list.append(row.language)
#         if row.source.startswith('@') == False:
#             col_list.append(row.source)

#         print(col_list)
#         is_columns_in_datasets(df, col_list)
        
        
# def to_do(df):
#     return