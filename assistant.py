from graph.builder import graph


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

        result = graph.invoke(
            {
                "messages": messages,
                "question": question
            }
        )

        answer = result.get("answer", "")

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