import pandas as pd

def load_medical_dataset():

    df = pd.read_csv("data/disease.csv")

    docs = []

    for _, row in df.iterrows():

        docs.append(str(row))

    return docs