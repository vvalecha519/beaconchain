import aiohttp
import json
import asyncio
from subgraph import Subgraph
import ssl
import math

class BeaconChainProvider():
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = f"https://rpc.ankr.com/premium-http/eth_beacon/{api_key}/"
        print(self.url)
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
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    print(query, body)
                    async with session.post(query, json={"ids": ["0xae2a349dc26aa3ced31730eb5f1cb68562071122b02ea8dc5e8136484ab4aa64ce176285cd5bc210190ce663635421b6"]}) as response:
                        json_data = await response.json()
                        #error handling check status
                        return json_data
            except Exception as e:
                print(f"Error posting to beacon node: {e}")
                raise e
        
    async def fetch_slot_info(self, slot: str):
        return 0

    def epoch_to_slot(self, epoch: int):
        return epoch*32
    
    def extract_validators_balance_info(self, validators_info, epoch):
        validators_balance_info = []
        for validator in validators_info:
            print(validator)
            balance_info = {
                "index": validator["index"],
                "effective_balance": validator["effective_balance"],
                "balance": validator["balance"],
                "epoch": epoch
            }
            validators_balance_info.append(balance_info)
        return validators_balance_info

    async def balance_history(self, validators: list, epoch: int, limit: int = 100):
        validators_balance_history = []
        tasks = [self.fetch_validator_info(validators, self.epoch_to_slot(current_epoch)) for current_epoch in range(epoch, epoch-limit, -1)]
        validators_info_per_epoch = await asyncio.gather(*tasks)
        for i, validators_info in enumerate(validators_info_per_epoch):
            current_epoch = epoch - i
            validators_balance_history.extend(self.extract_validators_balance_info(validators_info['data'], current_epoch))
        return validators_balance_history

    async def fetch_batch_validator_info(self, validators: list[str], state="head"):
        url = f"{self.url}eth/v1/beacon/states/{state}/validators"
        print(url)
        try:
            res = await self.post(url, {"ids": validators})
        except Exception as e:
            print(f"Error fetching batch validator info: {e}")
            return {'status': f"Error fetching batch validator info: {e}", 'data': None}
        print("fetching batch validator info")
        return res

    async def fetch_validator_info(self, validators: list[str], state="head"): #validators can be either indices or pubkeys
        print("fetching validator info")
        try:
            validators_info = []
            total_validators = len(validators)
            batched_validator_info = []
            for start in range(0, total_validators, 64*64):
                end = min(start+64*64, total_validators)
                tasks = [self.fetch_batch_validator_info(validators[j: min(j+64, total_validators)], state) for j in range(start, end, 64)]
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
    
    