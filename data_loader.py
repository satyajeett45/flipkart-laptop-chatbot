import pandas as pd

def load_laptop_data(path="data/laptops_with_description.csv"):
    df = pd.read_csv(path)
    df.dropna(subset=["Description"], inplace=True)
    return df