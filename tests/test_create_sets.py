from forest.dataset_split import create_sets

def test_create_sets(X_y):
    X, y = X_y
    X_train, X_test, y_train, y_test = create_sets(X, y, 0.1)

    assert len(X_train) + len(X_test) == len(X)
    assert len(y_train) + len(y_test) == len(y)

    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)

