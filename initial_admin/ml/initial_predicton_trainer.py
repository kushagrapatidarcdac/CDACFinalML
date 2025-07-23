import pickle
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from app.crud import create_mlmodel, create_dataset


class InitialPredictionTrainer:
    
    
    def __init__(self, segment, game):
        self.segment = segment
        self.game = game
        self.features=None
        self.target=None
        self.pipeline=None
        self.model_type="prediction" 
        self.model_bytes=None
    
    def extract_features(self, clean_data):
        self.features = clean_data[['total_rounds', 'kd']]
        self.target = clean_data['rating']

    def initpipeline(self):
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', SGDRegressor(max_iter=1000, tol=1e-3, random_state=42))
        ])
        
    def train_model(self):
        self.pipeline.fit(self.features, self.target)
    
    def byte_model(self):
        self.model_bytes = pickle.dumps(self.pipeline)
    
    def save_data(self, clean_data):
        # This method is used to save the initial data to the database
        player_name=clean_data['player_name'].tolist()
        country=clean_data['country'].tolist()
        team=clean_data['team'].tolist()
        total_rounds=clean_data['total_rounds'].tolist(),
        kd=clean_data['kd'].tolist(),
        rating=clean_data['rating'].tolist()
        data = {
            "player_name": player_name,
            "country": country,
            "team": team,
            "total_rounds": total_rounds,
            "kd": kd,
            "rating": rating
        }
        
        create_dataset(
            segment=self.segment,
            game=self.game,
            data=data

        )

    
    def save_model(self):
        create_mlmodel(
            segment=self.segment,
            game=self.game,
            model_type=self.model_type,
            model_bytes=self.model_bytes
        )
    
def initial_trainer(segment, game, clean_data):
    initialtrainer = InitialPredictionTrainer(segment=segment, game=game)
    initialtrainer.extract_features(clean_data)
    initialtrainer.initpipeline()
    initialtrainer.train_model()
    initialtrainer.byte_model()
    initialtrainer.save_data(clean_data)
    initialtrainer.save_model()

