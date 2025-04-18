import Streamlit as st
from src.sdlc.LLMS.groq_llm import GroqLLM
from src.sdlc.LLMS.gemini_llm import GeminiLLM
from src.sdlc.ui.uiconfigfile import Config
from src.sdlc.utils.constants import Constants
from src.sdlc.STATE.state import UserStoryList
import os
from dotenv import load_dotenv

def initialize_session():
    st.session_state.stage=Constants.PROJECT_INITILIZATION
    st.session_state.project_name=""
    st.session_state.requirements=""
    st.session_state.task_id=""
    st.session_state.state={}
    
    
def load_sidebar():
    user_controls={}
    config=Config()
    with st.sidebar:
        # Get LLM options
        llm_options=config.get_llm_options()
        
        ## LLM Selection
        
        user_controls["selected_llm"]=st.selectbox("Select Your LLM",llm_options)
    
        
        if user_controls["selected_llm"] == "Groq":
            groq_model=config.get_groq_model_options()
            user_controls["selected_groq_model"]=st.selectbox("Select Groq Model",groq_model)
            load_dotenv()
            groq_api_key=st.text_input("API_KEY",type="password",value=os.getenv("GROQ_API_KEY"))
            user_controls["GROQ_API_KEY"]=groq_api_key
            os.environ["GROQ_API_KEY"]=groq_api_key
            if not user_controls["GROQ_API_KEY"]:
                st.warning("⚠️ Please enter your GROQ API key to proceed. Don't have? refer : https://console.groq.com/keys ")
                
                
                
        if user_controls["selected_llm"] == 'Gemini':
                
            # Model selection
            model_options = config.get_gemini_model_options()
            user_controls["selected_gemini_model"] = st.selectbox("Select Model", model_options)
            # API key input
            os.environ["GEMINI_API_KEY"] = user_controls["GEMINI_API_KEY"] = st.session_state["GEMINI_API_KEY"] = st.text_input("API Key",
                                                                                                    type="password",
                                                                                                    value=os.getenv("GEMINI_API_KEY", "")) 
            # Validate API key
            if not user_controls["GEMINI_API_KEY"]:
                st.warning("⚠️ Please enter your GEMINI API key to proceed. Don't have? refer : https://ai.google.dev/gemini-api/docs/api-key ")
            
            
        if st.button("Reset Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
                
                
            initialize_session()
            st.rerun()
            
            
            
        st.subheader("Wrokflow Overview")
        st.image("workflow_graph.png")
        
    return user_controls



def load_streamlit_ui():
    config=Config()
    st.set_page_config(page_title=config.get_page_title(),layout="wide")
    st.header(config.get_page_title())
    st.subheader("Plan Your SDLC Journey With AI Agents",divider="rainbow",anchor=False)
    user_controls=load_sidebar()
    return user_controls


# Entry Point
def load_app():
    " Entry point to the Streamlit web app"
    config=Config()
    if "stage" not in st.session_state:
        initialize_session()
        
    user_input=load_streamlit_ui()
    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    try:
        
        selectedLLM=user_input.get("selected_llm")
        
        if selectedLLM == "Gemini":
            obj_llm_config=GeminiLLM(user_controls_input=user_input)
            model=obj_llm_config.get_gemini_model()
            
        elif selectedLLM == "Groq":
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_groq_model()
            
            
        if not model:
            st.error("Error: LLM model could not be initialized.")
            return
        
        
        ## Graph Builder
        graph_builder=GraphBuilder(model)
        try:
            graph=graph_builder.setup_graph()
            graph_executor=GraphExecutor(graph)
            
        except Exception as e:
            st.error(f"Error: Graph setup Failed {e}")
            return
        
        
        tabs=st.tabs(["Project Requirement","User Stories","Design Document","Code Generation","Test Cases","QA Testing","Deployment","Download Artifacts"])
        
        
        # -------------------------------------------------tab-1----------------------------------------
        # Project Requirement
        with tabs[0]:
            st.header("Project Requirement")
            project_name=st.text_input("Enter your Project Name :",value=st.session_state.get["project_name"])
            st.session_state["project_name"]=project_name
            
            if st.session_state.stage==Constants.PROJECT_INITIALIOZATION:
                if st.button("🚀 Let's Start"):
                    if not project_name:
                        st.error("Error: Please Enter your Project Name")
                        st.stop()
                        
                    graph_response=graph_executor.start_workflow(project_name)
                    st.session_state.task_id=graph_response["task_id"]
                    st.session_state.state=graph_response["state"]
                    st.session_state.stage = Constants.REQUIREMENT_COLLECTION
                    st.rerun()
                    
                    
            # If stage has progressed belond initialization , show requirements input and details
            if st.session_state.stage in [Constants.REQUIREMENT_COLLECTION,Constants.GENERATE_USER_STORIES]:
                requirements_input=st.text_area(
                    "Enter the requirements. Write each requirement in a new line",
                    value="\n".join(st.session_state.get("requirements",[]))
                )
                if st.button("Submit Requirements"):
                    requirements=[req.strip() for req in requirements_input.split("\n") if req.strip()]
                    st.session_state.requirements=requirements
                    if not requirements:
                        st.error("Error: Please Enter the Requirements")
                        
                        
                    else:
                        st.success("Project details saved Successfully")
                        st.subheader("Project Details:")
                        st.write(f"Project Name: {project_name}")
                        st.subheader("Project Requirements:")
                        for req in requirements:
                            st.write(req)
                            
                            
                        graph_response=graph_executor.generate_stories(st.session_state.task_id,requirements)
                        st.session_state.stage=Constants.GENERATE_USER_STORIES
                        st.session_state.state=graph_response["state"]
                        st.rerun()
                        
                        