from forest.dataset_split import create_sets
from forest.downsample_majority import downsample_majority
from forest import config
import pytest
from forest.data_preprocessing import preprocess, split_features_target

@pytest.fixture
def preprocessed_df():
    preprocessed_df = preprocess(
    config.test_path,
    config.get_features,
    config.dummies,
    config.drop_list
    )
    
    return preprocessed_df

@pytest.fixture
def downsampled_df(preprocessed_df):
    df_downsampled = downsample_majority(preprocessed_df, config.num_samples_test)

    return df_downsampled

@pytest.fixture
def X_y(downsampled_df):
    X, y = split_features_target(downsampled_df, 'is_fraud')

    return X, y

@pytest.fixture
def sets(X_y):
    X, y = X_y
    X_train, X_test, y_train, y_test = create_sets(X, y, 0.1)

    return X_train, X_test, y_train, y_test

