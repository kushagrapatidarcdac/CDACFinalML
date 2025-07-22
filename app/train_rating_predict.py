# Libraries
import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import joblib

# Import the Data
def importData(fileloc):
    try:
        return pd.read_csv(fileloc),True
    except:
        print("File not Found")
        return None,False

# Split Data According to games
def prepData(data):
    games=list(data.game.unique())
    datas={}
    for game in games:
        datas[game] = data[data.game==game]
        datas[game]=datas[game].reset_index(drop=True)
    return datas,games

# Split into Features and Targets
def getFTs(datas,games):
    Xs={}
    ys={}

    for game in games:
        # Extract features and target from the game
        datatemp=datas[game]
        Xs[game]=datatemp[["total_rounds","kd"]]
        ys[game]=datatemp['rating']
    
    return Xs,ys

# Get the Features, Targets and FilePath for a game
def getGameData(segment,game,Xs,ys):
    X=Xs[game]
    y=ys[game]
    segment = segment.lower()
    game=game.lower()
    filename='app\mlmodels\\'+segment+'\\'+game+'\prediction\predict_rating.pkl'
    return X,y,filename

# Initialize Pipeline: scaling + SGDRegressor
def initPipeline():
    sgd_pipeline = make_pipeline(
        StandardScaler(),
        SGDRegressor(max_iter=1000, tol=1e-3, random_state=42)
    )

    return sgd_pipeline

# Train the Pipeline
def trainPipeline(sgd_pipeline,X,y):
    sgd_pipeline.fit(X,y)
    return sgd_pipeline

# Save the Pipeline
def savePipeline(sgd_pipeline,filename):
    joblib.dump(sgd_pipeline,filename)

# Main
if __name__=="__main__":
    data,flag=importData('../datasets/datacombined/player_combined_stats.csv')
    if flag:
        datas,games=prepData(data)
        Xs,ys=getFTs(datas,games)
        segment='Esports'
        for game in games:
            X,y,filename=getGameData(segment,game,Xs,ys)

            sgd_pipline=initPipeline()
            
            sgd_pipline=trainPipeline(sgd_pipline,X,y)

            savePipeline(sgd_pipline,filename)





