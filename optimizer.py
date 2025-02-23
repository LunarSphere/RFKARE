import numpy as np
import pandas as pd
from gekko import GEKKO

data = pd.read_csv("ijmatrix.csv")

n_rows = data['i'].max() * 2 + 1
n_cols = data['j'].max() * 2 + 1

new_i = np.arange(0, 2*n_rows + 1)
new_j = np.arange(0, 2*n_cols + 1)

new_df = pd.MultiIndex.from_product([new_i, new_j], names=['i', 'j']).to_frame(index=False)
new_df['orig_i'] = new_df['i'] // 2
new_df['orig_j'] = new_df['j'] // 2

df_renamed = data.rename(columns={'i': 'orig_i', 'j': 'orig_j'})
new_df = new_df.merge(df_renamed, on=['orig_i', 'orig_j'], how='left')
new_df['isValid'] = new_df['isValid'].fillna(0).astype(int)

new_df = new_df.drop(columns=['orig_i', 'orig_j'])
new_df = new_df[['price', 'isValid', 'i', 'j']]

# Corrected price averaging using .loc and original price values
new_df['priceAvg'] = 0.0  # Initialize as float
for i in new_df['i'].unique():
    for j in new_df['j'].unique():
        total = 0.0
        count = 0
        for di, dj in [(0,0), (0,1), (0,-1), (1,0), (-1,0)]:
            ni = i + di
            nj = j + dj
            if ni in new_df['i'].values and nj in new_df['j'].values:
                total += new_df[(new_df['i'] == ni) & (new_df['j'] == nj)]['price'].values[0]
                count += 1
        if count > 0:
            new_df.loc[(new_df['i'] == i) & (new_df['j'] == j), 'priceAvg'] = total / count

# Properly handle column operations
new_df = new_df.drop(columns=['price'])
new_df = new_df.rename(columns={'priceAvg': 'price'})

# Create validity and price matrices
a = []
b = []
for i in range(n_rows):
    a_row = []
    b_row = []
    for j in range(n_cols):
        valid = new_df[(new_df['i'] == i) & (new_df['j'] == j)]['isValid'].values[0]
        price = new_df[(new_df['i'] == i) & (new_df['j'] == j)]['price'].values[0]
        a_row.append(valid)
        b_row.append(price)
    a.append(a_row)
    b.append(b_row)

# Initialize GEKKO model
m = GEKKO(remote=False)
m.options.SOLVER = 1  # APOPT solver

# Create variables only for valid locations
valid_indices = [(i,j) for i in range(n_rows) for j in range(n_cols) if a[i][j] == 1]
l = m.Array(m.Var, len(valid_indices), lb=0, ub=1, integer=True)
s = m.Var(lb=50000, ub=82500, integer=True)



# Constraints
m.Equation(sum(l) == 1)  # Exactly one stadium


# Objective function with stadium capacity relationship
m.Minimize(
    sum(b[i][j] * l_var for (i,j), l_var in zip(valid_indices, l)) - 
    0.025 * (s**2 + 67500**2) + 0.0025 * s * b[n_rows//2][n_cols//2]
)
m.Minimize(b[i][j] * sum(l_var * ((i-n_rows/2)**2 + (j-n_cols/2)**2) for (i,j), l_var in zip(valid_indices, l)))

m.options.IMODE = 3

try:
    m.solve(disp=False)
except Exception as e:
    print(f"Solver failed: {e}")

# Print solution
print("\nOptimal solution:")
selected = np.argmax([x.value[0] for x in l])
i, j = valid_indices[selected]
print(f"Stadium location: ({i}, {j})")
print(f"Stadium capacity: {s.value[0]:.0f} seats")
