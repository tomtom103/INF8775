import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv("data.csv").groupby(['Algorithm', 'Matrix Size']).mean(numeric_only=True).reset_index()

res = df.pivot(index='Matrix Size', columns='Algorithm', values='Execution Time').reset_index()
res['Actual Size'] = res['Matrix Size'].apply(lambda x: 2 ** x)


res = res[['Actual Size', 'Classic', 'Strassen', 'Strassen with Leaf']]

# plot = sns.lineplot(x='Actual Size', )
# plot.set(xscale='log')
# plot.set(yscale='log')
# plot.add_legend()
# plt.show()

# print(df)
print(pd.melt(res, ['Actual Size']))

plot = sns.lineplot(x='Actual Size', y='value', hue='Algorithm',
             data=pd.melt(res, ['Actual Size']))

plot.set(xscale='log')
plot.set(yscale='log')

plt.savefig("plots/puissance_combined.png")

exit()
# df = pd.read_csv("leaf_data.csv").groupby(['Leaf Size', 'Matrix Size']).mean(numeric_only=True).reset_index()
# df['Actual Size'] = df['Matrix Size'].apply(lambda val: 2 ** val)

# leaf_sizes = [2 ** i for i in range(4, 11)]

# for size in leaf_sizes:
#     df2 = df.loc[df['Leaf Size'] == size]

#     graph = sns.FacetGrid(df2, height=4, aspect=1)
#     graph = graph.map(plt.plot, 'Actual Size', 'Execution Time')
#     graph.set(xscale='log')
#     graph.set(yscale='log')
#     graph.add_legend()
#     plt.savefig(f'plots/puissance_strassen_leaf_size_{size}.png')

#     plt.close()

# classic = df.loc[df['Algorithm'] == 'Classic']

# graph = sns.FacetGrid(classic, height=4, aspect=1)
# graph = graph.map(plt.plot, 'Actual Size', 'Execution Time')
# graph.set(xscale='log')
# graph.set(yscale='log')
# graph.add_legend()
# plt.savefig('plots/puissance_classic.png')

# plt.close()

# strassen = df.loc[df['Algorithm'] == 'Strassen']

# graph = sns.FacetGrid(strassen, height=4, aspect=1)
# graph = graph.map(plt.plot, 'Actual Size', 'Execution Time')
# graph.set(xscale='log')
# graph.set(yscale='log')
# graph.add_legend()
# plt.savefig('plots/puissance_strassen.png')

# plt.close()

# strassen_leaf = df.loc[df['Algorithm'] == 'Strassen with Leaf']

# graph = sns.FacetGrid(strassen_leaf, height=4, aspect=1)
# graph = graph.map(plt.plot, 'Actual Size', 'Execution Time')
# graph.set(xscale='log')
# graph.set(yscale='log')
# graph.add_legend()
# plt.savefig('plots/puissance_strassen_leaf.png')

# plt.close()
