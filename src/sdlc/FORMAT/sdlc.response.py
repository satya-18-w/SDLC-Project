from pydantic import BaseModel
from typing import Optional,Dict,Any

class SDLCResponse(BaseModel):
    status: str
    message: str
    task_id: Optional[str] = None
    state: Optional[Dict[str,Any]] = None
    error: Optional[str] = None
    
