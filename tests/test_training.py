from forest.random_forest_numpy import RandomForest
from forest import config


def test_train(sets):
    X_train, _, y_train, _, = sets

    model = RandomForest(**config.parametry_rf_test)
    model.fit(X_train, y_train)

    
