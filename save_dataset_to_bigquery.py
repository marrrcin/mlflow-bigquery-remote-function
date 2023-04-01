import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("X_test.csv")
    df.to_gbq(
        "mlflow_model_demo.california_housing_test",
        project_id="zablonet-gce",
        if_exists="replace",
    )
