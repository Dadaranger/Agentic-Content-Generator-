from typing import TypedDict
from pydantic import BaseModel, Field 

class Maincontent(BaseModel):
    title: str=Field(description="The title of the content to be generated.")
    content: str=Field(description="The main content of the content to be generated.")
    # audience: str=Field(description="The target audience for the content.")

class ContentState(TypedDict):
    topic: str 
    content: Maincontent
    current_language: str