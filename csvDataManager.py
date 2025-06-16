import pandas as pd
from tabulate import tabulate


class CSVDataManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath)

    def get_csv_columns(self, columns):
        return self.df[columns]

    def print_df_data(self, columns):
        df_dict = self.get_csv_columns(columns).drop_duplicates().to_dict("records")
        print(tabulate(df_dict, headers="keys", tablefmt="pretty"))

    def get_row_by_index(self, index):
        try:
            return self.df.loc[index]
        except KeyError:
            print("Check if index is set for a data frame (check set_index() method")

    def get_all_data_by_index(self, index):
        try:
            return self.df.loc[[index]]
        except KeyError:
            print("Check if index is set for a data frame (check set_index() method")

    def save_to_csv(self):
        self.df.to_csv(self.filepath, index=False)

    def search_data(self, column_name, data):
        results_df = self.df[self.df[column_name].str.contains(data, case=False)]
        return results_df

    def update_cell(self, index, column_name, new_data):
        self.df.at[index, column_name] = str(new_data)
        self.save_to_csv()
