import pickle
from app.models import Model
from app.crud import IncrementalDataCrud, PlayerDataCrud, ModelCrud



class IncrementalPredictionTrainer:
    def __init__(self, segment, game, playerdata=None):
        self.segment = segment
        self.game = game
        self.playerdata = playerdata
        self.current_data=None
        self.features=None
        self.new_data=None
        self.model=None
        self.IDC=IncrementalDataCrud(self.segment, self.game)
        self.PDC= PlayerDataCrud(self.segment, self.game)
            
    def update_player_data(self, player_doc):
        currentdata=player_doc['data']
        new_data={k: currentdata[k] + self.playerdata[k] for k in self.playerdata.keys()}
        self.PDC.update_data(new_data)
        
    # Fetch incremental data for segment/game
    def fetch_incremental_data(self):
        player_doc= self.PDC.read_data()
        
        if player_doc is None:
            # If no document exists, create one with current player data
            self.PDC.create_data(self.playerdata)
            
            return False
        
        else:
            self.update_player_data(player_doc)
            inc_doc = self.IDC.read_data()
            
            if inc_doc is None:
                # If no document exists, create one with current features
                self.IDC.create_data(self.features)
                
                return False
            
            else:
                self.update_player_data(player_doc)
                self.current_data=inc_doc['data']
                
                return True

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
            
            return False
            
        if len(self.new_data)<=99:
            return False
        else:
            return True
    
    # Update Incremental Data
    def update_incremental_data(self):
        self.IDC.update_data(self.new_data)
    
    # Decide whether to train the model or update the incremental collection
    def train_model(self):
            self.model = Model(self.segment, self.game, 'prediction', self.new_data)
            self.model.fetch_model()  # Fetch existing model
            self.model.predData()
            self.model.train_inc()
            
            # 5.4) Empty data list in incrementaldatasets for segment/game
            self.IDC.reset_data(
                self.segment, 
                self.game
                )
    
    # Save model back to collection
    def save_model(self):
        MC=ModelCrud(self.segment, self.game)
        model_bytes = pickle.dumps(self.model.mlmodel)
        MC.update_mlmodel(
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
    flag=trainer.fetch_incremental_data()  # 1) Fetch existing incremental data
    if flag:
        trainer.extract_features()  # 2) Extract features from new data
        flag=trainer.append_extracted_features()  # 3) Append extracted features to current data
        
        if flag:
            trainer.train_model() # 4) Train the model
            trainer.save_model()  # 5) Save the model if trained
        
        else:
            # Update the incremental collection with the new data
            trainer.update_incremental_data()
        