import json
from typing import Any
import time
import aiohttp
import asyncio
from constant import constants
PAGINATION_LIMIT = 1000

class Subgraph():

    def __init__(self, network: str):
        self.network = network
        self.config_map = {
            "mainnet": {
                "graph_url": "https://gateway-arbitrum.network.thegraph.com/api/73b09012e7e6301b5e0e20b45fd66b48/deployments/id/" + constants["SUBGRAPH_API_KEY"],
            }
        }
        self.queries = {
            "validators": '''
            query GetValidators($limit: Int!, $value: String!) {
              validators(
                first: $limit
                where: { id_gt: $value }
              ) {
                id
                validatorPubKey
                BNFTHolder
                TNFTHolder
                etherfiNode
                bid {
                  bidderAddress
                }
              }
            }
            ''',
        }

    async def query_graph(self, query: str, field_name: str, variables: dict[str, Any]):
        GRAPH_URL = self.config_map[self.network]["graph_url"]
        async with aiohttp.ClientSession() as session:
            async with session.post(GRAPH_URL, json={'query': query, 'variables': variables}) as response:
                data = await response.json()
                if 'data' in data and field_name in data['data']:
                    return data['data'][field_name]
                else:
                    raise Exception(f"Error fetching data from subgraph: {data}")
      
    async def fetch_large_data_from_graph(self, query: str, field_name: str):   
        try:
            async def get_batch(value):
                try:
                    variables = {'limit': PAGINATION_LIMIT, 'value': value}
                    res = await self.query_graph(query, field_name, variables)
                    return res
                except Exception as error:
                    raise Exception(str(error))
            res = []
            value = " "
            while True:
                batch = await get_batch(value)
                res.extend(batch)
                if len(batch) < PAGINATION_LIMIT:
                    break
                
                value = batch[-1]["id"]
                time.sleep(0.1)
            print("length of large data is: ", len(res))
            return res
        except Exception as error:
            raise Exception("Error: query_from_graph: {}".format(error))
        
    async def fetch_validators(self):
        query = self.queries["validators"]
        validators = await self.fetch_large_data_from_graph(query, "validators")
        print("Total validators in graph is:" , len(validators))
        return validators

    
    