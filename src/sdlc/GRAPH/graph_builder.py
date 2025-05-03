import os
from src.sdlc.STATE.state import SDLCState
from src.sdlc.NODES.requirements_node import ProjectRequirementNode
from src.sdlc.NODES.design_document_node import DesignDocumentNode
from src.sdlc.NODES.markdown_node import MarkdownArtifactsNode
from src.sdlc.NODES.coding_node import CodingNode
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph,START,END
from langchain_core.runnables.graph import MermaidDrawMethod




class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm
        self.memory=MemorySaver()
        self.builder=StateGraph(SDLCState)
        
        
    def build_sdlc_graph(self):
        self.project_requirement_node=ProjectRequirementNode(self.llm)
        self.design_document_node=DesignDocumentNode(self.llm)
        self.markdown_artifact_node=MarkdownArtifactsNode(self.llm)
        self.coding_node=CodingNode(self.llm)
        
        self.builder.add_node("initialize_project",self.project_requirement_node.initialize_project())
        self.builder.add_node("get_user_requirements",self.project_requirement_node.get_user_requirements())
        self.builder.add_node("generate_user_stories",self.project_requirement_node.generate_user_stories())
        self.builder.add_node("revise_user_stories", self.project_requirement_node.revise_user_stories())
        self.builder.add_node("review_user_stories",self.project_requirement_node.review_user_stories())
        self.builder.add_node("create_design_documents",self.design_document_node.create_design_documents())
        self.builder.add_node("review_design_documents",self.design_document_node.review_design_documents())
        self.builder.add_node("revise_design_documents", self.design_document_node.revise_design_documents())
        
        
        # Code generation node
        self.builder.add_node("generate_code",self.coding_node.generate_node())
        self.builder.add_node("code_review",self.coding_node.code_review())
        self.builder.add_node("fix_code",self.coding_node.fix_code())
        
        self.builder.add_node("security_recomendations",self.coding_node.security_review_recomendations())
        self.builder.add_node("security_review",self.coding_node.security_review())
        self.builder.add_node("fix_code_after_security_review",self.coding_node.fix_code_after_security_review())
        
        self.builder.add_node("write_test_cases",self.coding_node.write_test_cases())
        self.builder.add_node("review_test_cases",self.coding_node.review_test_cases())
        self.builder.add_node("revise_test_cases",self.coding_node.revise_test_cases())
        
        self.builder.add_node("qa_testing",self.coding_node.qa_testing())
        self.builder.add_node("qa_review",self.coding_node.qa_review())
        self.builder.add_node("deployment",self.coding_node.deployment())
        self.builder.add_node("download_artifacts",self.markdown_artifact_node.generate_markdown_artifacts())
        
        
        
        # Connecting the edges according to the flow
        self.builder.add_edge(START,"initialize_project")
        self.builder.add_edge("initialize_project","get_user_requirements")
        self.builder.add_edge("get_user_requirements","generate_user_stories")
        self.builder.add_edge("generate_user_stories","review_user_stories")
        self.builder.add_conditional_edge("review_user_stories",self.project_requirement_node.review_user_stories_router(),{
            "approved":"create_design_documents",
            "feedback":"revise_user_stories"
        })
        self.builder.add_edge("revise_user_stories","generate_user_stories")
        self.builder.add_edge("create_design_documents","review_design_documents")
        self.builder.add_conditional_edge("review_design_documents",self.design_documents_node.review_design_documents_router(),
                                          {
                                              "approved":"generate_code",
                                              "feedback":"revise_design_documents"
                                          })
        
        self.builder.add_edge("revise_design_documents","create_design_documents")
        self.builder.add_edge("generate_code","code_review")
        self.builder.add_conditional_edge("code_review",self.coding_node.code_review_router(),
                                          {
                                              "approved":"security_recomendations",
                                              "feedback":"fix_code"
                                          })
        self.builder.add_edge("fix_code","generate_code")
        self.builder.add_edge("security_recomendations","security_review")
        self.add_conditional_edge("security_review",self.coding_node.security_review_router(),
                                  {
                                      "approved":"write_test_cases",
                                      "feedback":"fix_code_after_security_review"
                                  })
        self.add_edge("fix_code_after_security_review","generate_code")
        self.builder.add_edge("write_test_cases","review_test_cases")
        self.builder.add_conditional_edge("review_test_cases",self.coding_node.review_test_cases_router(),
                                          {
                                              "approved":"qa_testing",
                                              "feedback":"revise_test_cases"
                                          })
        self.builder.add_edge("revise_test_cases","write_test_cases")
        self.builder.add_edge("qa_testing","qa_review")
        self.builder.add_conditional_edge("qa_review",self.coding_node.qa_review_router(),
                                          {
                                              "approved":"deployment",
                                              "feedback":"generate_code"
                                          })
        self.builder.add_edge("deployment","download_artifacts")
        self.builder.add_edge("download_artifacts",END)
        
        
        
        
    def setup_graph(self):
        "Set up the graph"
        self.build_sdlc_graph()
        return self.builder.compile(
            interrupt_before=[
                "get_user_requirements",
                "review_user_stories",
                "review_design_documents",
                "code_review",
                "security_review",
                "review_test_cases",
                "qa_review"
            ],checkpointer=self.memory
        )
        
        
    def save_graph(self,graph):
        img=graph.get_graph.draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,

        )
        graph_path="workflow_graph.png"
        with open(graph_path,"wb") as f:
            f.write(img)