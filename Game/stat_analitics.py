#!/usr/bin/env python3

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

df = pd.read_csv('history.csv', index_col=0)

# keep only the 2 first columns
df = df.iloc[:, :2]

for column in df.columns:
    plt.plot(df.index, df[column], label=column)

plt.xlabel('Index de la partie')
plt.ylabel('Points')
plt.legend()
plt.show()

df_diff = df.diff()


print(df_diff.describe())

# for column in df_diff.columns:
#     print(column)
#     print(df_diff[column].describe())
#     print()

for column in df_diff.columns:
    plt.plot(df_diff.index, df_diff[column], label=column)

plt.xlabel('Index de la partie')
plt.ylabel('Différence de points')
plt.legend()
plt.show()

# count the number of times a player has the maximum score
print(df_diff.max())
print(df_diff[df_diff == df_diff.max()].count())