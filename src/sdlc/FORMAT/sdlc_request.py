from pydantic import BaseModel,Field
from typing import Optional

class SDLCRequest(BaseModel):
    project_name: str =Field(...,example="Ecommerce platform",description="Name of the project")
    requirements: Optional[list[str]] = Field(None,example=["User can browse the product",
                                                            "User can be able to purchase or add to cart the product",
                                                            "user should be able to do the payment",
                                                            "User can place the order",
                                                            "user should be able to see their order history"],
                                              description="List of requirements of the project")
    task_id: Optional[str] = Field(None,example="SDLC-SESSION-237897fgh",description="task id of the workflow")
    next_node: Optional[str] = Field(None,example="review_user_stroies",description="The next node to be executed in the wirkflow.pass the input the you got from the previous nodes output")
    
    status: Optional[str] = Field(None,example="approved or feedback",description="The status of the review")
    feedback: Optional[str] = Field(None,example="the user stories need to be more specific to the project",description="the feedback for the review")