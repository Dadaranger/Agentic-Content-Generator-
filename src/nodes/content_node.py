from src.states.contentstate import ContentState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.contentstate import Maincontent

class ContentNode:
    """
    A class to represent a content node in a content generation system.
    """

    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:ContentState):
        """
        create the title for the content.
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are a expert blog writer. Use the {topic} provided to create an engaging blog title.
                   Use Markdown formatting. This title should be creative and SEO friendly.
                   """
            system_message=prompt.format(topic=state["topic"])
            response=self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}
        
    def content_creation(self, state:ContentState):
        if "topic" in state and state["topic"]:
            system_prompt="""You are an expert blog writer. Use Markdown formatting.
            Generate a detailed blog content that reasonate with the audience with detailed breakdown for the {topic} and {title} provided."""
            system_message = system_prompt.format(topic=state["topic"], title=state["blog"]["title"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": state["blog"]["title"], "content": response.content}}
        
    def translation(self, state:ContentState):
        """
        Translate the content to the specified language.
        """
        translation_prompt="""
        Translate the following content into {currrent_language}.
        - Maintain the original tone, style, meaning, context, and formatting.
        - Adapt cultural references and idioms to be apporpriate for speakers of {currrent_language}.

        ORIGINAL CONTENT:
        {article_content}    
        """

        articale_content=state["blog"]["content"]
        message=[
            HumanMessage(translation_prompt.format(currrent_language=state["current_language"], article_content=articale_content))
        ]
        response = self.llm.invoke(message)
        return {"blog": {"title": state["blog"]["title"], "content": response.content}}

    def route(self, state:ContentState):
        return {"current_language": state["current_language"]}


    def route_decision(self, state:ContentState):
        """
        Route the content to the respective translation function.
        """
        language = state["current_language"].lower().strip()
        if language == "traditional chinese":
            return "traditional chinese"
        elif language == "japanese":
            return "japanese"
        else:
            return "END"