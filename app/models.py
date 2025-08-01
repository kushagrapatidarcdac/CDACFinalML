import pickle
import pandas as pd
from app.crud import ModelCrud
from pydantic import BaseModel
from sklearn.pipeline import Pipeline


# PredictMLInput is used for prediction
class PredictMLInput(BaseModel):
    segment: str
    game: str
    total_rounds: int
    kd: float

# RecommendMLInput is used for recommendation
class RecommendMLInput(BaseModel):
    segment: str
    game: str
    player_name: str
    k: int

# IncrementalMLInput is used for incremental learning
class IncrementalMLInput(BaseModel):
    segment: str
    game: str
    player_name: str
    country: str
    team: str
    total_rounds: int
    kd: float
    rating: float

# ML Model
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
        MC=ModelCrud(self.segment, self.game)
        model_binary = MC.read_mlmodel(model_type=self.model_type)
        self.mlmodel = pickle.loads(model_binary)

    # Prepare data for partial_fit
    def predData(self):
        df = pd.DataFrame.from_dict(self.new_data, orient='columns')
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
            X_scaled = scaler.transform(self.X)
            # partial_fit with unscaled is normally required, so we will call partial_fit on regressor with scaled X
            # SGDRegressor supports partial_fit for regression natively.
            regressor.partial_fit(X_scaled, self.y)
