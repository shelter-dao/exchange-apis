import pandas as pd


df= pd.read_csv("./hist-data/100-hr.csv", index_col="datetime", parse_dates=['datetime'])

print(df[:10])
