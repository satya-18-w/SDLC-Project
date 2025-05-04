import redis
import json
from typing import Optional
from src.sdlc.STATE.state import SDLCState,CustomEncoder
from upstash_redis import Redis
import os
from dotenv import load_dotenv
from loguru import logger


load_dotenv()

# Initialize the redis client
REDIS_URL=os.getenv("REDIS_URL")
REDIS_TOKEN=os.getenv("REDIS_TOKEN")
redis_client=Redis(url=REDIS_URL,token=REDIS_TOKEN)



def save_state_to_redis(task_id:str,stateLSDLCState):
    "Save the state to redis"
    state=json.dumps(state,cls=CustomEncoder)
    
    #Expired after 24 Hours
    redis_client.expire(task_id,86400)
    
    
def get_state_from_redis(task_id: str) -> Optional[SDLCState]:
    "Get the state from redis"
    
    state_json=redis_client.get(task_id)
    if not state_json:
        return None
    state_dict=json.loads(state_json)[0]
    return SDLCState(**state_dict)

def delete_from_redis(task_id:str):
    """ Delete from Redis"""
    redis_client.delete(task_id)
    
def flush_redis_cache():
    """ Flus the Redis Cache """
    #Clear all the keys in all databases
    redis_client.flushall()
    logger.info("---Redis cache cleared----")