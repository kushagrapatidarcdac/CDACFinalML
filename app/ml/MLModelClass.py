import pickle
import pandas as pd
from sklearn.pipeline import Pipeline

class Model:
                def __init__(self,new_data):
                    self.new_data = new_data
                    self.X=None
                    self.y=None
                    self.mlmodel=None
                    
            
                # Fetch model from mlmodels collection
                def fetch_model(self):
                    model_doc = self.mlmodels_collection.find_one({
                    "segment": self.segment,
                    "game": self.game,
                    "model_type": "prediction"
                    })
                    if not model_doc or "model" not in model_doc:
                        raise ValueError("Model not found in mlmodels collection for segment/game.")

                    model_binary = model_doc["model"]
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
