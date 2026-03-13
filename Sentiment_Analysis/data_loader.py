import pandas as pd

def load_dataset(path):
    df = pd.read_csv("IMDB Dataset.csv")

    df = df[['review', 'sentiment']]
    df.dropna(inplace=True)

    return df