import pickle
import pandas as pd
from crud import read_mlmodel
from pydantic import BaseModel
from typing import Dict, List
from sklearn.pipeline import Pipeline


# TrainMLInput is used for training requests
class TrainMLInput(BaseModel):
    segemnt: str
    game: str
    data: Dict[str,]

# PredictMLInput and PredictMLOutput are used for prediction requests
class PredictMLInput(BaseModel):
    segment: str
    game: str
    features: Dict[str, float]

class PredictMLOutput(BaseModel):
    prediction: float

class RecommendRequest(BaseModel):
    pass

class RecommendResponse(BaseModel):
    pass

class Model:
    def __init__(self,segment, game, model_type,new_data):
        self.segment = segment
        self.game = game
        self.model_type = model_type
        self.new_data = new_data
        self.X=None
        self.y=None
        self.mlmodel=None
        

    # Fetch model from mlmodels collection
    def fetch_model(self):
        model_binary = read_mlmodel(segment=self.segment, game=self.game, model_type=self.model_type)
        self.mlmodel = pickle.loads(model_binary)

    # Prepare data for partial_fit
    def predData(self):
        df = pd.DataFrame(self.new_data)
        self.X = df[["total_rounds", "kd"]].values
        self.y = df["rating"].values

    # Partial fit the model
    def train_inc(self):
        # Model is a pipeline with StandardScaler + SGDRegressor:
        # Partial fit requires calling on the regressor inside pipeline.

        # Extract scaler and regressor from the pipeline
        if isinstance(self.mlmodel, Pipeline):
            scaler = self.mlmodel.named_steps['scaler']
            regressor = self.mlmodel.named_steps['regressor']

            # Scale features
            X_scaled = scaler.transform(self.X) if hasattr(scaler, "transform") else self.X
            # partial_fit with unscaled is normally required, so we will call partial_fit on regressor with scaled X
            # SGDRegressor supports partial_fit for regression natively.
            regressor.partial_fit(X_scaled, self.y)
        else:
            # If model isn't a pipeline, fallback to just partial_fit on model
            self.mlmodel.partial_fit(self.X, self.y)
