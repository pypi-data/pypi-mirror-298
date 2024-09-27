import pandas as pd


def split_data(df: pd.DataFrame) -> dict:
    splitted_data = {
        "to_fit": df.sample(frac=0.8, random_state=7),
        "to_test": df.drop(df.sample(frac=0.8, random_state=7).index),
    }

    return splitted_data
