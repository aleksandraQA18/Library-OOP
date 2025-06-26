import pandas as pd
from tabulate import tabulate


class CSVDataManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath)

    def print_df_results(self, df: pd.DataFrame, columns: list) -> None:
        """
        Prints the specified columns of a pandas DataFrame in a formatted table.
        Args:
            df (pd.DataFrame): The DataFrame to display.
            columns (list): List of column names to include in the output.
        Returns:
            None
        """
        try:
            df_dict = df[columns].to_dict("records")
            print(tabulate(df_dict, headers="keys", tablefmt="pretty"))
        except KeyError as e:
            print("KeyError:", e)

    def get_rows_by_index(self, index: list) -> pd.DataFrame | None:
        """
        Retrieve rows from the DataFrame based on the provided list of indices.
        Args:
            index (list): A list of indices specifying which rows to retrieve from the DataFrame.
        Returns:
            pd.DataFrame | None: A DataFrame containing the selected rows if the indices are valid, otherwise None.
        """

        row_df = self.df.loc[index]
        return row_df

    def get_data_from_column(self, index: str, column_name: str):
        """
        Retrieve data from a specific column and row in the DataFrame.
        Args:
            index (str): The index (row label) from which to retrieve the data.
            column_name (str): The name of the column from which to retrieve the data.
        Returns:
            Any: The value located at the specified row and column in the DataFrame.
        """

        return self.df.loc[index, column_name]

    def save_to_csv(self) -> None:
        """
        Saves the current DataFrame to a CSV file at the specified filepath.
        """

        self.df.to_csv(self.filepath, index=False)

    def match_data(self, column_name: str, data: str) -> pd.DataFrame | None:
        """
        Searches for rows in the DataFrame where the specified column contains the given substring (case-insensitive).
        Args:
            column_name (str): The name of the column to search within.
            data (str): The substring to search for in the specified column.
        Returns:
            pd.DataFrame | None: A DataFrame containing the matching rows, or None if no matches are found.
        """

        results_df = self.df[self.df[column_name].str.contains(data, case=False)]
        return results_df

    def search_exact_data(self, column_name: str, data: str) -> pd.DataFrame | None:
        """
        Searches for rows in the DataFrame where the specified column matches the given data exactly.
        Args:
            column_name (str): The name of the column to search in.
            data (str): The exact value to match in the specified column.
        Returns:
            pd.DataFrame | None: A DataFrame containing all rows where the column matches the data exactly.
        """

        results_df = self.df[self.df[column_name] == data]
        return results_df

    def update_df(self, index, column_name: str, new_data: str) -> None:
        """
        Updates a specific cell in the DataFrame at the given index and column with new data,
        then saves the updated DataFrame to the CSV file.
        Args:
            index: The index (row label) of the DataFrame to update.
            column_name (str): The name of the column to update.
            new_data (str): The new value to set in the specified cell.
        """

        try:
            self.df.at[index, column_name] = new_data
            self.save_to_csv()
        except KeyError:
            print(
                f"KeyError: Index '{index}' or column '{column_name}' does not exist."
            )
        except Exception as e:
            print("An error eccured ", e)
