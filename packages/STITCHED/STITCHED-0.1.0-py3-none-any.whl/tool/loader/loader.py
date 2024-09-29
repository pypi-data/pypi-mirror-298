from tool.loader.formatter import DataFrameFormatter
from STITCHED.tool.loader.validator import Validator, read_dataframe

class DataLoader:
    def __init__(self, conn, validator):
        """
        Initializes the DataLoader with a validator object.
        :param validator: A validator object that validates the config and datasets.
        """
        assert isinstance(validator, Validator), "validator must be an instance of Validator"
        self.validator = validator
        self.conn = conn

    def _insert_data(self, df, table_name):
        df.to_sql(table_name, self.conn, if_exists='append', index=False)

    def storage_datasets(self):
        try:
            # Validate and fetch configuration
            config = self.validator.final_config()
        except Exception as e:
            # Catch any error that occurs during the config validation
            print(f"Error occurred during validation: {e}")
            return  # Abort the process if validation fails

        for index, row in config.iterrows():
            try:
                # Start a transaction for each row
                self.conn.execute("BEGIN")

                file_names = row['dataset_file_name'].split(';')
                first_iter = True
                converter = None
                formatted_df = None
                for file_name in file_names:
                    full_path = self.validator.data_folder + '/' + file_name.strip()
                    df = read_dataframe(full_path)
                    # create a new converter in the first iter
                    if first_iter:
                        # print(file_name, "first")
                        converter = DataFrameFormatter(row, df, self.conn)
                        formatted_df = converter.format_for_sql()
                        first_iter = False
                    else:
                        converter.set_df(df)
                        formatted_df = converter.format_for_sql(append=True)
                        # formatted_df = {key: pd.concat([formatted_df[key], new_formatted_df[key]], ignore_index=True) for key in formatted_df.keys()}
                    # for table_name, df in formatted_df.items():
                    # print(f"TABLE {table_name}:\n{df}")
                    # print("\n")
                    for table_name, df in formatted_df.items():
                        self._insert_data(df, table_name)
                    print(f"{file_name} Insertion Complete")

                # Commit the transaction for this row
                self.conn.commit()
                print(f"Row {index + 1}: Dataset(s) inserted successfully.")

            except Exception as e:
                # Rollback the transaction for the current row if any error occurs
                self.conn.rollback()
                print(f"Row {index + 1}: Error occurred: {e}. Transaction rolled back.")

        print("Data insertion process complete.")

# def insert_data(conn, df, table_name):
#     df.to_sql(table_name, conn, if_exists='append', index=False)
#     try:
#
#         df.to_sql(table_name, conn, if_exists='append', index=False)
#     except Exception as e:
#         print(f"TABLE {table_name}:\n{df}")
#         print(e)
#
#
# def storage_datasets(config):
#     for index, row in config.iterrows():
#         file_names = row['dataset_file_name'].split(';')
#         first_iter = True
#         converter = None
#         formatted_df = None
#         for file_name in file_names:
#             full_path = data_folder + '/' + file_name.strip()
#             df = read_dataframe(full_path)
#             # create a new converter in the first iter
#             if first_iter:
#                 # print(file_name, "first")
#                 converter = DataFrameFormatter(row, df, conn)
#                 formatted_df = converter.format_for_sql()
#                 first_iter = False
#             else:
#                 converter.set_df(df)
#                 formatted_df = converter.format_for_sql(append=True)
#                 # formatted_df = {key: pd.concat([formatted_df[key], new_formatted_df[key]], ignore_index=True) for key in formatted_df.keys()}
#             # for table_name, df in formatted_df.items():
#                 # print(f"TABLE {table_name}:\n{df}")
#                 # print("\n")
#             for table_name, df in formatted_df.items():
#                 insert_data(conn, df, table_name)
#                 conn.commit()
#
#             print(f"{file_name} Insertion Complete")
