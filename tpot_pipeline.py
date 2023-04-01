import shutil

import mlflow
import pandas as pd
from mlflow.models import infer_signature
from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.svm import LinearSVR
from sklearn.tree import DecisionTreeRegressor
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive

X_train = pd.read_csv("X_train.csv")
y_train = pd.read_csv("y_train.csv")


with mlflow.start_run() as run:
    # Average CV score on the training set was: -39252.13134203072
    exported_pipeline = make_pipeline(
        RobustScaler(),
        VarianceThreshold(threshold=0.0001),
        StackingEstimator(
            estimator=LinearSVR(
                C=10.0,
                dual=True,
                epsilon=0.1,
                loss="squared_epsilon_insensitive",
                tol=0.001,
            )
        ),
        DecisionTreeRegressor(max_depth=10, min_samples_leaf=14, min_samples_split=4),
    )
    # Fix random state for all the steps in exported pipeline
    set_param_recursive(exported_pipeline.steps, "random_state", 666)

    exported_pipeline.fit(X_train, y_train)

    test_df = pd.read_csv("X_test.csv")
    shutil.rmtree("model", ignore_errors=True)
    mlflow.sklearn.save_model(
        exported_pipeline,
        "model",
        signature=infer_signature(X_train),
        input_example=test_df.sample(n=7, random_state=666),
    )
    print("Done :)")
