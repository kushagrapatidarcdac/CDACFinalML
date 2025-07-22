from fastapi import FastAPI
from app.routes import predictrating, profilerecommendations, update


app = FastAPI()

#routes={"Predict Player Rating":'/predictrating',"Incremental Learner":'/incrementallearner',"Profile Recommendations":'/profilerecommendations',"Feed Recommendations":'/feedrecommenations'}
routes=[predictrating, update, profilerecommendations]

@app.get('/')
def root():
    return {'Available Routes': [route.router.prefix for route in routes]}

for route in routes:
    app.include_router(route.router)



