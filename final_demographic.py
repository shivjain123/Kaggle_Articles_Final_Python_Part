import pandas as pd

df = pd.read_csv('shared_articles_proccessed.csv')

df = df.sort_values(['Total Events'], ascending=[False])

output = df[["url", "title", "text", "lang", "Total Events"]].head(20).values.tolist()
