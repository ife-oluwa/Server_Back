from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from Database.models import User, Predictions
from schemas import PredictionModel
from fastapi.exceptions import HTTPException
from Database.database import session, engine
from fastapi.encoders import jsonable_encoder

predict_router = APIRouter(
    prefix='/predictions',
    tags=['Predictions']
)

session = session(bind=engine)

@predict_router.get('/')
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return {"message": "Hello World"}

@predict_router.post('/predict', status_code=status.HTTP_201_CREATED)
async def prediction(Predict: PredictionModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()


    new_prediction = Predictions(
        date_created= Predict.date_created,
        predictions = Predict.predictions
    )
    #### Model processing ####



    ############################

    new_prediction.user = user
    
    session.add(new_prediction)
    session.commit()

    response = {
        "dates": [new_prediction.date_created],
        "predictions": new_prediction.predictions,

    }

    return jsonable_encoder(response)

@predict_router.get('/predictions')
async def getAllPredictions(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    current_user = Authorize.get_jwt_subject()
    user= session.query(User).filter(User.username==current_user).first()

    if user.is_admin:
        predictions = session.query(Predictions).all()

        return jsonable_encoder(predictions)
    
    raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                        detail = "You are not an administrator.") 