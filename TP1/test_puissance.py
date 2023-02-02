import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data.csv")

print(df)

data = [
    ["Strassen", "8x8", 64, 0.00441924123, "n^3"], 
    ["Strassen", "8x8", 64, 0.00441924123, "n^3"], 
    ["Strassen", "8x8", 64, 0.00441924123, "n^3"], 
    ["Conventional", "4x4", 24, 0.00441924123, "n^3"], 
    ["Conventional", "4x4", 32, 0.543254325, "1"], 
    ["Conventional", "4x4", 32, 0.4231432155, "1"], 
    ["Conventional", "4x4", 32, 0.1432213231, "1"]
]

x_input = np.linspace(0, 10, 1000) # Execution Time
y_input = x_input**3

plt.loglog(x_input, y_input)

# plt.show()