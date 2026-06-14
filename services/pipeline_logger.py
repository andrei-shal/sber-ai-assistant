"""
Структурированный логгер пайплайна LangGraph.

Логирует:
- Вход/выход каждого узла с таймингом
- Маршрутизацию (router → ветка)
- Ошибки с трейсбэком
- Финальный ответ
"""

import logging
import sys
import time
import traceback
from functools import wraps

# ─── ANSI colors ───────────────────────────────────────────────

class _Colors:
    GREY = "\033[90m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# ─── Log levels ────────────────────────────────────────────────

LEVEL_ICONS = {
    logging.DEBUG: "🔍",
    logging.INFO: " ℹ",
    logging.WARNING: "⚠",
    logging.ERROR: "✖",
    logging.CRITICAL: "🔥",
}

NODE_ICONS = {
    "router": "🧭",
    "rag_rewriter": "✏️",
    "rag_document_search": "🔎",
    "rag_document_context_build": "📦",
    "rag_assistant": "🤖",
    "nav_navigator": "🧭",
    "nav_search": "🔎",
    "nav_build_context": "📦",
    "nav_assistant": "🤖",
    "control_button": "✅",
    "controller": "🎯",
    "user_data_sql_writer": "💾",
    "user_load_data": "📥",
    "user_context_builder": "🧱",
    "user_rag_req_writer": "✏️",
    "user_document_search": "🔎",
    "user_document_context_build": "📦",
    "user_assistant": "🤖",
    "default": "⚙️",
}

BRANCH_ICONS = {
    "rag": "📚",
    "navigation": "🧭",
    "user_data": "👤",
}


# ─── Logger ─────────────────────────────────────────────────────

class PipelineLogger:
    """Единый логгер для пайплайна LangGraph."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, name="pipeline", log_file=None, level=logging.DEBUG):
        if self._initialized:
            return
        self._initialized = True

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers.clear()

        # Форматтер
        formatter = logging.Formatter(
            "%(asctime)s | %(message)s",
            datefmt="%H:%M:%S",
        )

        # Консоль
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        console.setFormatter(formatter)
        self.logger.addHandler(console)

        # Файл (опционально)
        if log_file:
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setLevel(level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    # ── Публичные методы ──────────────────────────────────────

    def pipeline_start(self, question: str, session_id: str = "-"):
        icon = _Colors.MAGENTA
        self.logger.info(
            f"{_Colors.BOLD}{icon}═╗ ПАЙПЛАЙН СТАРТ{_Colors.RESET}"
        )
        self.logger.info(
            f"{_Colors.GREY}  │ session_id : {session_id}{_Colors.RESET}"
        )
        self.logger.info(
            f"{_Colors.GREY}  │ question   : {question[:200]}{_Colors.RESET}"
        )

    def pipeline_end(self, answer: str, support: str, elapsed: float):
        icon = _Colors.MAGENTA
        emoji = "✅" if support == "False" else "⚠️"
        self.logger.info(
            f"{_Colors.BOLD}{icon}═╝ ПАЙПЛАЙН КОНЕЦ ({elapsed:.2f}s) {emoji}{_Colors.RESET}"
        )
        self.logger.info(
            f"{_Colors.GREY}  │ support : {support}{_Colors.RESET}"
        )
        self.logger.info(
            f"{_Colors.GREY}  │ answer  : {answer[:200]}{_Colors.RESET}"
        )

    def route(self, route: str):
        icon = BRANCH_ICONS.get(route, "➡️")
        colors = {
            "rag": _Colors.CYAN,
            "navigation": _Colors.GREEN,
            "user_data": _Colors.YELLOW,
        }
        c = colors.get(route, _Colors.BLUE)
        self.logger.info(
            f"{c}{icon} │ ВЕТКА: {route.upper()}{_Colors.RESET}"
        )

    def node_enter(self, node_name: str):
        icon = NODE_ICONS.get(node_name, NODE_ICONS["default"])
        self.logger.info(
            f"{_Colors.CYAN}  ┌─ {icon} [{node_name}]{_Colors.RESET}"
        )

    def node_exit(self, node_name: str, elapsed: float):
        self.logger.info(
            f"{_Colors.GREEN}  └─ ✓ [{node_name}] ({elapsed:.2f}s){_Colors.RESET}"
        )

    def node_error(self, node_name: str, exc: Exception):
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        self.logger.error(
            f"{_Colors.RED}  └─ ✖ [{node_name}] {type(exc).__name__}: {exc}{_Colors.RESET}"
        )
        # Сокращённый трейсбэк (последние 10 строк)
        lines = tb.strip().split("\n")
        if len(lines) > 12:
            lines = lines[:2] + ["     ..."] + lines[-8:]
        for line in lines:
            self.logger.debug(f"  {_Colors.GREY}{line}{_Colors.RESET}")

    def info(self, msg: str):
        self.logger.info(f"  {_Colors.BLUE}i  {msg}{_Colors.RESET}")

    def warn(self, msg: str):
        self.logger.warning(f"  {_Colors.YELLOW}⚠  {msg}{_Colors.RESET}")

    def error(self, msg: str):
        self.logger.error(f"  {_Colors.RED}✖  {msg}{_Colors.RESET}")


# ─── Singleton ──────────────────────────────────────────────────

_logger: PipelineLogger | None = None


def get_logger(log_file: str | None = None) -> PipelineLogger:
    global _logger
    if _logger is None:
        _logger = PipelineLogger(log_file=log_file)
    return _logger


# ─── Декоратор для узлов графа ──────────────────────────────────

def logged_node(node_name: str):
    """Декоратор для оборачивания узла LangGraph с логированием."""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(state):
            log = get_logger()
            log.node_enter(node_name)
            t0 = time.perf_counter()
            try:
                result = await func(state)
                elapsed = time.perf_counter() - t0
                log.node_exit(node_name, elapsed)
                return result
            except Exception as e:
                elapsed = time.perf_counter() - t0
                log.node_error(node_name, e)
                raise

        @wraps(func)
        def sync_wrapper(state):
            log = get_logger()
            log.node_enter(node_name)
            t0 = time.perf_counter()
            try:
                result = func(state)
                elapsed = time.perf_counter() - t0
                log.node_exit(node_name, elapsed)
                return result
            except Exception as e:
                elapsed = time.perf_counter() - t0
                log.node_error(node_name, e)
                raise

        if hasattr(func, "__code__") and func.__code__.co_flags & 0x80:
            return async_wrapper
        return sync_wrapper

    return decorator