import numpy as np
import pandas as pd
from gekko import GEKKO

data = pd.read_csv("ijmatrix.csv")

iMax = max(data["i"])
jMax = max(data["j"])

a = []
for i in range(iMax):
    a.append([])
    for j in range(jMax):
        a[i][j] = data.iloc((i * jMax) + j)["isValid"]

#dimensions of stadium locations array
#SAMPLE -- this should be 2* the #of rows in the image array and 2* the #of cols in the image array
#read these values in, store here
n_rows = max(data["i"]) * 2
n_cols = max(data["j"]) * 2

#penalizes expensive land
#SAMPLE -- adjust functions as you like
#A matrix is land/property value (total) in an area
def land_value(A, X, _):
    return sum(A[i][j] * X[i][j] for i in range(n_rows) for j in range(n_cols))

#penalizes drastic height changes
#SAMPLE - adjust functions as you like
#A matrix is "steepness" metric of area
def topography(A, X, _):
    return sum(A[i][j] * X[i][j] for i in range(n_rows) for j in range(n_cols))

#requires singular stadium
def CONST_one_stadium(_, X, __):
    return (-1 + sum(X[i][j] for i in range(n_rows) for j in range(n_cols)))**2

#requires no water
#A matrix should be 1 for invalid areas, 0 for valid areas
def CONST_no_water(A, X, _):
    return sum(A[i][j] * X[i][j] for i in range(n_rows) for j in range(n_cols))

#requires stadium to be in radius of the city
#SAMPLE - adjust functions as you like
#A matrix should be 1 for invalid areas, 0 for valid areas
def CONST_in_radius(A, X, _):
    return sum(A[i][j] * X[i][j] for i in range(n_rows) for j in range(n_cols))

#rewards larger stadiums, within range
#SAMPLE - adjust functions as you like
#y variable is stadium capacity ()
def stadium_size(A, X, y):
    return 0.0095009*y - sum(A[i][j] * X[i][j] * (0.75 + 0.0005 * y) for i in range(n_rows) for j in range(n_cols))

#initialize GEKKO model (solve locally) and set the MINLP solver (APOPT) for binary vars
m = GEKKO(remote=False)
m.options.SOLVER = 1 

#is stadium at i,j & # seats (thousands)
l = m.Array(m.Var, (n_rows, n_cols), lb=0, ub=1, integer=True)
s = m.Var(lb=50000, ub=82500, integer=True)

#function weights
M = 50000000
num_terms = 5
weights = [1,M,M,M, -0.005]

#functions
funcs = [land_value, CONST_one_stadium, CONST_no_water, CONST_in_radius, stadium_size]

#coefficient matrices for functions
#make sure coeffs[-1] == coeffs[0]
#SAMPLE -- these are read in from gis data
coeffs = [[[20,30,10,15],
           [15,16,19,5],
           [12,21,23,21]],
          [[5,6,7,8],
           [7,1,2,3],
           [9,7,5,4]],
          [[20,30,10,15],
           [15,16,19,5],
           [12,21,23,21]],
          [[1,1,1,1],
           [0,1,0,0],
           [1,1,0,0]],
          [[1,1,0,1],
           [1,0,0,1],
           [1,1,0,1]],
          [[20,30,10,15],
           [15,16,19,5],
           [12,21,23,21]]]
counter = 1  # start counter at 1


#objective
def obj_term(f, A, X, y):
    return f(A,X,y)

#min weighted terms
m.Minimize(sum(weights[i]*obj_term(funcs[i],coeffs[i],l,s) for i in range(num_terms)))

#steady-state optimization mode (IMODE=3)
m.options.IMODE = 3

#solve (display intermediate steps)
m.solve(disp=True)

# Print the resulting binary 2D array and the objective value
print("Solution for the binary 2D array:")
for i in range(n_rows):
    row = [int(round(l[i][j].value[0])) for j in range(n_cols)]
    print(f"Row {i}: {row}")
print(f"Solution for stadium seat number: {s.value[0]}")
print("Objective value:", m.options.objfcnval)
