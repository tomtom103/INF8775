import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("data.csv").groupby(['Algorithm', 'Matrix Size']).mean(numeric_only=True).reset_index()

res = df.pivot(index='Matrix Size', columns='Algorithm', values='Execution Time').reset_index()
res['Taille'] = res['Matrix Size'].apply(lambda x: 2 ** x)


res = res[['Taille', 'Classic', 'Strassen', 'Strassen avec Seuil']]

plot = sns.lineplot(x='Taille', y='Temps', hue='Algorithm',
             data=pd.melt(res, ['Taille'], value_name='Temps'))

plot.set(xscale='log')
plot.set(yscale='log')

plt.savefig("plots/puissance_combined.png")
