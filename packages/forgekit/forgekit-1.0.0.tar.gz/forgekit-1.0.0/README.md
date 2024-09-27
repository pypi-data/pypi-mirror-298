# forgekit

**forgekit** is a python3 package designed to simplify data handling, visualization, and reporting. It provides a wide range of functions for cleaning, transforming, visualizing data, and performing machine learning tasks.

## Features

- Display and summarize DataFrames
- Export and load CSV files
- Handle missing data, outliers, and invalid values
- Data scaling and transformation (min-max scaling, standardization, log transformation)
- Generate interactive and static plots (matplotlib and Plotly)
- Machine learning utilities (K-Means clustering, feature importance calculation, train-test splitting)

## Installation

You can install **forgekit** by cloning the repository and installing it locally.

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/forgekit.git
   ```

2. Navigate to the package directory and install it:

   ```bash
   cd forgekit
   pip3 install .
   ```

3. Alternatively, install dependencies directly from `requirements.txt`:

   ```bash
   pip3 install -r requirements.txt
   ```

## Usage

Here’s an example of how to use **forgekit**:

```python
import pandas as pd
from forgekit import ForgeKit

# Sample data
data = {
    'Domain': ['example.com', 'example.net'],
    'Price': [10.0, 12.5]
}
df = pd.DataFrame(data)

# Display the DataFrame
ForgeKit.display_dataframe(df)

# Plot the DataFrame
ForgeKit.plot_dataframe(df, kind='bar', title="Domain Prices")
```

## Available Functions

### Data Display and Summarization:
- `display_dataframe()`: Display a DataFrame with a row limit.
- `summary_stats()`: Show summary statistics of a DataFrame.
- `custom_summary()`: Show a custom summary of data types, missing values, and statistics.

### Data Cleaning:
- `impute_missing_data()`: Handle missing values with strategies like mean, median, mode, or a constant value.
- `remove_outliers()`: Remove outliers using the IQR method.
- `remove_duplicates()`: Remove duplicate rows in the DataFrame.
- `clean_text_columns()`: Clean text columns by stripping whitespace and converting to lowercase.

### Data Transformation:
- `minmax_scale()`: Scale numerical data between 0 and 1.
- `standard_scale()`: Standardize numerical data to have zero mean and unit variance.
- `log_transform()`: Apply log transformation to reduce skewness.

### Data Visualization:
- `plot_dataframe()`: Generate static plots using matplotlib.
- `interactive_plot()`: Generate interactive plots using Plotly.

### Machine Learning Tools:
- `kmeans_clustering()`: Perform K-Means clustering on the DataFrame.
- `train_test_split_data()`: Split the DataFrame into training and test sets.
- `feature_importance()`: Calculate feature importance using a Random Forest classifier.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues or pull requests if you would like to contribute!
