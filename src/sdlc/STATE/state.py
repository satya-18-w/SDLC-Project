from pydantic import BaseModel,Field
from typing import Any,Dict,Literal,Annotated
from typing_extensions import TypedDict
import json
from src.sdlc.utils import constants


class UserStory(BaseModel):
    id: int = Field(...,example=1,description="the key that uniquely identify the user story")
    title: str = Field(...,description="the titleof the user story")
    description: str = Field(...,description="The complete description of the user story")
    priority: int = Field(...,description="The priority of the user story")
    acceptance_criteria: str = Field(...,description="The acceptance critreia of the user story")
    
    
class UserStoryList(BaseModel):
    user_stories: list[UserStory]
    
    
class DesignDocument(BaseModel):
    functional: str = Field(...,descritpion="Holds the functional requirements of the design document")
    technical: str = Field(..., description="Holds the technical requirements of the design document")
    
    

class SDLCState(TypedDict):
    next_node: str =constants.PROJECT_INITILIZATION
    project_name: str
    requirements: list[str]
    user_stories: UserStoryList
    user_stories_feedback: str
    user_stories_review_status: str
    design_documents: DesignDocument
    design_documents_feedback: str
    design_documents_review_status: str
    code_generated: str
    code_review_comments: str
    code_review_feedback: str
    code_review_status: str
    test_cases: str
    test_cases_review_status: str
    test_cases_review_feedback: str
    qa_testing_comments: str
    qa_testing_status: str
    qa_testing_feedback: str
    deployment_status: str
    deployment_feedback: str
    artifacts: dict[str,str]
    
    
    

    
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object is any kind of Pydantic model
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        # Or check for specific classes if needed
        # if isinstance(obj, UserStories) or isinstance(obj, DesignDocument):
        #     return obj.model_dump()
        return super().default(obj)