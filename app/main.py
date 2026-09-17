import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")

app = FastAPI(title="Spam Detection API")
model = None

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str

@app.on_event("startup")
def load_model():
    global model
    model = joblib.load(MODEL_PATH)

@app.get("/healthz")
def healthz():
    if model is None:
        return {"status": "not ready"}, 503
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    label = model.predict([req.text])[0]
    return PredictResponse(label=label)