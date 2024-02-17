from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from db import engine
from router import auth

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Intro": "SUST Project Backend"}


app.include_router(auth.router)
