import os
import joblib
import redis
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
CACHE_TTL_SECONDS = 300

app = FastAPI(title="Spam Detection API")
model = None
cache = None

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str

@app.on_event("startup")
def load_model():
    global model, cache
    model = joblib.load(MODEL_PATH)
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/healthz")
@app.get("/healthz")
def healthz():
    if model is None:
        return {"status": "not ready"}, 503
    return {"status": "ok", "version": "v2"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    cache_key = f"predict:{req.text}"

    cached = cache.get(cache_key)
    if cached is not None:
        return PredictResponse(label=cached)

    label = model.predict([req.text])[0]
    cache.setex(cache_key, CACHE_TTL_SECONDS, label)
    return PredictResponse(label=label)