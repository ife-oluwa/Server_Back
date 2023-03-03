from fastapi import FastAPI
import uvicorn
from routers.admin import auth_router
from routers.prediction_routes import predict_router

description = """
    ## This collection of API routes manage the backend services for the machine learning service.
"""

tags_metadata = [
    {
        "name": "Auth",
        "description": "Authentication related routes."
    },
    {
        "name": "User",
        "description": "User related routes."
    },
    {
        "name": "Predictions",
        "description": "Predictions related routes."
    },
]

app = FastAPI(
    title="Timeseries model APIs",
    description=description,
    version='0.0.1',
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json")


app.include_router(auth_router)
app.include_router(predict_router)



@app.get('/', tags=['Predictions'])
def index():
    return { "message": "Hello" }


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, reload= True)