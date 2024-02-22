import aiohttp
import json
import asyncio

class BeaconChainProvider():
    def __init__(self, api_key):
        self.api_key = api_key
        self.cache = {
            "balancehistory": {}
        }

    async def query(self, query: str):
        json_data = None
        cnts = 0
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(query) as response:
                        json_data = await response.json()
                        #error handling check status
                        return json_data
            except Exception as e:
                print(f"Error fetching data from beacon api node: {e}")
                raise e

    async def post(self, query: str, body):
        json_data = None
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    serialized_body = json.dumps(body)
                    async with session.post(query, data=serialized_body.encode('utf-8')) as response:
                        json_data = await response.json()
                        #error handling check status
                        return json_data
            except Exception as e:
                print(f"Error posting to beacon node: {e}")
                raise e
            
    def test(self):
        print("test")
        return 1
        
    async def fetch_slot_info(self, slot: str):
        return 0

    async def balance_history(self, index, epoch: int):
        return 0


    async def fetch_validator_info(self, index: str):
                return {}

    async def fetch_latest_epoch(self):
        return 0

    async def fetch_queue_info(self) -> int:
        return 0
    
    