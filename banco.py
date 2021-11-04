import pandas as pd
import numpy as np
import os


def win(n):
    if n[3] > n[4]:
        return n[1]
    elif n[4] > n[3]:
        return n[2]
    else:
        return np.nan


df = pd.read_csv('results.csv')
wins = []
for x in df.values:
    wins.append(win(x))

df['win'] = wins

df['date'] = pd.to_datetime(df['date'])
df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
df2 = df.groupby(['win', 'date']).size().reset_index(name='size')
df2.to_csv('results_novo.csv', index=False)

# aqui

datas = pd.date_range('1872-10-30', '2019-09-30', freq='MS')
df1 = pd.DataFrame(datas, columns=['date'])
df2 = pd.read_csv('results_novo.csv')

a = df1['date'].values
b = np.unique(df2['win'].values)

index = pd.MultiIndex.from_product([a, b], names=['date', 'win'])
df3 = pd.DataFrame(index=index).reset_index()
df3.to_csv('produto.csv', index=False)

df = pd.read_csv('results_novo.csv')
df['date'] = pd.to_datetime(df['date'])
df.to_csv('results_novo.csv', index=False)

df1 = pd.read_csv('results_novo.csv')
df2 = pd.read_csv('produto.csv')
merged = pd.merge(df1, df2, on=['date', 'win'], how='outer')
merged = merged.fillna(0)
merged['size'] = merged['size'].astype('int32')
merged = merged.sort_values('date')
merged.to_csv('semifinal.csv', index=False)

df = pd.read_csv('semifinal.csv')
df['cumsum'] = df.groupby(['win'])['size'].cumsum()
df.to_csv('final.csv', index=False)

os.remove('semifinal.csv')
os.remove('produto.csv')
os.remove('results_novo.csv')
