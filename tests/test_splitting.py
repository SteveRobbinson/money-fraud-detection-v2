from forest.data_preprocessing import split_features_target
import numpy as np

def test_splitting(df_preprocessed):
    X, y = split_features_target(df_preprocessed, 'is_fraud')

    assert 'is_fraud' not in X.columns

    unique_vals = np.unique(y)
    assert np.isin(unique_vals, [0, 1, True, False]).all()

    assert len(df_preprocessed.drop('is_fraud').columns) == len(X.columns)

    assert y.reset_index(drop=True).equals(df_preprocessed["is_fraud"].reset_index(drop=True))
        
