from .forgekit import ForgeKit

# Expose all functions at the package level
display_dataframe = ForgeKit.display_dataframe
plot_dataframe = ForgeKit.plot_dataframe
export_csv = ForgeKit.export_csv
summary_stats = ForgeKit.summary_stats
load_csv = ForgeKit.load_csv
minmax_scale = ForgeKit.minmax_scale  # Correct function for normalization
standard_scale = ForgeKit.standard_scale
correlation_matrix = ForgeKit.correlation_matrix
custom_plot = ForgeKit.custom_plot
remove_outliers = ForgeKit.remove_outliers
pivot_data = ForgeKit.pivot_data
melt_data = ForgeKit.melt_data
merge_dataframes = ForgeKit.merge_dataframes
join_dataframes = ForgeKit.join_dataframes
custom_summary = ForgeKit.custom_summary
generate_report = ForgeKit.generate_report
rolling_average = ForgeKit.rolling_average
interactive_plot = ForgeKit.interactive_plot
load_from_sql = ForgeKit.load_from_sql
one_hot_encode = ForgeKit.one_hot_encode
kmeans_clustering = ForgeKit.kmeans_clustering
train_test_split_data = ForgeKit.train_test_split_data
impute_missing_data = ForgeKit.impute_missing_data
log_transform = ForgeKit.log_transform
feature_importance = ForgeKit.feature_importance
remove_duplicates = ForgeKit.remove_duplicates
missing_data_report = ForgeKit.missing_data_report
clean_text_columns = ForgeKit.clean_text_columns
replace_invalid_values = ForgeKit.replace_invalid_values
drop_high_missing_columns = ForgeKit.drop_high_missing_columns
