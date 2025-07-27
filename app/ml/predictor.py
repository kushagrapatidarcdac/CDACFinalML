import pickle
from app.crud import ModelCrud

class Predictor:
    def __init__(self, segment, game, features):
        self.segment = segment
        self.game = game
        self.features = features
        self.pipeline = None
        self.model_binary = None
        self.prediction = None
        
        # Make predictions while initialization
        self.predict_rating()
        
    def get_model(self):
        # Use Segment and Game and model_type = 'prediction' to fetch the model from the database
        # Set self.model_bytes to the fetched model
        MC=ModelCrud(self.segment, self.game)
        self.model_binary=MC.read_mlmodel(model_type="prediction")
        
    
    def load_model(self):
        self.get_model()
        self.pipeline = pickle.loads(self.model_binary)

    def make_predictions(self):
        self.load_model()
        self.prediction = {'rating': self.pipeline.predict([[self.features['total_rounds'], self.features['kd']]])}
        
    def predict_rating(self):
        self.load_model()
        self.make_predictions()
