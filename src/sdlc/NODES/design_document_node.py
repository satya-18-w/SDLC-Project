from src.sdlc.STATE.state import SDLCState,DesignDocument
from src.sdlc.utils.Utility import Utility
## Utility adition remains

from loguru import logger

class DesignDocumentNode:
    """
    Graph Node for the Designing Documents"""
    def __init__(self,llm):
        self.utility=Utility()
        self.llm=llm
        
        
    def create_design_documents(self,state: SDLCState):
        """
        generate the Design document functional and technical
        """
        
        logger.info("-----Creating Design Document-----")
        requirements=state["requirements"]
        user_stories=state["user_stories"]
        project_name=state["project_name"]
        design_feedback=None
        if "design_documents" in state:
            design_feedback=state["design_documents_feedback"]
            
            
        
        
        functional_documents = self.generate_functional_design(
            project_name=project_name,
            requirements=requirements,
            user_stories=user_stories,
            design_feedback=design_feedback
        )
        
        technical_documents = self.generate_technical_design(
            project_name=project_name,
            requirements=requirements,
            user_stories=user_stories,
            design_feedback=design_feedback
        )
        
        design_documents = DesignDocument(
            functional=functional_documents,
            technical = technical_documents
        )
        
        return {
            **state,
            "design_documents":design_documents,
            "technical_documents":technical_documents
        }
        
    
    def generate_functional_design(self,project_name,requirements,user_stories,design_feedback):
        """
        Helper method to generate functional design documents
        """
        logger.info("-----Generating Functional Design Document-----")
        prompt=f"""
        Create a comprehensive functional design documents for {project_name} in markdown format.
        The document should use proper Markdown syntax with headers (# for main titles, ## for sections, etc.), 
            bullet points, tables, and code blocks where appropriate.
            
        Requirements:
            {self.utility.format_list(requirements)}
            
            
        User Stories:
            {self.utility.format_user_stories(user_stories)}
            
            
        {f"When creating this functional design document, please incorporate the following feedback about the requirements: {design_feedback}" if design_feedback else ""}
        
        The functional desig document should include the following sections, each with proper markdown format:
        
        # Functional Design Document: {project_name}
        
        ##1. Introduction and Purpose
        ##2. Project scope
        ##3. User Role and permissions
        ##4. Functional requirement breakdown
        ##5. User Interface Desig Guidlines
        ##6. Bussiness process flows
        ##7. Data Entities and Relationships
        ##8. validation Rules
        ##9. Reporting Requirements
        ## 10. Integration Points
        
        make sure to maintain the proper markdown format throughout the document.
        
        
        """
        response=self.llm.invoke(prompt)
        return response.content
    
    def generate_technical_design(self,
            project_name,
            requirements,
            user_stories,
            design_feedback
        ):
        
        """
                Helper method to generate technical design document in Markdown format
            """
        logger.info("----- Creating Technical Design Document ----")
        prompt = f"""
                Create a comprehensive technical design document for {project_name} in Markdown format.
                
                The document should use proper Markdown syntax with headers (# for main titles, ## for sections, etc.), 
                bullet points, tables, code blocks, and diagrams described in text form where appropriate.
                
                Requirements:
                {self.utility.format_list(requirements)}
            
                User Stories:
                {self.utility.format_user_stories(user_stories)}

                {f"When creating this technical design document, please incorporate the following feedback about the requirements: {design_feedback}" if design_feedback else ""}
                
                The technical design document should include the following sections, each with proper Markdown formatting:
                
                # Technical Design Document: {project_name}

                ## 1. System Architecture
                ## 2. Technology Stack and Justification
                ## 3. Database Schema
                ## 4. API Specifications
                ## 5. Security Considerations
                ## 6. Performance Considerations
                ## 7. Scalability Approach
                ## 8. Deployment Strategy
                ## 9. Third-party Integrations
                ## 10. Development, Testing, and Deployment Environments
                
                For any code examples, use ```language-name to specify the programming language.
                For database schemas, represent tables and relationships using Markdown tables.
                Make sure to maintain proper Markdown formatting throughout the document.
            """
        response = self.llm.invoke(prompt)
        return response.content
    
    def review_design_documents(self, state: SDLCState):
        return state
    def revise_design_documents(self, state: SDLCState):
        pass
    
    def review_design_documents_router(self, state: SDLCState):
        """
            Evaluates design review is required or not.
        """
        return state.get("design_documents_review_status", "approved")