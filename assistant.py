import asyncio
import time

from graph.builder import graph
from services.pipeline_logger import get_logger

log = get_logger()


async def main():

    messages = []

    while True:

        question = input(
            "\nВопрос: "
        ).strip()

        if question.lower() in (
            "exit",
            "quit"
        ):
            break

        if not question:
            continue

        t_start = time.perf_counter()
        log.pipeline_start(question, "console")

        result = await graph.ainvoke(
            {
                "messages": messages,
                "question": question
            }
        )

        answer = result.get("answer", "")
        elapsed = time.perf_counter() - t_start

        log.pipeline_end(answer, result.get("support", "True"), elapsed)

        messages.append({
            "role": "user",
            "content": question
        })
        messages.append({
            "role": "assistant",
            "content": answer
        })
        messages = messages[-20:]

        print(
            "\nОтвет:\n"
        )

        print(answer)
        print(result.get("button") or "")


if __name__ == "__main__":
    asyncio.run(main())