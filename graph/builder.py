from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.nodes.context import context_builder_node
from graph.state import AgentState

from graph.nodes.rewrite import rewrite_node
from graph.nodes.search import search_node
from graph.nodes.answer import answer_node


def build_graph():

    builder = StateGraph(
        AgentState
    )

    builder.add_node(
        "rewrite",
        rewrite_node
    )

    builder.add_node(
        "search",
        search_node
    )

    builder.add_node(
        "context_builder",
        context_builder_node
    )

    builder.add_node(
        "answer",
        answer_node
    )

    builder.add_edge(
        START,
        "rewrite"
    )

    builder.add_edge(
        "rewrite",
        "search"
    )

    builder.add_edge(
        "search",
        "context_builder"
    )

    builder.add_edge(
        "context_builder",
        "answer"
    )

    builder.add_edge(
        "answer",
        END
    )

    return builder.compile()


graph = build_graph()