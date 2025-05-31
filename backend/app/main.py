from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import plans

app = FastAPI()
app.include_router(plans.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)