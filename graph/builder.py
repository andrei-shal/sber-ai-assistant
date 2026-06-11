from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.nodes.nav_assistant import nav_assistant_node
from graph.nodes.nav_build_context import nav_build_context_node
from graph.nodes.nav_navigator import nav_navigator_node
from graph.nodes.nav_search import nav_search_node
from graph.nodes.user_assistant import user_assistant_node
from graph.nodes.user_context_builder import user_context_builder_node
from graph.nodes.user_context_merge import user_context_merge_node
from graph.nodes.user_data_filtrator import user_data_filtrator_node
from graph.nodes.user_load_data import user_load_data_node
from graph.nodes.user_rag_assistant import user_rag_assistant_node
from graph.nodes.user_rag_req_writer import user_rag_req_writer_node
from graph.state import AgentState

from graph.nodes.rag_rewriter import rag_rewriter_node
from graph.nodes.document_search import document_search_node
from graph.nodes.rag_assistant import rag_assistant_node
from graph.nodes.document_context_build import document_context_build_node
from graph.nodes.router import router_node

def build_graph():

    builder = StateGraph(
        AgentState
    )

    # Узлы

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

    builder.add_node(
        "rag_document_search",
        document_search_node
    )

    builder.add_node(
        "rag_document_context_build",
        document_context_build_node
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
        "user_load_data",
        user_load_data_node
    )

    builder.add_node(
        "user_context_builder",
        user_context_builder_node
    )

    builder.add_node(
        "user_rag_req_writer",
        user_rag_req_writer_node
    )

    builder.add_node(
        "user_document_search",
        document_search_node
    )

    builder.add_node(
        "user_document_context_build",
        document_context_build_node
    )

    builder.add_node(
        "user_rag_assistant",
        user_rag_assistant_node
    )

    builder.add_node(
        "user_data_filtrator",
        user_data_filtrator_node
    )

    builder.add_node(
        "user_assistant",
        user_assistant_node
    )

    builder.add_node(
        "user_context_merge",
        user_context_merge_node
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
            "user_data": "rag_rewriter"
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
        "user_load_data",
        "user_context_builder"
    )

    builder.add_edge(
        "user_context_builder",
        "user_rag_req_writer"
    )

    builder.add_edge(
        "user_context_builder",
        "user_data_filtrator"
    )

    builder.add_edge(
        "user_data_filtrator",
        "user_context_merge"
    )

    builder.add_edge(
        "user_rag_req_writer",
        "user_document_search"
    )

    builder.add_edge(
        "user_document_search",
        "user_document_context_build"
    )

    builder.add_edge(
        "user_document_context_build",
        "user_rag_assistant"
    )

    builder.add_edge(
        "user_rag_assistant",
        "user_context_merge"
    )

    builder.add_edge(
        "user_context_merge",
        "user_assistant"
    )

    builder.add_edge(
        "user_assistant",
        END
    )

    # ветка RAG

    builder.add_edge(
        "rag_rewriter",
        "rag_document_search"
    )

    builder.add_edge(
        "rag_document_search",
        "rag_document_context_build"
    )

    builder.add_edge(
        "rag_document_context_build",
        "rag_assistant"
    )

    builder.add_edge(
        "rag_assistant",
        END
    )

    return builder.compile()


graph = build_graph()