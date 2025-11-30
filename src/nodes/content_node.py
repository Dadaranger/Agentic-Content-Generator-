from src.states.contentstate import ContentState


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
            return {"content": {"title": response.content}}
        
    def content_creation(self, state:ContentState):
        if "topic" in state and state["topic"]:
            system_prompt="""You are an expert blog writer. Use Markdown formatting.
            Generate a detailed blog content that reasonate with the audience with detailed breakdown for the {topic} and {title} provided."""
            system_message = system_prompt.format(topic=state["topic"], title=state["content"]["title"])
            response = self.llm.invoke(system_message)
            return {"content": {"title": state["content"]["title"], "content": response.content}}