import numpy as np
import pandas as pd

from forest import config
from forest.data_preprocessing import preprocess, split_features_target
from forest.downsample_majority import downsample_majority
from forest.dataset_split import create_sets
from forest.random_forest_numpy import RandomForest
from forest.load_save_model import save_model


def main():
    df = preprocess(
    config.raw_path,
    config.get_features,
    config.dummies,
    config.drop_list
    )

    df = downsample_majority(df)

    X, y = split_features_target(df, 'is_fraud')

    feature_names = list(X.columns)
    
    X_train, X_test, y_train, y_test = create_sets(X, y, 0.10)
    
    model = RandomForest(**config.parametry_rf)
    model.fit(X_train, y_train)

    save_model(
        model,
        config.parametry_rf,
        feature_names,
        config.model_path
    )

    if __name__ == '__main__':
        main()
