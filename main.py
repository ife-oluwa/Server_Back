from fastapi import FastAPI

description = """
    ## This collection of API routes manage the backend services for the machine learning service.
"""

tags_metadata = [
    {
        "name": "Authentication",
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

@app.get('/', tags=['Predictions'])
def index():
    return { "message": "Hello" }