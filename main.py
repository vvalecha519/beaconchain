from fastapi import FastAPI
from api import api_router
from dotenv import load_dotenv
import os
from subgraph import Subgraph
app = FastAPI()
app.include_router(api_router, prefix="/api")

def main():
    load_dotenv()

@app.on_event("startup")
async def startup_event():
    print("Starting up")
