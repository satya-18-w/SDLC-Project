from src.sdlc.STATE.state import SDLCState
import uuid
import src.sdlc.utils.constants as cons
from src.sdlc.cache.redis_cache import 
from loguru import logger
import redis 

class GraphExecutor:
    def __init__(self,graph):
        self.graph=graph
        
        
    def get_tread(self,task_id):
        return {"configurable":{"tread_id":task_id}}
    
    
    def start_workflow(self,project_name: str):
        task_id=f"sdlc-session-{uuid.uuid4().hex[:8]}"
        thread=self.get_thread(task_id)
        
        state=None
        for event in self.graph.stream({"project_name":project_name},thread,stream_mode="values"):
            state=event
            
        current_state=self.graph.get_state(thread)
        # Redis cache
        
        return {'task_id':task_id,"sstate":state}
    
    #User story Generation
    def generate_stories(self,task_id:str,requirements:list[str]):
        
