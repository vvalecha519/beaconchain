from fastapi import FastAPI
from api import api_router
from dotenv import load_dotenv
import os

app = FastAPI()
app.include_router(api_router, prefix="/api")

def main():
    load_dotenv()

@app.on_event("startup")
async def startup_event():
    print("Starting up")

#beacon_api = beaconChainProvider()