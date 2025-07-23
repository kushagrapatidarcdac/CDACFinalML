import pickle
from app.crud import read_mlmodel

class Predictor:
    def __init__(self, segment, game, features):
        self.segment = segment
        self.game = game
        self.features = features
        self.pipeline = None
        self.model_bytes = None
        self.prediction = None
    
    def get_model(self):
        # Use Segment and Game and model_type = 'prediction' to fetch the model from the database
        # Set self.model_bytes to the fetched model
        self.model_bytes=read_mlmodel(segment=self.segment, game=self.game, model_type="prediction")
        
    
    def load_model(self):
        self.get_model()
        self.pipeline = pickle.loads(self.model_bytes)

    def make_predictions(self):
        self.load_model()
        self.prediction = self.pipeline.predict([[self.features['total_rounds'], self.features['kd']]])
    
def predict_rating(segment, game, features):
    predict = Predictor(segment=segment, game=game, features=features)
    predict.load_model()
    predict.make_predictions()
    
    return predict.prediction[0]
