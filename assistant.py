from graph.builder import graph


def main():

    while True:

        question = input(
            "\nВопрос: "
        ).strip()

        if question.lower() in (
            "exit",
            "quit"
        ):
            break

        result = graph.invoke(
            {
                "question": question
            }
        )

        print(
            "\nОтвет:\n"
        )

        print(
            result["answer"]
        )


if __name__ == "__main__":
    main()