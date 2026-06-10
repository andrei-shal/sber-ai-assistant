from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.nodes.nav_assistant import nav_assistant_node
from graph.nodes.nav_build_context import nav_build_context_node
from graph.nodes.nav_navigator import nav_navigator_node
from graph.nodes.nav_search import nav_search_node
from graph.nodes.user_data import user_data_node
from graph.state import AgentState

from graph.nodes.rag_rewriter import rag_rewriter_node
from graph.nodes.document_search import document_search_node
from graph.nodes.rag_assistant import rag_assistant_node
from graph.nodes.document_context_build import context_context_build_node
from graph.nodes.router import router_node

def build_graph():

    builder = StateGraph(
        AgentState
    )

    # Узлы

    # Общие служебные узлы

    builder.add_node(
        "document_search",
        document_search_node
    )

    builder.add_node(
        "context_context_build",
        context_context_build_node
    )

    builder.add_node(
        "router",
        router_node
    )

    # Узлы RAG

    builder.add_node(
        "rag_rewriter",
        rag_rewriter_node
    )

    builder.add_node(
        "rag_assistant",
        rag_assistant_node
    )

    # Узлы навигации

    builder.add_node(
        "nav_navigator",
        nav_navigator_node
    )

    builder.add_node(
        "nav_search",
        nav_search_node
    )

    builder.add_node(
        "nav_build_context",
        nav_build_context_node
    )

    builder.add_node(
        "nav_assistant",
        nav_assistant_node
    )

    # Узлы работы с данными пользователя

    builder.add_node(
        "user_data",
        user_data_node
    )

    # Построение графа

    builder.add_edge(
        START,
        "router"
    )

    builder.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "rag": "rag_rewriter",
            "navigation": "nav_navigator",
            "user_data": "user_data"
        }
    )

    # ветка навигации

    builder.add_edge(
        "nav_navigator",
        "nav_search"
    )

    builder.add_edge(
        "nav_search",
        "nav_build_context"
    )

    builder.add_edge(
        "nav_build_context",
        "nav_assistant"
    )

    builder.add_edge(
        "nav_assistant",
        END
    )

    # ветка работы с данными пользователя

    builder.add_edge(
        "user_data",
        END
    )

    # ветка RAG

    builder.add_edge(
        "rag_rewriter",
        "document_search"
    )

    builder.add_edge(
        "document_search",
        "context_context_build"
    )

    builder.add_edge(
        "context_context_build",
        "rag_assistant"
    )

    builder.add_edge(
        "rag_assistant",
        END
    )

    return builder.compile()


graph = build_graph()