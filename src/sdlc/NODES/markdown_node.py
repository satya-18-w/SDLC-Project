import os
import json
from src.sdlc.STATE.state import SDLCState
from src.sdlc.utils.Utility import Utility
from loguru import logger

class MerkdownArtifactsNode:
    """
    Graph Node for generating markdown artifacts for sdlc process
    This Node generates markdown files for:
    - Project requirements
    - User Stories
    - Design Documents
    - Generated COde
    
    save them to 'artifacts' folder
    """
    def __init__(self):
        self.utility=Utility()
        
        
    def generate_markdown_artifacts(self,state: SDLCState):
        """
        Generate Markdown files for each step in SDLC state and save them to artifacts folder.
        Returns the updated state with a new key 'artifacts' that maps to a directory offile path
        """
        artifacts_dir="artifacts"
        os.makedirs(artifacts_dir,exist_ok=True)
        project_name=state.get("project_name","Project")
        # Project Requirements Markdown
        requirements=state.get("requirements",[])
        md_project=f"# Project Requirements for {project_name}\n\n ## Requirements: \n {self.utility.format_list(requirements)}"
        file_project=os.path.join(artifacts_dir,"Project_Requirements.md")
        with open(file_project,"w") as f:
            f.write(md_project)
            
            
            
        # Security Recomendations MARKDOWN
        security_recomendations=state.get("security_recomentaions",None)
        file_security=None
        if security_recomendations:
            md_security=f"# Security Recimendations for {project_name}\n\n"
            md_security+=security_recomendations
            file_security=os.path.join(artifacts_dir,"Security_Recomendations.md")
            with open(file_security,"w") as f:
                f.write(md_security)
                
                
        # -- Generated Code Markdown --
        code_generated = state.get("code_generated", None)
        file_code = None
        if code_generated:
            md_code = f"# Generated Code for {project_name}\n\n"
            md_code += "\n" + code_generated
            file_code = os.path.join(artifacts_dir, "Generated_Code.md")
            with open(file_code, "w") as f:
                f.write(md_code)
            
            
        # -- Test Cases Markdown --
        test_cases = state.get("test_cases", None)
        file_tests = None
        if test_cases:
            md_tests = f"# Test Cases for {project_name}\n\n"
            md_tests += "\n" + test_cases
            file_tests = os.path.join(artifacts_dir, "Test_Cases.md")
            with open(file_tests, "w") as f:
                f.write(md_tests)
        
        # -- QA Testing Comments Markdown --
        qa_testing_comments = state.get("qa_testing_comments", None)
        file_qa = None
        if qa_testing_comments:
            md_qa = f"# QA Testing Comments for {project_name}\n\n"
            md_qa += qa_testing_comments
            file_qa = os.path.join(artifacts_dir, "QA_Testing_Comments.md")
            with open(file_qa, "w") as f:
                f.write(md_qa)
        
        
        
        # -- Deployment Feedback Markdown --
        deployment_feedback = state.get("deployment_feedback", None)
        file_deployment = None
        if deployment_feedback:
            md_deployment = f"# Deployment Feedback for {project_name}\n\n"
            md_deployment += deployment_feedback
            file_deployment = os.path.join(artifacts_dir, "Deployment_Feedback.md")
            with open(file_deployment, "w") as f:
                f.write(md_deployment)
               
               
               
        
        # -- User Stories Markdown --
        user_stories = state.get("user_stories", None)
        file_stories = None
        if user_stories:
            md_stories = f"# User Stories for {project_name}\n\n"
            md_stories += self.utility.format_user_stories(user_stories)
            file_stories = os.path.join(artifacts_dir, "User_Stories.md")
            with open(file_stories, "w") as f:
                f.write(md_stories)
        
        
        
        # -- Design Documents Markdown --
        design_docs = state.get("design_documents", None)
        file_design = None
        if design_docs:
            md_design = f"# Design Documents for {project_name}\n\n"
            md_design += "## Functional Design Document\n"
            md_design += design_docs.get("functional", "No Functional Design Document available.")
            md_design += "\n\n## Technical Design Document\n"
            md_design += design_docs.get("technical", "No Technical Design Document available.")
            file_design = os.path.join(artifacts_dir, "Design_Documents.md")
            with open(file_design, "w") as f:
                f.write(md_design)
        
         
        # Update the state with the paths to the generated artifact files.
        state["artifacts"] = {
            "Project_Requirements": file_project,
            "User_Stories": file_stories,
            "Design_Documents": file_design,
            "Generated_Code": file_code,
            "Security_Recommendations": file_security,
            "Test_Cases": file_tests,
            "QA_Testing_Comments": file_qa,
            "Deployment_Feedback": file_deployment
        }
        logger.info("Markdown artifacts generated in folder:", artifacts_dir)
        return state