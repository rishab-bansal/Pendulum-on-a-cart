import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
print(df.columns)
print(df.shape)
print(df.at[df.shape[0] - 1, "xp"])
plt.plot(df.loc[:, "xp"])
plt.show()