import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data.csv")

# Tailles : 2^ : 4,5,6,7,8,9,10
# print(df.loc[df['Algorithm'] == "Classic"][['Matrix Size', 'Execution Time']])

def test_rapport(methode : str):
    x_input = 2**df.loc[df['Algorithm'] == methode]['Matrix Size']     # Mat size 2ˆn
    y_input = df.loc[df['Algorithm'] == methode]['Execution Time']*1000  # Exec time in ms
    z_input = y_input/(x_input**3) # Exec time / Complexity func (y/h(x) with h(x) = x^3)
    print(z_input)
    plt.scatter(x_input, z_input)
    plt.show()

test_rapport("Strassen")
