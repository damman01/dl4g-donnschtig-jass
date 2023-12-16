import pandas as pd

# Load the data
# df = pd.read_csv('x_train.csv')

# Calculate min and max for each column
# ranges = df.agg(['min', 'max']).transpose()

# Save the ranges to a CSV file
# ranges.to_csv('feature_ranges.csv', header=True)


# Load the data
df = pd.read_csv('feature_ranges.csv', index_col=0)

# Convert the DataFrame to a dictionary
feature_ranges = df.transpose().to_dict('list')

print(feature_ranges)

