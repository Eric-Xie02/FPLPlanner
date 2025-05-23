from fastapi import FastAPI
from app.routes import plans

app = FastAPI()
app.include_router(plans.router)
