from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import NearestNeighbors
import app.train_rating_predict as trp
import pandas as pd

# Preprocess Pipeline
def preprocessPipeline():
    preprocessor = ColumnTransformer(
    transformers=[
        ('game', OneHotEncoder(), ['game']),
        ('num', StandardScaler(), ['kd', 'rating', 'total_rounds'])
    ])
    
    return preprocessor

# Similarity Model
def buildModel():
    model = NearestNeighbors(n_neighbors=3, metric='cosine')
    
    return model

# Train Model
def trainModel(data):
    model=buildModel()
    preprocessor=preprocessPipeline()
    X=preprocessor.fit_transform(data)
    model.fit(X)
    
    return model,X

# Recommend Players using Similarity Model
def recommend_connections(data, target_player_name, n):
    model, X= trainModel(data)
    target_idx = data[data['player_name'] == target_player_name].index[0]
    distances, indices = model.kneighbors(X[target_idx].reshape(1, -1), n+1)
    
    del distances
    
    # Exclude self and return the recommendations
    return data.iloc[indices[0][1:]]['player_name']



# Recommend Players
def recommendPlayers(data, target_player_name, segment, game, n):
    recommendedplayers=[]
    data=pd.DataFrame(data)
    datas,games=trp.prepData(data)
    data=datas[game]
    del(datas)
    del(games)

    recommendedplayers=recommend_connections(data, target_player_name,n)
        
    return list(recommendedplayers)


if __name__ == "__main__":
    game = "Valorant"
    target_player_name="mezoky"
    recommendedplayers=recommendPlayers(game, target_player_name)
    
    
    print(recommendedplayers)