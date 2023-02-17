import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("data.csv").groupby(['Algorithm', 'Matrix Size']).mean(numeric_only=True).reset_index()

res = df.pivot(index='Matrix Size', columns='Algorithm', values='Execution Time').reset_index()
res['Taille'] = res['Matrix Size'].apply(lambda x: 2 ** x)

res = pd.melt(res[['Taille', 'Classic', 'Strassen', 'Strassen avec Seuil']], 'Taille', value_name='Temps')

for algo in ['Classic', 'Strassen', 'Strassen avec Seuil']:
    df2 = res[res['Algorithm'] == algo]

    # On applique f(x) à la taille en fonction de s'il s'agit de Strassen ou Classic
    # Estimation Classic: O(n^3) et Estimation Strassen: O(n^log(7))
    df2['Taille'] = df2['Taille'].apply(lambda x: x ** 3 if algo == 'Classic' else x ** 2.8074)

    plot = sns.lineplot(x='Taille', y='Temps', hue='Algorithm',
             data=df2)

    plt.savefig(f"plots/constante_{'_'.join(algo.lower().split(' '))}.png")
    plt.close()
