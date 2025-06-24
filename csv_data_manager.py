import pandas as pd
from tabulate import tabulate


class CSVDataManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath)

    def print_df_results(self, df: pd.DataFrame, columns: list) -> None:
        """
        Prints the specified columns of a pandas DataFrame in a formatted table.
        """
        try:
            df_dict = df[columns].to_dict("records")
            print(tabulate(df_dict, headers="keys", tablefmt="pretty"))
        except KeyError as e:
            print("KeyError:", e)

    def get_row_by_index(self, index: str) -> dict | None:
        """
        Retrieve a row from the DataFrame by its index and return as a list of dictionaries.
        """
        row_df = self.df.loc[[index]]
        return row_df.to_dict("records")[0]

    def save_to_csv(self) -> None:
        self.df.to_csv(self.filepath, index=False)

    def match_data(self, column_name: str, data: str) -> pd.DataFrame | None:
        """Search for rows where the given column contains the data (case-insensitive)."""
        results_df = self.df[self.df[column_name].str.contains(data, case=False)]
        return results_df

    def search_exact_data(self, column_name: str, data: str) -> pd.DataFrame | None:
        """Search for rows where the given column are equal to the data (case-sensitive)."""
        results_df = self.df[self.df[column_name] == data]
        return results_df

    def update_csv(self, index, column_name: str, new_data: str) -> None:
        """Update CSV file with new data."""
        try:
            self.df.at[index, column_name] = new_data
            self.save_to_csv()
        except KeyError:
            print(
                f"KeyError: Index '{index}' or column '{column_name}' does not exist."
            )
        except Exception as e:
            print("An error eccured ", e)
