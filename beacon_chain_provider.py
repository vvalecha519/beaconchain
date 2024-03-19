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
    
    async def fetch_batch_validator_info(self, validators: list):
        suffix_url = "eth/v1/beacon/states/head/validators?key=" + self.api_key
        res = await self.post(self.url + suffix_url, {'ids': validators})
        print("fetching batch validator info")
        return res

    async def fetch_validator_info(self, validators: list[str]): #validators can be either indices or pubkeys
        print("fetching validator info")
        try:
            validators_info = []
            total_validators = len(validators)
            batched_validator_info = []
            for start in range(0, total_validators, 64*64):
                end = min(start+64*64, total_validators)
                tasks = [self.fetch_batch_validator_info(validators[j: min(j+64, total_validators)]) for j in range(start, end, 64)]
                batched_validator_info.extend(await asyncio.gather(*tasks))
            for batch in batched_validator_info:
                validators_info.extend(batch["data"])
            print("len of validator info ", len(validators_info))
        except Exception as e:
            print(f"Error fetching validator info: {e}")
            return {'status': f"Error fetching validator info: {e}", 'data': None}
        return {'status': "OK", 'data': self.flatten_validator_info(validators_info)}
    
    def flatten_validator_info(self, l):
        validators_info = []
        for validator in l:
            flatten_info = {
                "index": validator["index"],
                "balance": validator["balance"],
                "status": validator["status"],
                "pubkey": validator["validator"]["pubkey"],
                "withdrawal_credentials": validator["validator"]["withdrawal_credentials"],
                "effective_balance": validator["validator"]["effective_balance"],
                "slashed": validator["validator"]["slashed"],
                "activation_eligibility_epoch": validator["validator"]["activation_eligibility_epoch"],
                "activation_epoch": validator["validator"]["activation_epoch"],
                "exit_epoch": validator["validator"]["exit_epoch"],
                "withdrawable_epoch": validator["validator"]["withdrawable_epoch"]
            }
            validators_info.append(flatten_info)
        return validators_info

    async def fetch_latest_epoch(self):
        return 0

    async def fetch_queue_info(self) -> int:
        return 0
    
    