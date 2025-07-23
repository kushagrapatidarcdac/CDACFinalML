import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors

# Existing database of players
players = pd.DataFrame([
    {"player_name": "Alice", "country": "USA", "total_rounds": 10, "kd": 1.4, "rating": 22.0},
    {"player_name": "Bob",   "country": "UK",  "total_rounds": 14, "kd": 1.1, "rating": 20.5},
    # ... other players
])
feature_cols = ["country", "total_rounds", "kd", "rating"]

encoder = OneHotEncoder()
scaler = StandardScaler()
X_country = encoder.fit_transform(players[["country"]]).toarray()
X_numeric = scaler.fit_transform(players[["total_rounds", "kd", "rating"]])
X = pd.concat([
    pd.DataFrame(X_country, index=players.index),
    pd.DataFrame(X_numeric, index=players.index)
], axis=1)

knn = NearestNeighbors(n_neighbors=3, metric='cosine')
knn.fit(X)

# Function to incrementally add new player
def add_new_player(new_record):
    global players, knn, encoder, scaler, X
    players = pd.concat([players, pd.DataFrame([new_record])], ignore_index=True)
    X_country = encoder.fit_transform(players[["country"]]).toarray()
    X_numeric = scaler.fit_transform(players[["total_rounds", "kd", "rating"]])
    X = pd.concat([
        pd.DataFrame(X_country, index=players.index),
        pd.DataFrame(X_numeric, index=players.index)
    ], axis=1)
    knn.fit(X)  # Refit; for very large datasets, use incremental index updates

# When new data arrives:
add_new_player({"player_name": "Carol", "country": "USA", "total_rounds": 8, "kd": 1.7, "rating": 23})

# Recommend players for a query profile
query = pd.DataFrame([{"country": "USA", "total_rounds": 11, "kd": 1.5, "rating": 21.8}])
X_query_country = encoder.transform(query[["country"]]).toarray()
X_query_numeric = scaler.transform(query[["total_rounds", "kd", "rating"]])
X_query = pd.concat([
    pd.DataFrame(X_query_country),
    pd.DataFrame(X_query_numeric)
], axis=1)

dists, indices = knn.kneighbors(X_query)
recommended_indices = indices.flatten()
recommended_players = players.iloc[recommended_indices]["player_name"].tolist()
print("Recommended players:", recommended_players)
