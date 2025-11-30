from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.contentstate import ContentState
from src.nodes.content_node import ContentNode


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(ContentState)

    def build_topic_graph(self):
        """
        Build a graph to generate content on topic.
        """

        self.content_node_obj=ContentNode(self.llm)

        ## Nodes
        self.graph.add_node("title_creation", self.content_node_obj.title_creation)
        self.graph.add_node("content_creation", self.content_node_obj.content_creation)

        ## Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_creation")
        self.graph.add_edge("content_creation", END)

        return self.graph
    
    def setup_graph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()
        return self.graph.compile()
    
## below code is for the langsmith langgraph studio
llm=GroqLLM().get_llm()

## get the graph
graph_builder = GraphBuilder(llm)
graph=graph_builder.build_topic_graph().compile()
