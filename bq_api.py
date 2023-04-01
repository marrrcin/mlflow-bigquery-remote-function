import mlflow.sklearn
import pandas as pd
from fastapi import FastAPI

from api.models import BigQueryUDFRequest, BigQueryUDFResponse, AppContext

app = FastAPI()
ctx = AppContext()


@app.on_event("startup")
def load_model():
    # Load your MLflow model here
    ctx.model = mlflow.sklearn.load_model("model")


@app.post("/", response_model=BigQueryUDFResponse)
def udf(request: BigQueryUDFRequest):
    df = pd.DataFrame(request.calls)
    # Optionally - parse the request
    predictions = ctx.model.predict(df)
    return BigQueryUDFResponse(replies=predictions.tolist())
