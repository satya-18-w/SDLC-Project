from src.sdlc.STATE.state import SDLCState,UserStoryList,UserStory
from src.sdlc.utils.Utility import Utility
from loguru import logger



class CodingNode:
    """
    Graph Node for the coding
    """
    
    def __init__(self,llm):
        self.llm=llm
        self.utility=Utility()
        
        
    def generate_code(self,state: SDLCState):
        """
        Generate the code for the given SDLC state as multiple python files
        """
        logger.info("-------Generate Code--------")
        
        requirements=state.get("requirements","")
        user_stories=state.get("user_stories","")
        code_feedback=state.get("code_review_feedback","")
        security_feedback=state.get("security_recomendations","") if "security_recomendations" in state else ""
        
        prompt=f"""
        Generate a complete python project organized as multiple code files.
        Based on the following SDLC State , generate only the python code files with their complete implementations.
        Do not add any explanations , requirements text or design document details in the output-only code files with proper names and code content.
        
        SDLC State:
        -----------------
        Project Name: {state["project_name"]}
        
        Requirements:
        {self.utility.format_list(state["requirements"])}
        
        User Stoiries:
        {self.utility.format_user_stories(user_stories)}
        
        Functional Design Document:
        {state["design_documents"]["functional"]}
        
        Technical Design Documents:
        {state["design_documents"]["technical"]}
        
        
        {"Note: Incorporate the following code review feedback: " + code_feedback if code_feedback else ""}
        {"Note: Apply the following security recommendations: " + security_feedback if security_feedback else ""}
        
        Instructions:
        - Structure the output as multiple code files (for example, "main.py", "module1.py", etc.), each separated clearly.
        - Each file should contain only the code necessary for a modular, fully-functional project based on the input state.
        - Do not output any additional text, explanations, or commentary outside the code files.
        - Ensure the code follows Python best practices, is syntactically correct, and is ready for development.
        
        
        """
        response=self.llm.invoke(prompt)
        code_review_comments=self.get_code_review_comments(code=response.content)
        
        return {
            "code_generated":response.content,
            "code_review_comments": code_review_comments
        }
        
        # This code review comments will be used while generating test cases
    def get_code_review_comments(self,code: str):
        """
        Generate code review comments for the provided code
        """
        logger.info("------------Generating code review comments------------")
        prompt="""
        You are a coding expert in python programing language .please review the following code and provide detailed feedback:
        CODE: {code}
        ------
        focus on:
        1. Code Quality and best Practises
        2. Potential bugs and edge cases
        3. Performance Consideration
        4. Security Concerns
        
        End your review with an explicit APPROVED or NEEDS_FEEDBACK status."""
            
            
        response=self.llm.invoke(prompt)
        review_comment=response.content
        return review_comment
    
    
    def code_review(self,state: SDLCState):
        return state
    
    def fix_code(self,state: SDLCState):
        pass
    
    def code_review_router(self,state: SDLCState):
        """
        Evaluate code review is required or not
        """
        return state.get("code_review_status","approved")
    
    
    def security_review_recomendations(self,state: SDLCState):
        """
        Perform security review of the code generated
        """
        logger.info("------------Performing security review------------")
        code_generated=state["code_generated"]
        
        
        # Create a prompt for the LLM to review the code for security concerns
        prompt = f"""
            You are a security expert. Please review the following Python code for potential security vulnerabilities:
            ```
            {code_generated}
            ```
            Focus on:
            1. Identifying potential security risks (e.g., SQL injection, XSS, insecure data handling).
            2. Providing recommendations to mitigate these risks.
            3. Highlighting any best practices that are missing.

            End your review with an explicit APPROVED or NEEDS_FEEDBACK status.
        """
        response=self.llm.invoke(prompt)
        return {"security_recomendations":response.content}
    def security_review(self, state: SDLCState):
        return state
    
    def fix_code_after_security_review(self, state: SDLCState):
        pass
    
    def security_review_router(self, state: SDLCState):
        """
            Security Code review is required or not.
        """
        return state.get("security_review_status", "approved")  # default to "approved" if not present
    
    ## ---- Test Cases ----- ##
    def write_test_cases(self, state: SDLCState):
        """
            Generates the test cases based on the generated code and code review comments
        """
        logger.info("----- Generating Test Cases ----")
    
        # Get the generated code and code review comments from the state
        code_generated = state.get('code_generated', '')
        code_review_comments = state.get('code_review_comments', '')

         # Create a prompt for the LLM to generate test cases
        prompt = f"""
            You are a software testing expert. Based on the following Python code and its review comments, generate comprehensive test cases:
            
            ### Code:
            ```
                {code_generated}
                ```

                ### Code Review Comments:
                {code_review_comments}

                Focus on:
                1. Covering all edge cases and boundary conditions.
                2. Ensuring functional correctness of the code.
                3. Including both positive and negative test cases.
                4. Writing test cases in Python's `unittest` framework format.

                Provide the test cases in Python code format, ready to be executed.
        """

        response = self.llm.invoke(prompt)
        return {"test_cases": response.content}
    
    def review_test_cases(self, state: SDLCState):
        return state
    
    def revise_test_cases(self, state: SDLCState):
        pass
    
    def review_test_cases_router(self, state: SDLCState):
        """
            Evaluates Test Cases review is required or not.
        """
        return state.get("test_case_review_status", "approved")  # default to "approved" if not present
    
    ## ---- QA Testing ----- ##
    def qa_testing(self, state: SDLCState):
        """
            Performs QA testing based on the generated code and test cases
        """
        logger.info("----- Performing QA Testing ----")
        # Get the generated code and test cases from the state
        code_generated = state.get('code_generated', '')
        test_cases = state.get('test_cases', '')

        # Create a prompt for the LLM to simulate running the test cases
        prompt = f"""
            You are a QA testing expert. Based on the following Python code and test cases, simulate running the test cases and provide feedback:
            
            ### Code:
            ```
            {code_generated}
            ```

            ### Test Cases:
            ```
            {test_cases}
            ```

            Focus on:
            1. Identifying which test cases pass and which fail.
            2. Providing detailed feedback for any failed test cases, including the reason for failure.
            3. Suggesting improvements to the code or test cases if necessary.

            Provide the results in the following format:
            - Test Case ID: [ID]
            Status: [Pass/Fail]
            Feedback: [Detailed feedback if failed]
        """

        # Invoke the LLM to simulate QA testing
        response = self.llm.invoke(prompt)
        qa_testing_comments = response.content
        return {"qa_testing_comments":qa_testing_comments}\
            
    def qa_review(self, state: SDLCState):
        pass
    
    
    def deployment(self,state: SDLCState):
        """
        Performs the deployment
        """
        logger.info("-------Generatin  the Deplyment simulation-------")
        
        
        code_generated=state.get("code_generated")
        
        # writing a prompt for llm to simulate deployment
        prompt=f"""
        You are an devops expert .Based of the following python code ,simulate the deployment process and provide feedback:
        CODE: {code_generated}
        
        Focus on:
        1. Identifying potential deployment issues(eg. missing dependensies,configuration errors)
        2.Providing recomendations to resolve the issues.
        3. Confirming weather the deployment is sucessful or needs further action.
        
        Provide the results in following format:
        - Deployment Status: [Success/Failure]
        - Feedback: [Detailed feedback on the deployment process]
        """
        
        response=self.llm.invoke(prompt)
        deployment_feedback=response.content
        if "SUCCESS" in deployment_feedback.upper():
            deployment_status="success"
        else:
            deployment_status="failed"
            
            
        return {
            "deployment_status":deployment_status,
            "deployment_feedback":deployment_feedback
        }