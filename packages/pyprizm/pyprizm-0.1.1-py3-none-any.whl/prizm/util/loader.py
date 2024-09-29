import pandas as pd


class Loader:

    @staticmethod
    def csv(path: str) -> pd.DataFrame:
        return pd.read_csv(path)
