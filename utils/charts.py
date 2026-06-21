import pandas as pd
import matplotlib.pyplot as plt

def create_chart():

    data = {
        "Test": ["Hemoglobin", "Glucose", "Vitamin D"],
        "Value": [10.5, 145, 18]
    }

    df = pd.DataFrame(data)

    fig, ax = plt.subplots()

    ax.bar(df["Test"], df["Value"])

    return fig