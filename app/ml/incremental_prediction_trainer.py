import pickle
from MLModelClass import Model
from app.crud import update_mlmodel, read_incrementals, upsert_incremental, reset_incremental



class IncrementalPredictionTrainer:
    def __init__(self, segment, game, playerdata=None):
        self.segment = segment
        self.game = game
        self.playerdata = playerdata
        self.current_data=None
        self.features=None
        self.new_data=None
        self.model=None

    # Fetch incremental data for segment/game
    def fetch_incremental_data(self):
        inc_doc = read_incrementals(self.segment, self.game)
        
        if inc_doc is None:
            # If no document exists, create one with empty data list
            upsert_incremental({
                "segment": self.segment,
                "game": self.game,
                "data": self.current_data
            })
        else:
            self.current_data=inc_doc.get("data", [])

    # Extract required features from new data
    def extract_features(self):
        self.features={
                "total_rounds": self.playerdata["total_rounds"],
                "kd": self.playerdata["kd"],
                "rating": self.playerdata["rating"]
                }
    
    # Append new extracted features
    def append_extracted_features(self):
        if self.current_data is not None:
            self.new_data={k: self.current_data[k] + self.features[k] for k in self.features.keys()}
        else:
            self.new_data=self.extract_features()
  
        
    # Decide whether to train the model or update the incremental collection
    def train_or_update(self):
        # If less than 100 instances: just update incremental collection
        if len(self.new_data)< 99:
                upsert_incremental(
                    segment=self.segment,
                    game=self.game,
                    new_data=self.new_data
                    )
        else:
            
            self.model = Model(self.new_data)
            self.model.fetch_model()  # Fetch existing model
            self.model.predData()
            self.model.train_inc()
            
            # 5.4) Empty data list in incrementaldatasets for segment/game
            reset_incremental(
                self.segment, 
                self.game
                )
    
    # Save model back to collection
    def save_model(self):
        model_bytes = pickle.dumps(self.model.mlmodel)
        update_mlmodel(
            segment=self.segment,
            game=self.game,
            model_type="prediction",
            model_bytes=model_bytes
        )

      
        
def process_new_data(segment, game, newdata):
    """
    newdata: dict to lists , dict.keys() contains
        player_name, country, team, total_rounds, kd, rating
    """
    trainer = IncrementalPredictionTrainer(segment, game, playerdata=newdata)
    trainer.fetch_incremental_data()  # 1) Fetch existing incremental data
    trainer.extract_features()  # 2) Extract features from new data
    trainer.append_extracted_features()  # 3) Append extracted features to current data
    trainer.train_or_update()  # 4) Train or update incremental collection
    trainer.save_model()  # 5) Save the model if trained