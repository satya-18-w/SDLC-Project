import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiLLM:
    def __init__(self,user_controls_input=None,model=None,api_key=None):
        self.user_controls_input=user_controls_input
        self.model=model
        self.api_key=api_key
        
    def get_gemini_model(self):
        try:
            if self.user_controls_input:
                api_key=self.user_controls_input["GEMINI_API_KEY"]
                selected_gemini_model=self.user_controls_input["selected_gemini_model"]
                if api_key == None:
                    print(" Enter your Gemini API Key")
                
                llm=ChatGoogleGenerativeAI(model=selected_gemini_model,api_key=api_key)
                
            else:
                llm=ChatGoogleGenerativeAI(api_key=self.api_key,model=self.model)
                
        except Exception as e:
            raise ValueError(f" Error occured in gemini llm file with exception: {e}")
        
        return llm
        