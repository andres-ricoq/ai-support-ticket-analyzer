import pandas as pd


def load_and_clean_data():

    df = pd.read_csv("dataset/tickets.csv")

    df = df.fillna("")

    df["Customer Email"] = (
        df["Customer Email"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df["Ticket Status"] = (
        df["Ticket Status"]
        .astype(str)
        .str.strip()
    )

    return df