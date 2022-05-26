from __future__ import annotations
from typing import TYPE_CHECKING
from tcod.context import new
from tcod import event
from tcod.tileset import load_tilesheet, CHARMAP_CP437
from data import TILE_SHEET, WINDOW

if TYPE_CHECKING:
    from typing import Any
    from tcod.context import Context
    from geography.world import World


def handle_events(world: World, context: Context) -> None:
    for e in event.wait():
        context.convert_event(e)
        match e:
            case event.Quit():
                raise SystemExit()
            case event.MouseButtonDown():
                print(world.biome[e.tile.y, e.tile.x])


def render_content(*entities: Any, context: Context) -> None:
    console = context.new_console()

    for entity in entities:
        entity.render(console)

    context.present(console, integer_scaling=True)


def set_context() -> Context:
    return new(
        width=WINDOW["WIDTH"],
        height=WINDOW["HEIGHT"],
        sdl_window_flags=WINDOW["FLAGS"],
        tileset=load_tilesheet(TILE_SHEET, 16, 16, CHARMAP_CP437)
    )
