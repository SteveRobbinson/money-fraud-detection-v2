from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import numpy as np

def create_sets(X: pd.DataFrame,
                y: pd.Series,
                test_size: float
                ) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:

    indices = StratifiedShuffleSplit(n_splits = 1, test_size=test_size)
    train_indices, test_indices = next(indices.split(X, y))

    X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
    y_train, y_test = y.iloc[train_indices], y.iloc[test_indices]

    return X_train.to_numpy(), X_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy()


