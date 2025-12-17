from forest.data_preprocessing import split_features_target
import numpy as np

def test_splitting(preprocessed_df):
    X, y = split_features_target(preprocessed_df, 'is_fraud')

    assert 'is_fraud' not in X.columns

    unique_vals = np.unique(y)
    assert np.isin(unique_vals, [0, 1, True, False]).all()

    assert len(preprocessed_df.drop('is_fraud').columns) == len(X.columns)

    assert y.reset_index(drop=True).equals(preprocessed_df["is_fraud"].reset_index(drop=True))
        
