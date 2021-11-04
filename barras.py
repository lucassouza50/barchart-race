import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker


Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, bitrate=-1)

df = pd.read_csv('final.csv')
df = df.sort_values(by='win')

datas = np.unique(df['date'].sort_values())
coris = ['#68edc4', '#dbdcf3', '#beaf5b', '#157151', '#8af936', '#d07cd5',
         '#aad13c', '#b6b8ac', '#63e535', '#74948f', '#0a528e', '#6ccfeb',
         '#d04204', '#a73e20', '#98b0b9', '#6c8538', '#4e60b4', '#8cb296',
         '#c1c106', '#2e9503', '#c0fc65', '#9ae0d2']
cores = ['#845ec2', '#d65db1', '#ff6f91', '#ff9671', '#ffc75f', '#f9f871']

paises = np.unique(df['win'])
cores = np.random.choice(coris, size=len(paises))
dic = dict(zip(paises, cores))

fig = plt.figure(figsize=(15, 8))
ax = plt.subplot()


def data_to_string(data):
    nova_data = data.split('-')
    meses = ['JAN', 'FEV', 'MAR', 'ABR', 'MAIO', 'JUN',
             'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
    numeros = ['01', '02', '03', '04', '05', '06',
               '07', '08', '09', '10', '11', '12']
    dic = dict(zip(numeros, meses))
    return dic[nova_data[1]] + '-' + nova_data[0]


def barra(data):
    df2 = df[df['date'].eq(data)].sort_values(by='cumsum',
                                              ascending=True).tail(10)
    ax.clear()
    ax.barh(df2['win'], df2['cumsum'], color=[dic[x] for x in df2['win']])
    dx = df2['cumsum'].max() / 200
    for i, (value, name) in enumerate(zip(df2['cumsum'], df2['win'])):
        if value == 0:
            name = ''
        ax.text(value-dx, i, name, size=14, ha='right', va='center')
        ax.text(value+dx, i, value, size=14, ha='left',  va='center')
    ax.text(1, 0.4, data_to_string(data), transform=ax.transAxes,
            size=20, ha='right', weight=800)
    ax.text(0, 1.12, 'Número de vitórias de seleções de 1872 a 2019',
            transform=ax.transAxes, size=20, ha='left', va='top')
    ax.set_yticks([])
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', labelsize=12)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    plt.box(False)


animator = animation.FuncAnimation(fig, barra,
                                   frames=datas,
                                   interval=1000)
animator.save('graficos.mp4', writer=writer)
