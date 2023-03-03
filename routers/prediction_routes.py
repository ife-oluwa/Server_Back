from fastapi import APIRouter

predict_router = APIRouter(
    prefix='/predictions',
    tags=['Predictions']
)

@predict_router.get('/')
async def hello():
    return {"message": "Hello World"}