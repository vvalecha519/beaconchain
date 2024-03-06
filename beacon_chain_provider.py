import aiohttp
import json
import asyncio
from subgraph import Subgraph
import ssl
import math

class BeaconChainProvider():
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://beacon.6r4i7nz1iqzyzulw1qntu3yt8.blockchainnodeengine.com/"
        self.cache = {
            "balancehistory": {}
        }
        self.graph = Subgraph("mainnet")

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
        context = ssl._create_unverified_context()
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    serialized_body = json.dumps(body)
                    async with session.post(query, json=body) as response:
                        json_data = await response.json()
                        #error handling check status
                        return json_data
            except Exception as e:
                print(f"Error posting to beacon node: {e}")
                raise e
        
    async def fetch_slot_info(self, slot: str):
        return 0

    async def balance_history(self, index, epoch: int):
        return 0
    
    async def fetch_batch_validator_info(self, pubkeys: list):
        suffix_url = "eth/v1/beacon/states/head/validators?key=" + self.api_key
        res = await self.post(self.url + suffix_url, {'ids': pubkeys})
        return res

    async def fetch_validator_info(self):
        print("fetching validator info")
        validators = await self.graph.fetch_validators()
        pubkeys = []
        for validator in validators:
            pubkey = validator["validatorPubKey"]
            if(pubkey == None or len(pubkey) != 98):
                continue
            pubkeys.append(pubkey)
        validators_info = []
        total_validators = len(pubkeys)
        batched_validator_info = []
        for start in range(0, total_validators, 64*64):
            end = min(start+64*64, total_validators)
            tasks = [self.fetch_batch_validator_info(pubkeys[j: min(j+64, total_validators)]) for j in range(start, end, 64)]
            batched_validator_info.extend(await asyncio.gather(*tasks))
        for batch in batched_validator_info:
            print(batch)
            validators_info.extend(batch["data"])
            print("len of batch ", len(batch["data"]))
        print("len of validator info ", len(validators_info))
        return validators_info

    async def fetch_latest_epoch(self):
        return 0

    async def fetch_queue_info(self) -> int:
        return 0
    
    