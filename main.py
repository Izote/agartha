from geography.world import World
from game.system import set_context, render_content, handle_events


def main() -> None:
    world = World([1, 2, 3])

    with set_context() as context:
        while True:
            render_content(world, context=context)
            handle_events(context=context)


if __name__ == "__main__":
    main()
