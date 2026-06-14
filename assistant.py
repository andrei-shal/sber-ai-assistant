from graph.builder import graph
from services.pipeline_logger import get_logger
import time

log = get_logger()


def main():

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

        result = graph.invoke(
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
        print(result.get("button", ""))


if __name__ == "__main__":
    main()