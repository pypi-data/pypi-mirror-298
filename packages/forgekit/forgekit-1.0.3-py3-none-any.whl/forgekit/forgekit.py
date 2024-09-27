import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import sqlite3

class ForgeKit:
    
    # Display DataFrame
    @staticmethod
    def display_dataframe(dataframe, max_rows=10):
        """Displays a pandas DataFrame in the console, limiting the number of rows."""
        with pd.option_context('display.max_rows', max_rows):
            print(dataframe)

    # Plot DataFrame using Matplotlib
    @staticmethod
    def plot_dataframe(dataframe, kind='bar', title="Data Plot", figsize=(10, 6), save_path=None):
        """Plots a pandas DataFrame using matplotlib with options for saving."""
        dataframe.plot(kind=kind, figsize=figsize)
        plt.title(title)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        else:
            plt.show()

    # Export DataFrame to CSV
    @staticmethod
    def export_csv(dataframe, file_name="output.csv"):
        """Exports a pandas DataFrame to a CSV file."""
        dataframe.to_csv(file_name, index=False)
        print(f"Data exported to {file_name}")

    # Generate Summary Statistics
    @staticmethod
    def summary_stats(dataframe):
        """Prints a summary of statistical information of a pandas DataFrame."""
        print(dataframe.describe())

    # Load CSV into DataFrame
    @staticmethod
    def load_csv(file_path):
        """Loads a CSV file into a pandas DataFrame."""
        return pd.read_csv(file_path)

    # Normalize DataFrame
    @staticmethod
    def minmax_scale(dataframe):
        """Scales the DataFrame between 0 and 1."""
        return (dataframe - dataframe.min()) / (dataframe.max() - dataframe.min())

    # Standardize DataFrame
    @staticmethod
    def standard_scale(dataframe):
        """Standardizes the DataFrame (zero mean, unit variance)."""
        return (dataframe - dataframe.mean()) / dataframe.std()

    # Correlation Matrix
    @staticmethod
    def correlation_matrix(dataframe):
        """Generates and prints the correlation matrix for the DataFrame."""
        corr_matrix = dataframe.corr()
        print(corr_matrix)
        return corr_matrix

    # Custom Plot (Matplotlib)
    @staticmethod
    def custom_plot(dataframe, x_col, y_col, kind='scatter', title="Custom Plot", save_path=None):
        """Creates a customizable plot with options for saving."""
        dataframe.plot(kind=kind, x=x_col, y=y_col)
        plt.title(title)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print(f"Plot saved to {save_path}")
        else:
            plt.show()

    # Pivot Data
    @staticmethod
    def pivot_data(dataframe, index, columns, values):
        """Creates a pivot table."""
        return dataframe.pivot(index=index, columns=columns, values=values)

    # Melt Data
    @staticmethod
    def melt_data(dataframe, id_vars, value_vars):
        """Melts the DataFrame to long format."""
        return pd.melt(dataframe, id_vars=id_vars, value_vars=value_vars)

    # Remove Outliers
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

    # Merge DataFrames
    @staticmethod
    def merge_dataframes(df1, df2, how='inner', on=None):
        """Merges two DataFrames."""
        return pd.merge(df1, df2, how=how, on=on)

    # Join DataFrames
    @staticmethod
    def join_dataframes(df1, df2, how='left'):
        """Joins two DataFrames based on their indexes."""
        return df1.join(df2, how=how)

    # Custom Summary
    @staticmethod
    def custom_summary(dataframe):
        """Generates a custom summary with data types, missing values, and descriptive stats."""
        print("Data Types:")
        print(dataframe.dtypes)
        print("\nMissing Values:")
        print(dataframe.isnull().sum())
        print("\nDescriptive Statistics:")
        print(dataframe.describe())

    # Generate Report
    @staticmethod
    def generate_report(dataframe, file_name='report.md'):
        """Generates a markdown report of the DataFrame."""
        report = dataframe.describe().to_markdown()
        with open(file_name, 'w') as f:
            f.write("# Data Report\n\n")
            f.write(report)
        print(f"Report generated as {file_name}")

    # Rolling Average
    @staticmethod
    def rolling_average(dataframe, column, window=3):
        """Calculates the rolling average for a specific column."""
        return dataframe[column].rolling(window=window).mean()

    # Interactive Plot using Plotly
    @staticmethod
    def interactive_plot(dataframe, x_col, y_col, kind='scatter', title="Interactive Plot"):
        """Generates an interactive plot using Plotly."""
        if kind == 'scatter':
            fig = px.scatter(dataframe, x=x_col, y=y_col, title=title)
        elif kind == 'line':
            fig = px.line(dataframe, x=x_col, y=y_col, title=title)
        fig.show()

    # Load data from SQL database
    @staticmethod
    def load_from_sql(db_path, query):
        """Loads data from an SQL database."""
        conn = sqlite3.connect(db_path)
        return pd.read_sql_query(query, conn)

    # One-Hot Encoding
    @staticmethod
    def one_hot_encode(dataframe, columns):
        """One-hot encodes the specified categorical columns."""
        return pd.get_dummies(dataframe, columns=columns)

    # K-Means Clustering
    @staticmethod
    def kmeans_clustering(dataframe, n_clusters=3):
        """Performs K-Means clustering on the DataFrame and returns cluster labels."""
        model = KMeans(n_clusters=n_clusters)
        dataframe['cluster'] = model.fit_predict(dataframe)
        return dataframe

    # Train-Test Split
    @staticmethod
    def train_test_split_data(dataframe, target_column, test_size=0.2):
        """Splits the DataFrame into training and test sets."""
        X = dataframe.drop(columns=[target_column])
        y = dataframe[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        return X_train, X_test, y_train, y_test

    # Impute Missing Data
    @staticmethod
    def impute_missing_data(dataframe, strategy='mean'):
        """Imputes missing values in the DataFrame based on the specified strategy, only for numeric columns."""
        # Select only numeric columns
        numeric_columns = dataframe.select_dtypes(include=[np.number])

        # Apply the strategy only to the numeric columns
        if strategy == 'mean':
            dataframe[numeric_columns.columns] = numeric_columns.fillna(numeric_columns.mean())
        elif strategy == 'median':
            dataframe[numeric_columns.columns] = numeric_columns.fillna(numeric_columns.median())
        elif strategy == 'mode':
            dataframe[numeric_columns.columns] = numeric_columns.fillna(numeric_columns.mode().iloc[0])
        else:
            raise ValueError("Invalid strategy. Choose 'mean', 'median', or 'mode'.")

        return dataframe


    @staticmethod
    def impute_missing_data(dataframe, strategy='mean'):
        """Imputes missing values in the DataFrame based on the specified strategy."""
        if strategy == 'mean':
            return dataframe.fillna(dataframe.mean())
        elif strategy == 'median':
            return dataframe.fillna(dataframe.median())
        elif strategy == 'mode':
            return dataframe.fillna(dataframe.mode().iloc[0])
        else:
            raise ValueError("Invalid strategy. Choose 'mean', 'median', or 'mode'.")

    # Log Transformation
    @staticmethod
    def log_transform(dataframe, columns):
        """Applies log transformation to the specified columns."""
        for col in columns:
            dataframe[col] = np.log1p(dataframe[col])
        return dataframe

    # Feature Importance
    @staticmethod
    def feature_importance(dataframe, target_column):
        """Computes feature importance using a Random Forest classifier."""
        X = dataframe.drop(columns=[target_column])
        y = dataframe[target_column]
        
        model = RandomForestClassifier()
        model.fit(X, y)
        
        importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        print("Feature importance:\n", importance)
        return importance

    # Remove duplicates
    @staticmethod
    def remove_duplicates(dataframe):
        """Removes duplicate rows from the DataFrame."""
        cleaned_df = dataframe.drop_duplicates()
        print(f"Removed {dataframe.shape[0] - cleaned_df.shape[0]} duplicates.")
        return cleaned_df

    # Missing Data Report
    @staticmethod
    def missing_data_report(dataframe):
        """Returns a report showing the percentage of missing data for each column."""
        missing_report = dataframe.isnull().mean() * 100
        missing_report = missing_report[missing_report > 0].sort_values(ascending=False)
        print(f"Missing data report:\n{missing_report}")
        return missing_report

    # Clean Text Columns
    @staticmethod
    def clean_text_columns(dataframe, columns):
        """Cleans text-based columns by stripping whitespace and correcting cases."""
        for col in columns:
            dataframe[col] = dataframe[col].str.strip().str.lower()
        return dataframe

    # Replace Invalid Values
    @staticmethod
    def replace_invalid_values(dataframe, column, invalid_values, replacement=None):
        """Replaces or drops invalid values from a specific column."""
        if replacement is None:
            cleaned_df = dataframe[~dataframe[column].isin(invalid_values)]
            print(f"Removed {dataframe.shape[0] - cleaned_df.shape[0]} invalid values from {column}.")
            return cleaned_df
        else:
            dataframe[column] = dataframe[column].replace(invalid_values, replacement)
            print(f"Replaced invalid values in {column} with {replacement}.")
            return dataframe

    # Drop Columns with High Percentage of Missing Data
    @staticmethod
    def drop_high_missing_columns(dataframe, threshold=50):
        """Drops columns that have more than the specified threshold percentage of missing values."""
        missing_report = dataframe.isnull().mean() * 100
        columns_to_drop = missing_report[missing_report > threshold].index
        cleaned_df = dataframe.drop(columns=columns_to_drop)
        print(f"Dropped columns with more than {threshold}% missing data: {list(columns_to_drop)}")
        return cleaned_df

