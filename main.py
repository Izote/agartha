from game.system import set_context, render_content, handle_events


def main() -> None:
    with set_context() as context:
        while True:
            render_content(context)
            handle_events(context)


if __name__ == "__main__":
    main()
