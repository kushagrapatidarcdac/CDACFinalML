from bson import Binary
from database import db

# ==== Database Collections ====
datasets_collection = db['datasets']
incremental_collection = db['incrementaldatasets']
mlmodels_collection = db['mlmodels']



# ==== DATASETS CRUD ====

'''
datasets collection document structure:
{   
    "segment": "", # String
    "game": "", # String
    "data": {
        "player_name": player_name, # List of String
        "country": country, # List of String
        "team": team, # List of String
        "total_rounds": total_rounds, # List of integers
        "kd": kd, # List of floats
        "rating": rating # List of floats
    }
'''

def create_dataset(segment, game, player_name, country, team, total_rounds, kd, rating):
    doc = {
        "segment": segment,
        "game": game,
        "data": {
            "player_name": player_name,
            "country": country,
            "team": team,
            "total_rounds": total_rounds,
            "kd": kd,
            "rating": rating
        }
    }
    datasets_collection.insert_one(doc)


def read_datasets(segment=None, game=None):
    query = {}
    if segment:
        query["segment"] = segment
    if game:
        query["game"] = game
    return datasets_collection.find(query)


def update_dataset(segment, game, new_data):
    """
    update_data should be a dict with keys for fields inside 'data', e.g.
    {
        "player_name": "new name",
        "kd": 1.5,
        ...
    }
    """
    # Build $set for the nested 'data' field for each key in update_data
    update = {
        "$set": {"data": new_data}
    }
    query = {"segment": segment, "game": game}
    datasets_collection.update_one(query, update)


def delete_dataset(segment, game):
    query = {"segment": segment, "game": game}
    datasets_collection.delete_one(query)

# ==== INCREMENTALDATASETS CRUD ====

'''
incremantaldatasets collection document structure:
{
    "segment": "", # String
    "game": "", # String
    "data": {
        "total_rounds": total_rounds, # List of integers
        "kd": kd, # List of floats
        "rating": rating # List of floats
    }
}
'''

def upsert_incremental(segment, game, new_data):
    query = {
        "segment": segment,
        "game": game
    }
    update = {
        "$set": {
            "data.total_rounds": new_data["total_rounds"],
            "data.kd": new_data["kd"],
            "data.rating": new_data["rating"],
        }
    }
    incremental_collection.update_one(query, update, upsert=True)


def read_incrementals(segment=None, game=None):
    query = {}
    if segment:
        query["segment"] = segment
    if game:
        query["game"] = game
    return incremental_collection.find(query)


def reset_incremental(segment, game):
    query = {"segment": segment, "game": game}
    update = {"$set": {"data": {"total_rounds": [], "kd": [], "rating": []}}}
    incremental_collection.update_one(query, update)




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


def create_mlmodel(segment, game, model_type, model_bytes):
    """
    model_bytes: raw bytes of your model binary (e.g. pickle, joblib, protobuf)
    """
    doc = {
        "segment": segment,
        "game": game,
        "model_type": model_type,
        "model_binary": Binary(model_bytes),
    }
    mlmodels_collection.insert_one(doc)


def read_mlmodel(segment=None, game=None, model_type=None):
    query = {}
    if segment:
        query["segment"] = segment
    if game:
        query["game"] = game
    if model_type:
        query["model_type"] = model_type
    
    return mlmodels_collection.find_one(query)['model_binary']


def update_mlmodel(segment, game, model_type, model_bytes):
    """
    model_bytes: raw bytes of your model binary (e.g. pickle, joblib, protobuf)
    """
    update_doc = {}
    update_doc['model_binary'] = Binary(model_bytes)

    update = {
        "$set": update_doc
    }

    query = {"segment": segment, "game": game, "model_type": model_type}
    mlmodels_collection.update_one(query, update)


def delete_mlmodel(segment, game, model_type):
    query = {"segment": segment, "game": game, "model_type": model_type}
    mlmodels_collection.delete_one(query)
