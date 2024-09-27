# ForgeKit

**ForgeKit** is a Python package designed to simplify data manipulation, visualization, and basic machine learning tasks. Whether you're cleaning, transforming, or visualizing your data, **ForgeKit** provides an intuitive interface to make these processes faster and more efficient.

## Features

- **Data Display & Summarization**: Easily display and summarize DataFrames.
- **Data Cleaning & Transformation**: Handle missing data, remove outliers, scale data, and more.
- **Visualization**: Create static and interactive plots using Matplotlib and Plotly.
- **Machine Learning Utilities**: Perform K-Means clustering, evaluate feature importance, and split data into training and test sets.
- **Reporting**: Generate markdown reports from DataFrames.

## Installation

Install the package using pip:

```bash
pip install forgekit
```

For detailed setup instructions, see [INSTALL.md](INSTALL.md).

## Usage

Here's a simple example of **ForgeKit** in action. For a more comprehensive step-by-step workflow, refer to the `examples.py` file.

```python
import pandas as pd
import forgekit as fk

# Sample Data
data = {
    'A': [5, 8, 10, 15, 20],
    'B': [10, 20, 15, 10, 5],
    'C': ['red', 'blue', 'green', 'red', 'blue']
}
df = pd.DataFrame(data)

# Display DataFrame
fk.display_dataframe(df)

# Plot DataFrame
fk.plot_dataframe(df[['A', 'B']], kind='line', title="Sample Data Plot")

# Perform K-Means Clustering
df_clustered = fk.kmeans_clustering(df[['A', 'B']], n_clusters=2)
fk.display_dataframe(df_clustered)

# Generate a Markdown Report
fk.generate_report(df, file_name='report.md')
```

For more usage examples, see the `examples.py` file in the root directory, which includes:

- Data normalization and plotting
- Handling missing values
- K-Means clustering and more

## Key Functions in forgekit

Here is an overview of the most commonly used functions in **ForgeKit**:

### Data Display & Summarization
- `display_dataframe(dataframe, max_rows=10)`: Display a DataFrame with customizable row limits.
- `summary_stats(dataframe)`: Generate descriptive statistics for numerical columns.
- `custom_summary(dataframe)`: Display data types, missing values, and descriptive statistics in one output.

### Data Cleaning
- `impute_missing_data(dataframe, strategy='mean')`: Impute missing values using strategies like mean, median, or mode.
- `remove_outliers(dataframe, columns)`: Remove outliers from specified numerical columns using the IQR method.
- `remove_duplicates(dataframe)`: Remove duplicate rows from a DataFrame.
- `clean_text_columns(dataframe, columns)`: Clean text columns by removing whitespace and standardizing case.

### Data Transformation
- `minmax_scale(dataframe)`: Scale numerical data between 0 and 1.
- `standard_scale(dataframe)`: Standardize numerical data to have a mean of 0 and unit variance.
- `log_transform(dataframe, columns)`: Apply log transformations to reduce skewness in the data.
- `one_hot_encode(dataframe, columns)`: Perform one-hot encoding on categorical columns.

### Data Visualization
- `plot_dataframe(dataframe, kind='line', title)`: Generate static plots (e.g., line, bar, scatter) using Matplotlib.
- `interactive_plot(dataframe, x_col, y_col, kind='scatter', title)`: Create interactive plots using Plotly.

### Machine Learning Utilities
- `kmeans_clustering(dataframe, n_clusters=3)`: Perform K-Means clustering and add cluster labels to the DataFrame.
- `train_test_split_data(dataframe, target_column, test_size=0.2)`: Split data into training and test sets.
- `feature_importance(dataframe, target_column)`: Calculate feature importance using a RandomForest classifier.

### Reporting & Export
- `generate_report(dataframe, file_name='report.md')`: Generate a markdown report of the DataFrame with descriptive statistics.
- `export_csv(dataframe, file_name)`: Export a DataFrame to a CSV file.
- `load_csv(file_path)`: Load a CSV file into a DataFrame.

## Example Workflow

Here’s a brief example showing how you might use **ForgeKit** in a typical data analysis workflow. For the full script, check out the `examples.py` file.

```python
import pandas as pd
import forgekit as fk

# Step 1: Load data
df = pd.DataFrame({
    'A': [5, 8, 10, 15, 20],
    'B': [10, 20, 15, 10, 5],
    'C': ['red', 'blue', 'green', 'red', 'blue']
})

# Step 2: Display the DataFrame
fk.display_dataframe(df)

# Step 3: Summary statistics
fk.summary_stats(df)

# Step 4: Normalize numerical columns
df_normalized = fk.minmax_scale(df[['A', 'B']])

# Step 5: K-Means Clustering
df_clustered = fk.kmeans_clustering(df[['A', 'B']], n_clusters=2)

# Step 6: Plot results
fk.plot_dataframe(df_normalized, kind='line', title="Normalized Data")

# Step 7: Generate a markdown report
fk.generate_report(df, file_name='report.md')
```

This workflow demonstrates the ease of use of **ForgeKit** for quickly loading, transforming, visualizing, and analyzing data.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please feel free to open issues or pull requests if you'd like to add features, fix bugs, or improve documentation.
