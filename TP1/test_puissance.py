import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv("data.csv").groupby(['Algorithm', 'Matrix Size']).mean(numeric_only=True).reset_index()
df['Actual Size'] = df['Matrix Size'].apply(lambda val: 2 ** val)

classic = df.loc[df['Algorithm'] == 'Classic']

graph = sns.FacetGrid(classic, height=4, aspect=1)
graph = graph.map(plt.plot, 'Actual Size', 'Execution Time')
graph.set(xscale='log')
graph.set(yscale='log')
graph.add_legend()
plt.savefig('plots/puissance_classic.png')

plt.close()

strassen = df.loc[df['Algorithm'] == 'Strassen']

graph = sns.FacetGrid(strassen, height=4, aspect=1)
graph = graph.map(plt.plot, 'Actual Size', 'Execution Time')
graph.set(xscale='log')
graph.set(yscale='log')
graph.add_legend()
plt.savefig('plots/puissance_strassen.png')

plt.close()

strassen_leaf = df.loc[df['Algorithm'] == 'Strassen with Leaf']

graph = sns.FacetGrid(strassen_leaf, height=4, aspect=1)
graph = graph.map(plt.plot, 'Actual Size', 'Execution Time')
graph.set(xscale='log')
graph.set(yscale='log')
graph.add_legend()
plt.savefig('plots/puissance_strassen_leaf.png')

plt.close()
