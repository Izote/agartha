from __future__ import annotations
from typing import TYPE_CHECKING
from tcod.context import new
from tcod import event
from tcod.tileset import load_tilesheet, CHARMAP_CP437
from data import TILE_SHEET, WINDOW

if TYPE_CHECKING:
    from tcod.context import Context


def handle_events(context: Context) -> None:
    for e in event.wait():
        context.convert_event(e)
        match e:
            case event.Quit():
                raise SystemExit()


def render_content(context: Context) -> None:
    console = context.new_console()
    console.print(0, 0, "This is what text in your game will end up looking like. - MIKE")
    context.present(console, integer_scaling=True)


def set_context() -> Context:
    return new(
        width=WINDOW["WIDTH"],
        height=WINDOW["HEIGHT"],
        sdl_window_flags=WINDOW["FLAGS"],
        tileset=load_tilesheet(TILE_SHEET, 16, 16, CHARMAP_CP437)
    )
