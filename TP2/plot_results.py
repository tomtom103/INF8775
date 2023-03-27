import math
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

pd.options.display.float_format = '{:.2f}'.format

def test_puissance(df: pd.DataFrame) -> None:
    pivoted = df.pivot(index='size', columns='algo', values='time').reset_index()

    res = pivoted[['size', 'approx', 'glouton']]

    res['O(n^2)'] = res['size'].apply(lambda x: x ** 2)
    res['O(n^3)'] = res['size'].apply(lambda x: x ** 3)
    res['O(n^2*log(n))'] = res['size'].apply(lambda x: x ** 2 * np.log(x))

    fig, ax = plt.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')

    real_data = res[['size', 'glouton', 'approx']]
    theory_data = res[['size', 'O(n^2)', 'O(n^3)', 'O(n^2*log(n))']]

    sns.scatterplot(x='size', y='time', hue='algo',
                        data=pd.melt(real_data, ['size'], value_name='time'), ax=ax)
    
    sns.lineplot(x='size', y='time', hue='algo',
                        data=pd.melt(theory_data, ['size'], value_name='time'), ax=ax)

    plt.savefig("plots/test_puissance.png")

    for algo in ['approx', 'glouton']:
        log_taille = list(map(lambda v: math.log(v, 10), pivoted['size'].to_list()))
        log_temps = list(map(lambda v: math.log(v, 10), pivoted[algo].to_list()))

        X = np.array([np.array([e]) for e in log_taille])
        y = np.array(log_temps)
        
        reg = LinearRegression().fit(X, y)
        m = reg.coef_[0]
        b = reg.intercept_
        print(f"algo: {algo}")
        print(f'score: {reg.score(X, y)}')
        print(f'm: {m}')
        print(f'b: {b}')
        print(f'a: {10}')
        print(f'y = {pow(10, b)} * x^{m}')


def test_constantes(df: pd.DataFrame) -> None:
    res= df.pivot(index='size', columns='algo', values='time').reset_index()

    res = res[['size', 'progdyn']]

    res['size'] = res['size'].apply(lambda x: x ** 2 * 2 ** x)

    data = pd.melt(res, ['size'], value_name='time')
    data = data.dropna(axis=0, how='any')

    sns.lineplot(x='size', y='time', hue='algo',
                        data=data)
    
    plt.xlabel('x')
    plt.ylabel('y')

    plt.savefig("plots/test_constantes.png")

if __name__ == "__main__":
    df = (
        pd.read_csv("result.csv")
        .groupby(["algo", "size"])
        .mean(numeric_only=True)
        .reset_index()
    )
    test_puissance(df)
    plt.clf()
    test_constantes(df)
