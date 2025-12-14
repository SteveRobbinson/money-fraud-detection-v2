import numpy as np
import pandas as pd

class Node:
    def __init__(self,
                 feature_index: int | None = None,
                 threshold: float | None = None,
                 left: 'Node' = None,
                 right: 'Node' = None,
                 value: int = None
                ):

        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        


def gini_impurity(y: list[int] | np.ndarray) -> float:
    
    y = np.array(y)
    _, counts = np.unique(y, return_counts = True)
    p = counts/np.sum(counts)
    gini = 1 - (np.sum(p**2))

    return gini



def buildtree(X: pd.DataFrame, 
              y: np.ndarray,
              depth: int | None, 
              max_depth: int | None,
              min_samples_split: int | None,
              min_samples_leaf: int | None
             ) -> Node:
    
    if max_depth is not None and depth >= max_depth:
        return Node(value = np.bincount(y).argmax())
    
    if len(X) <= min_samples_split:
        return Node(value = np.bincount(y).argmax())

    else:
        
        best_feature, best_threshold, left_idx, right_idx = best_split_RF(X, y, min_samples_split)
        node = Node(feature_index = best_feature, threshold = best_threshold)
        
        if best_feature is None:
            return Node(value = np.bincount(y).argmax())
        
        X_left, X_right = X[left_idx], X[right_idx]
        y_left, y_right = y[left_idx], y[right_idx]
                    
        node.left = buildtree(X_left, y_left, depth + 1, max_depth, min_samples_split, min_samples_leaf)
        node.right = buildtree(X_right, y_right, depth + 1, max_depth, min_samples_split, min_samples_leaf)

    
    return node
      


class DecisionTree:
    def __init__(self,
                 max_depth: int | None,
                 min_samples_split: int | None,
                 min_samples_leaf: int | None
                ):
        
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.root = None

    
    def fit(self, X: pd.DataFrame, y: np.ndarray):
        self.root = buildtree(X,
                              y,
                              depth = 0,
                              max_depth = self.max_depth,
                              min_samples_split = self.min_samples_split,
                              min_samples_leaf = self.min_samples_leaf
                             )

    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return np.array([predict_one(x, self.root) for x in X])




def best_split_RF(X: pd.DataFrame,
                  y: np.ndarray,
                  min_samples_split: int | None
                 ) -> Node | tuple[int, float, np.ndarray, np.ndarray]:

    if len(X) <= min_samples_split:
        return Node(value=np.bincount(y).argmax())

    else:
        G_parent = gini_impurity(y)
        best_gain = 0
        best_feature = None
        features = np.random.choice(X.shape[1], size = np.sqrt(X.shape[1]).astype(int), replace=False)
    
        #Iterujemy po wybranych cechach
        for f in features:
            potential_threshold = np.unique(X[:, f])
    
            for t in potential_threshold:
                mask_left = X[:, f] <= t
                mask_right = X[:, f] > t
                
                left_gini = gini_impurity(y[mask_left])
                right_gini = gini_impurity(y[mask_right])
                
                n_left = np.sum(mask_left)
                n_right = np.sum(mask_right)
                
                weighted_gini = n_left/len(y) * left_gini + n_right/len(y) * right_gini
                gain = G_parent - weighted_gini
        
                if gain > best_gain:
                    best_gain = gain
                    best_threshold = t
                    best_feature = f
                    left_idx = np.arange(len(y))[mask_left]
                    right_idx = np.arange(len(y))[mask_right]
    
            if best_feature is None:
                return None, None, None, None
            
    return best_feature, best_threshold, left_idx, right_idx
            
 

class RandomForest:
    def __init__(self,
                 n_estimators: int,
                 batch_size:int,
                 max_depth: int | None,
                 max_features: int | None,
                 min_samples_split: int | None,
                 min_samples_leaf: int | None
                ):
        
        self.n_estimators = n_estimators
        self.batch_size = batch_size
        self.max_depth = max_depth
        self.max_features = max_features
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.trees = []

    
    def random_samples(self,
                       X: pd.DataFrame,
                       y: np.ndarray
                      ) -> pd.DataFrame | np.ndarray:
        
        indices = np.random.choice(np.arange(len(X)), size = self.batch_size)
        X_set, y_set = X.iloc[indices], y[indices]

        return X_set, y_set
        

    def fit(self, X: pd.DataFrame, y: np.ndarray):
        for t in range(self.n_estimators):
            X_set, y_set = self.random_samples(X, y)
            tree = DecisionTree(self.max_depth, self.min_samples_split, self.min_samples_leaf)
            tree.fit(X_set, y_set)
            self.trees.append(tree)

    
    def one_tree_predict(self, x: pd.Series, tree: DecisionTree) -> int:
                    
        # Jeżeli węzeł jest liściem zwracamy value          
        if tree.value is not None:
            return tree.value
        
        if x[tree.feature_index] <= tree.threshold:
            return self.one_tree_predict(x, tree.left)
        
        else:
            return self.one_tree_predict(x, tree.right)

        
    def predict_one(self, x: pd.Series) -> int:
        lista_glosow = []
    
        for tree in self.trees:
            lista_glosow.append(self.one_tree_predict(x, tree.root))
    
        return np.bincount(lista_glosow).argmax()

    
    def predict(self, X: pd.DataFrame) -> list[int]:
        return [self.predict_one(x) for x in range(len(X))]
        
