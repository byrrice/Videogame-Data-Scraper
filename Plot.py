import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plotit():

    # Manipulating the data to be suitable to plot
    df = pd.read_csv('gamesdata.csv')
    w = df.company.str.split('/', expand=True).unstack()
    w.index = w.index.droplevel(0)
    w = w.loc[~w.isnull()]
    df = df.drop('company', 1).join(pd.DataFrame(w), how='inner').reset_index(drop=True)
    df.columns = list(df.columns[:-1]) + ['company']
    # print(df)

    # Plotting the data
    plt.figure(2)
    ax = sns.countplot(x="company", data=df)
    plt.xticks(fontsize = 4, rotation=90)
    plt.title("Company's Number of Videogames")
    plt.savefig("company.png")

    # Plotting the data
    plt.figure(3)
    df2 = pd.DataFrame(df.groupby('company')['rating'].mean().sort_values().reset_index())
    ax = sns.barplot(x = "company", y = "rating", data=df2)
    plt.xticks(fontsize = 4, rotation=90)
    plt.yticks(np.arange(0, 100, 5.0))
    plt.title("Company's Average Rating")
    plt.savefig("rating.png")

    # Further plotting that plots specific companies' videogames and lets you see their individual ratings
    # # print(df.company.value_counts())
    # bw = df.loc[df.company == 'BioWare',:]
    # bw = bw.iloc[np.argsort(-bw.rating)].reset_index(drop=True)
    # plt.plot(np.arange(len(bw)), bw.rating)
    # # print(bw)
    # plt.xticks(np.arange(len(bw)), list(bw.name), rotation=90)
    # plt.tight_layout()

