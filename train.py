from functools import partial, update_wrapper
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tpot import TPOTRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_california_housing


def main():
    # split into train and test
    dataset = fetch_california_housing(as_frame=True)
    dataset.target = dataset.target * 100000
    X_train, X_test, y_train, y_test = train_test_split(
        dataset.data.astype(float),
        dataset.target,
        train_size=0.7,
        test_size=0.3,
    )

    for ds, name in zip(
        (X_train, X_test, y_train, y_test), ("X_train", "X_test", "y_train", "y_test")
    ):
        ds.to_csv(f"{name}.csv", index=False)

    # create and fit TPOT
    tpot = TPOTRegressor(
        generations=10,
        population_size=50,
        verbosity=2,
        random_state=666,
        n_jobs=-1,
        scoring="neg_mean_absolute_error",
        config_dict="TPOT light",
    )
    tpot.fit(X_train, y_train)
    # calculate mean_absolute_error, means_squared_error, r2_score in a loop
    predictions = tpot.predict(X_test)
    for metric in [
        mean_absolute_error,
        update_wrapper(partial(mean_squared_error, squared=False), mean_squared_error),
        r2_score,
    ]:
        print(f"{metric.__name__}: {metric(y_test, predictions)}")
    tpot.export("tpot_pipeline_TO_EDIT.py")


if __name__ == "__main__":
    main()
