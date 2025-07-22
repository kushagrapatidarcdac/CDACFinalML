import app.train_rating_predict as trp
import app.predict_rating as pr

import numpy as np
from sklearn.pipeline import make_pipeline

# Prepare the New Data
def prepNewData(total_rounds,kd,rating):
    X_new = np.array([total_rounds,kd])
    y_new = np.array([rating])

    return X_new,y_new

# Extract the scaler and regressor from the pipeline
def extractPipeline(sgd_pipeline):
    scaler = sgd_pipeline.named_steps['standardscaler']
    regressor = sgd_pipeline.named_steps['sgdregressor']

    return scaler, regressor

# Partial it scaler on new features
def partialFitScaler(scaler,X_new):
    # Update the scaler with the new data
    scaler.partial_fit(X_new)

    # Scale the new data
    X_new_scaled = scaler.transform(X_new)

    return X_new_scaled

# Partial fit regressor on new data
def partialFitRegressor(regressor,X_new_scaled,y_new):
    regressor.partial_fit(X_new_scaled, y_new)

    return regressor

def setPipeline(sgd_regressor,scaler,regressor):
    sgd_regressor = make_pipeline([
        scaler,
        regressor
    ])
    return sgd_regressor

# Increamental Learing
def trainNewRating(segement,game, total_rounds,kd,rating):

    # Prepare the New Data
    X_new,y_new=prepNewData(total_rounds,kd,rating)
    
    # Initialize the Pipeline
    pipeline=pr.getModel(game)

    # Extract the scaler and regressor from the pipeline
    scaler,regressor=extractPipeline(pipeline)

    # Scale the new Features
    X_new_scaled=partialFitScaler(scaler,X_new)

    # Partial fit the regressor on the new data
    regressor=partialFitRegressor(regressor,X_new_scaled,y_new)

    # Get the pipline filename for the game
    gamefile=trp.getGameData(segement,game, X_new_scaled, y_new)[-1]

    pipeline=setPipeline(pipeline,scaler,regressor)

    trp.savePipeline(pipeline,gamefile)