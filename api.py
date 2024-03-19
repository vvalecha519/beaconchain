from fastapi import APIRouter
from beacon_chain_provider import BeaconChainProvider
from constant import constants
from pydantic import BaseModel


api_router = APIRouter()

# @api_router.get("/")
# async def root():
#     return {"message": "Hello World"}

# @api_router.get("/epoch/latest")
# async def getLatestEpoch():
#     return 1

# @api_router.get("/slot")
# async def getSlot(slot: int):
#     return 1

class ValidatorsPostRequest(BaseModel):
    indicesOrPubkey: str

@api_router.post("/validator")
async def validators(request: ValidatorsPostRequest):
    indices_or_pubkey = request.indicesOrPubkey
    validators = indices_or_pubkey.split(",")
    print(validators)
    beaconapi = BeaconChainProvider(constants["BEACON_API_KEY"])
    return await beaconapi.fetch_validator_info(validators)
    return {}

# @api_router.get("/validator/{validator_id}/balancehistory")
# async def getValidatorBalanceHistory(validator_id: int, epoch: int, offset: int, limit: int):
#     return 1

# @api_router.get("/queue")
# async def getValidatorBalanceHistory(validator_id: int, epoch: int, offset: int, limit: int):
#     beaconapi = BeaconChainProvider(constants["BEACON_API_KEY"])
#     return await beaconapi.fetch_validator_info()


#beaconchain api used by oracle:
# a)https://beaconcha.in/api/v1/validators/queue (not used)
#   {"data": { "beaconchain_entering": 3796, "beaconchain_exiting": 3178, "validatorscount": 958223 }}

# b)https://beaconcha.in/api/v1/validator/1000/balancehistory?latest_epoch=264955&offset=0&limit=1 (everything)
#   # {"data": [ { "balance": 0, "effectivebalance": 0, "epoch": 264955, "validatorindex": 1000, "week": 168, "week_start": "2024-02-20T12:00:23Z", "week_end": "2024-02-27T12:00:23Z"}]}

# c)https://beaconcha.in/api/v1/validator (everything)
# { "data": {"activationeligibilityepoch": 0,"activationepoch": 0,"balance": 0,"effectivebalance": 0,
# "exitepoch": 200316,"lastattestationslot": 16,"name": "",
# "pubkey": "0xb18e1737e1a1a76b8dff905ba7a4cb1ff5c526a4b7b0788188aade0488274c91e9c797e75f0f8452384ff53d44fad3df",
# "slashed": false,"status": "exited","validatorindex": 1000,"withdrawableepoch": 200572,
# "withdrawalcredentials": "0x010000000000000000000000347ac2e04dd10cbf70f65c058ac3a078d4d9e0e5","total_withdrawals": 35782660631

# d)https://beaconcha.in/api/v1/epoch/latest (not used)
   # {"attestationscount": 0,"attesterslashingscount": 0,"averagevalidatorbalance": 32069838695,"blockscount": 0,"depositscount": 0,"eligibleether": 30662763000000000,"epoch": 264953,"finalized": false,"globalparticipationrate": 0,"missedblocks": 0,"orphanedblocks": 0,"proposedblocks": 29,"proposerslashingscount": 0,"rewards_exported": false,"scheduledblocks": 0,"totalvalidatorbalance": 30730057044223364,"ts": "2024-02-22T01:39:35Z","validatorscount": 958223,"voluntaryexitscount": 0,"votedether": 0,"withdrawalcount": 0}

# e)https://beaconcha.in/api/v1/slot/1000  
# required: slot_info["exec_block_number"]
#{"attestationscount": 0,"attesterslashingscount": 0,"blockroot": "string","depositscount": 0,"epoch": 0,"eth1data_blockhash": "string","eth1data_depositcount": 0,"eth1data_depositroot": "string","exec_base_fee_per_gas": 0,"exec_block_hash": "string","exec_block_number": 0,"exec_extra_data": "string","exec_fee_recipient": "string","exec_gas_limit": 0,"exec_gas_used": 0,"exec_logs_bloom": "string","exec_parent_hash": "string","exec_random": "string","exec_receipts_root": "string","exec_state_root": "string","exec_timestamp": 0,"exec_transactions_count": 0,"graffiti": "string","graffiti_text": "string","parentroot": "string","proposer": 0,"proposerslashingscount": 0,"randaoreveal": "string","signature": "string","slot": 0,"stateroot": "string","status": "string","syncaggregate_bits": "string","syncaggregate_participation": 0,"syncaggregate_signature": "string","voluntaryexitscount": 0,"withdrawalcount": 0}
 