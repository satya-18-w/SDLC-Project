from src.sdlc.STATE.state import SDLCState,UserStory,UserStoryList
from langchain_core.messages import SystemMessage,AIMessage


class ProjectRequirementNode:
    """
    Node for the project requirement
    """
    
    def __init__(self,llm):
        self.llm=llm
        
        
    def initialize_project(self,state: SDLCState):
        " Project initialization state "
        return state
    def get_user_requirements(self,state: SDLCState):
        """
            Gets the requirements from the user
        """
        pass
    
    def generate_user_stories(self,state: SDLCState):
        """
        Auto generate highly detailed and accurate user stories for each requirement.
        """
        project_name=state["project_name"]
        requirement=state["requirements"]
        feedback_reason = state.get("user_stories_feedback")
        prompt=f"""
        You are a senior software analyst specializing in agile agentic ai app development and user story generation.
        your task is to generate **a separate and well detailed user story for each requirements**from the details given below
        
        PROJECT NAME: {project_name}
        REQUIREMENTS: {requirement}
        
        Instruction for the user story generation:
        - Generate one story for one requirement.
        - Assign a uniqueidentifier (eg.US-001,US-002,etc).
        - Provide a clear and concise description of the user story.
        - write a DETAIL DESCRIPTION using the " As a [user role], iwant [goal] so that [benifit]" format.
        - Assign a **priority level** (1 = Critical, 2 = High, 3 = Medium, 4 = Low).
        - Define **acceptance criteria** with bullet points to ensure testability.
        - Use **domain-specific terminology** for clarity.
        
        
        {f"Additionally , consider the following feedback while refining the user stories: {feedback_reason}" if feedback_reason else ""}
        -----
        **Expected Output Format(For each user Stories):**
        - Unique Identifier: US-XXX
        - Title: [User story title]
        - description
        - As a [user role],  i want [feature] so that [benifit].
        - Priority: [1-4]
        - Acceptance Criteria: [list of bullet points]
        
        ** ensure that user stories are specific,testable and aligined with agile principles**.
        """
        
        llm_with_str=self.llm.with_structured_output(UserStoryList)
        response=llm_with_str.invoke(prompt)
        state["user_stories"]=response
        return state
    
        
    def review_user_stories(self, state: SDLCState):
        return state
    
    def revise_user_stories(self, state: SDLCState):
        pass
    
    def review_user_stories_router(self, state: SDLCState):
        return state.get("user_stories_review_status", "approved") 