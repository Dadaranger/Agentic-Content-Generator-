from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.contentstate import ContentState
from src.nodes.content_node import ContentNode


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(ContentState)
        self.content_node_obj = ContentNode(self.llm)

    def build_topic_graph(self):
        """
        Build a graph to generate content on topic.
        """

        ## Nodes
        self.graph.add_node("title_creation", self.content_node_obj.title_creation)
        self.graph.add_node("content_creation", self.content_node_obj.content_creation)

        ## Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_creation")
        self.graph.add_edge("content_creation", END)

        return self.graph
    
    def build_language_graph(self):
        """
        Build a graph for content generation with inputs topic and language.
        """

        ## nodes
        self.graph.add_node("title_creation", self.content_node_obj.title_creation)
        self.graph.add_node("content_creation", self.content_node_obj.content_creation)
        self.graph.add_node("chinese_translation", lambda state: self.content_node_obj.translation({**state, "current_language": "traditional chinese"}))
        self.graph.add_node("japanese_translation", lambda state: self.content_node_obj.translation({**state, "current_language": "japanese"}))
        self.graph.add_node("route", self.content_node_obj.route)

        ## edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_creation")
        self.graph.add_edge("content_creation", "route")
        self.graph.add_conditional_edges("route", 
                                         self.content_node_obj.route_decision,
                                         {"traditional chinese": "chinese_translation",
                                          "japanese": "japanese_translation",
                                          "END": END})
        self.graph.add_edge("chinese_translation", END)
        self.graph.add_edge("japanese_translation", END)
        return self.graph


    
    def setup_graph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()
        if usecase == "language":
            self.build_language_graph()

        return self.graph.compile()

    
## below code is for the langsmith langgraph studio
llm=GroqLLM().get_llm()

## get the graph
graph_builder = GraphBuilder(llm)
graph=graph_builder.build_language_graph().compile()
