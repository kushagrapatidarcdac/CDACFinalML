from .database import db
# ==== Database Collections ====
playerdatasets_collection = db['playerdatasets']
incremental_collection = db['incrementaldatasets']
mlmodels_collection = db['mlmodels']


'''
playerdatasets collection document structure:
{   
    "segment": "",
    "game": "",
    "data": {
        "player_name": player_name, # String
        "country": country, # String
        "team": team, # String
        "total_rounds": total_rounds, # List of integers
        "kd": kd, # List of floats
        "rating": rating # List of floats
    }
'''

class PlayerDataCrud:
    def __init__(self, segment, game):
        self.segment = segment
        self.game = game
    
    # 1. Create (Insert) a document
    def create_data(self, player_data):
        doc = {
            "segment": self.segment,
            "game": self.game,
            "data": {
                "player_name": player_data['player_name'],
                "country": player_data["country"],
                "team": player_data["team"],
                "total_rounds": player_data["total_rounds"],
                "kd": player_data["kd"],
                "rating": player_data["rating"]
            }
        }
        playerdatasets_collection.insert_one(doc)

    # 2. Read (Find) documents by segment and game
    def read_data(self):
        query = {"segment": self.segment, "game": self.game}
        doc = playerdatasets_collection.find_one(query)
        return doc

    # 3. Update - Add a new player in the data fields for a given segment and game
    def update_data(self, new_data):
        query = {"segment": self.segment, "game": self.game}
        newvalues = {"$set": {
            "data": {
                "player_name": new_data["player_name"],
                "country": new_data["country"],
                "team": new_data["team"],
                "total_rounds": new_data["total_rounds"],
                "kd": new_data["kd"],
                "rating": new_data["rating"]
            }
        }}
        
        playerdatasets_collection.update_one(query, newvalues)

    # 4. Delete - Remove a document by segment and game
    def delete_data(self):
        delete_query = {"segment": self.segment, "game": self.game}
        playerdatasets_collection.delete_one(delete_query)



# ==== INCREMENTAL DATASETS CRUD ==== Under Development

'''
incrementaldatasets collection document structure:
{   
    "segment": "",
    "game": "",
    "data": {
        "total_rounds": total_rounds, # List of integers
        "kd": kd, # List of floats
        "rating": rating # List of floats
    }
'''
class IncrementalDataCrud:
    def __init__(self, segment, game):
        self.segment = segment
        self.game = game
    
    # 1. Create (Insert) a document
    def create_data(self, player_data):
        doc = {
            "segment": self.segment,
            "game": self.game,
            "data": {
                "total_rounds": player_data["total_rounds"],
                "kd": player_data["kd"],
                "rating": player_data["rating"]
            }
        }
        incremental_collection.insert_one(doc)

    # 2. Read (Find) documents by segment and game
    def read_data(self):
        query = {"segment": self.segment, "game": self.game}
        doc = incremental_collection.find_one(query)
        return doc

    # 3. Update - Add a new player features and target in the data fields for a given segment and game
    def update_data(self, new_data):
        query = {"segment": self.segment, "game": self.game}
        newvalues = {"$set": {
            "data": {
                "total_rounds": new_data["total_rounds"],
                "kd": new_data["kd"],
                "rating": new_data["rating"]
            }
        }}
        
        incremental_collection.update_one(query, newvalues)

    # 4. Delete - Remove a document by segment and game
    def delete_data(self):
        delete_query = {"segment": self.segment, "game": self.game}
        incremental_collection.delete_one(delete_query)
        
    # 5. Reset - Remove the data from the document for a given segment and game
    def reset_data(self):
        query = {"segment": self.segment, "game": self.game}
        newvalues = {"$set": {
            "data": {}
            }}
        incremental_collection.update_one(query, newvalues)

# ==== ML MODELS CRUD ====

''' 
mlmodels collection document structure:
{   
    "segment": "", # String
    "game": "", # String
    "model_type": "", # String, e.g. "prediction" or "recommendation"
    "model_binary": Binary(pickle.dumps(model)) # Binary data of the model
}
'''

class ModelCrud:
    def __init__(self, segment, game):
        self.segment = segment
        self.game = game
        

    def create_mlmodel(self, model_type, model_bytes):
        """
        model_bytes: raw bytes of your model binary (e.g. pickle, joblib, protobuf)
        """
        doc = {
            "segment": self.segment,
            "game": self.game,
            "model_type": model_type,
            "model_binary": model_bytes,
        }
        mlmodels_collection.insert_one(doc)


    def read_mlmodel(self, model_type=None):
        query = {}
        if self.segment:
            query["segment"] = self.segment
        if self.game:
            query["game"] = self.game
        if model_type:
            query["model_type"] = model_type
        
        return mlmodels_collection.find_one(query)['model_binary']


    def update_mlmodel(self, model_type, model_bytes):
        """
        model_bytes: raw bytes of your model binary (e.g. pickle, joblib, protobuf)
        """
        update_doc = {}
        update_doc['model_binary'] = model_bytes

        update = {
            "$set": update_doc
        }

        query = {"segment": self.segment, "game": self.game, "model_type": model_type}
        mlmodels_collection.update_one(query, update)


    def delete_mlmodel(self, model_type):
        query = {"segment": self.segment, "game": self.game, "model_type": model_type}
        mlmodels_collection.delete_one(query)
