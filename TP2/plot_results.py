import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:.2f}'.format

df = (
    pd.read_csv("result.csv")
    .groupby(["algo", "size"])
    .mean(numeric_only=True)
    .reset_index()
)
res= df.pivot(index='size', columns='algo', values='time').reset_index()

res = res[['size', 'approx', 'glouton', 'progdyn']]

plot = sns.lineplot(x='size', y='time', hue='algo',
                    data=pd.melt(res, ['size'], value_name='time'))

plot.set(xscale='log')
plot.set(yscale='log')

plt.savefig("plots/test_puissance.png")