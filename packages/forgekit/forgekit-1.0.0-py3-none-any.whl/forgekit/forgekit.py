import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class ForgeKit:
    """A collection of handy tools for efficient data handling, visualization, and reporting."""

    # ---------------- Data Display and Summary ---------------- #

    @staticmethod
    def display_dataframe(dataframe, max_rows=10):
        """Displays a pandas DataFrame in the console with row limit for better readability."""
        with pd.option_context('display.max_rows', max_rows):
            print(dataframe)

    @staticmethod
    def summary_stats(dataframe):
        """Prints basic summary statistics of the DataFrame."""
        print(dataframe.describe())

    @staticmethod
    def custom_summary(dataframe):
        """Generates a custom summary with data types, missing values, and descriptive stats."""
        print(f"Data Types:\n{dataframe.dtypes}\n")
        print(f"Missing Values:\n{dataframe.isnull().sum()}\n")
        print(f"Descriptive Statistics:\n{dataframe.describe()}\n")

    # ---------------- Data I/O Operations ---------------- #

    @staticmethod
    def export_csv(dataframe, file_name="output.csv"):
        """Exports a pandas DataFrame to a CSV file."""
        dataframe.to_csv(file_name, index=False)
        print(f"Data exported to {file_name}")

    @staticmethod
    def load_csv(file_path):
        """Loads a CSV file into a pandas DataFrame."""
        return pd.read_csv(file_path)

    @staticmethod
    def load_large_csv(file_path, chunksize=10000):
        """Loads a large CSV file in chunks for better memory management."""
        for chunk in pd.read_csv(file_path, chunksize=chunksize):
            yield chunk  # Process each chunk as needed

    @staticmethod
    def load_from_sql(db_path, query):
        """Loads data from an SQL database using sqlite3."""
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query(query, conn)

    # ---------------- Missing Data Handling ---------------- #

    @staticmethod
    def impute_missing_data(dataframe, strategy='mean', fill_value=None):
        """Fills missing values using different strategies (mean, median, mode, or constant)."""
        if strategy == 'constant' and fill_value is None:
            raise ValueError("A fill_value must be provided for 'constant'.")
        strategies = {
            'mean': dataframe.fillna(dataframe.mean(), inplace=False),
            'median': dataframe.fillna(dataframe.median(), inplace=False),
            'mode': dataframe.fillna(dataframe.mode().iloc[0], inplace=False),
            'constant': dataframe.fillna(fill_value, inplace=False)
        }
        return strategies.get(strategy, dataframe)

    @staticmethod
    def drop_high_missing_columns(dataframe, threshold=50):
        """Drops columns with missing values greater than the specified threshold percentage."""
        missing_report = dataframe.isnull().mean() * 100
        columns_to_drop = missing_report[missing_report > threshold].index
        print(f"Dropping columns with >{threshold}% missing data: {list(columns_to_drop)}")
        return dataframe.drop(columns=columns_to_drop)

    @staticmethod
    def missing_data_report(dataframe):
        """Generates a report on missing data for each column, showing percentages."""
        missing_report = dataframe.isnull().mean() * 100
        return missing_report[missing_report > 0].sort_values(ascending=False)

    # ---------------- Data Cleaning ---------------- #

    @staticmethod
    def remove_duplicates(dataframe):
        """Removes duplicate rows from the DataFrame to optimize memory and processing."""
        return dataframe.drop_duplicates()

    @staticmethod
    def remove_outliers(dataframe, columns):
        """Removes outliers from specific columns using the IQR method."""
        for col in columns:
            Q1 = dataframe[col].quantile(0.25)
            Q3 = dataframe[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            dataframe = dataframe[(dataframe[col] >= lower_bound) & (dataframe[col] <= upper_bound)]
        return dataframe

    @staticmethod
    def clean_text_columns(dataframe, columns):
        """Cleans text-based columns by stripping whitespace and converting to lowercase."""
        for col in columns:
            dataframe[col] = dataframe[col].str.strip().str.lower()
        return dataframe

    @staticmethod
    def replace_invalid_values(dataframe, column, invalid_values, replacement=None):
        """Replaces or drops invalid values from a specified column."""
        if replacement is None:
            return dataframe[~dataframe[column].isin(invalid_values)]
        return dataframe.replace({column: {v: replacement for v in invalid_values}})

    # ---------------- Data Transformation ---------------- #

    @staticmethod
    def minmax_scale(dataframe):
        """Scales the DataFrame between 0 and 1 for all numerical columns."""
        return (dataframe - dataframe.min()) / (dataframe.max() - dataframe.min())

    @staticmethod
    def standard_scale(dataframe):
        """Standardizes the DataFrame to have zero mean and unit variance for all numerical columns."""
        return (dataframe - dataframe.mean()) / dataframe.std()

    @staticmethod
    def log_transform(dataframe, columns):
        """Applies log transformation to specified columns to reduce data skew."""
        for col in columns:
            dataframe[col] = np.log1p(dataframe[col])
        return dataframe

    # ---------------- Data Visualization ---------------- #

    @staticmethod
    def plot_dataframe(dataframe, kind='bar', title="Data Plot", figsize=(10, 6), save_path=None):
        """Plots a pandas DataFrame using matplotlib, with options to save."""
        dataframe.plot(kind=kind, figsize=figsize)
        plt.title(title)
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        else:
            plt.show()

    @staticmethod
    def interactive_plot(dataframe, x_col, y_col, kind='scatter', title="Interactive Plot"):
        """Generates an interactive plot using Plotly."""
        plot_funcs = {
            'scatter': px.scatter,
            'line': px.line
        }
        fig = plot_funcs[kind](dataframe, x=x_col, y=y_col, title=title)
        fig.show()

    # ---------------- Machine Learning Related ---------------- #

    @staticmethod
    def kmeans_clustering(dataframe, n_clusters=3):
        """Performs K-Means clustering on the DataFrame and returns cluster labels."""
        model = KMeans(n_clusters=n_clusters)
        dataframe['cluster'] = model.fit_predict(dataframe)
        return dataframe

    @staticmethod
    def train_test_split_data(dataframe, target_column, test_size=0.2):
        """Splits the DataFrame into training and test sets for model training."""
        X = dataframe.drop(columns=[target_column])
        y = dataframe[target_column]
        return train_test_split(X, y, test_size=test_size)

    @staticmethod
    def feature_importance(dataframe, target_column):
        """Computes feature importance using a Random Forest classifier."""
        X = dataframe.drop(columns=[target_column])
        y = dataframe[target_column]
        model = RandomForestClassifier()
        model.fit(X, y)
        importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        print(f"Feature importance:\n{importance}")
        return importance
