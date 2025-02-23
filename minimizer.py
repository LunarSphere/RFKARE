
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

# read ij matrix
mat = pd.read_csv('ijmatrix.csv')

num_rows = 10
num_cols = 13

heatmap_data = mat.pivot(index='i', columns='j', values='price')

# Display heatmap
seaborn.heatmap(heatmap_data, cmap='coolwarm', annot=True, fmt='d', cbar=False)
plt.title('Price Heatmap')
plt.xlabel('Column')
plt.ylabel('Row')
plt.show()