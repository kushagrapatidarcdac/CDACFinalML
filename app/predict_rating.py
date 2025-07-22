# import app.train_newrating_predict as tnrp
import joblib

# Load the trained model
def getModel(segment,game):
    segment = segment.lower()
    game=game.lower()
    # Load the saved model        
    model = joblib.load('app\mlmodels\\'+segment+'\\'+game+'\prediction\predict_rating.pkl')
    return model


# Predict Rating
def predict_rating(segment,game,total_rounds,kd):
    loaded_model=getModel(segment,game)

    # Example prediction with loaded model
    sample_player = [[total_rounds,kd]]
    predicted_rating = loaded_model.predict(sample_player)
    
    return predicted_rating[0]

# Main
if __name__=="__main__":
    segment='Esports'
    game='Valorant'
    total_rounds=569
    kd=0.9 #win/loss
    rating=predict_rating(segment,game,569, 0.9)
    print(f"\nPredicted Rating for Sample Player: {rating:.2f}")
    # tnrp.trainNewRating(game, total_rounds, kd, rating)
