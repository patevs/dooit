from typing import TYPE_CHECKING
from textual.app import events
from textual.screen import Screen

if TYPE_CHECKING:
    from ..api import DooitAPI
    from ..tui import Dooit


class BaseScreen(Screen):
    """
    Base screen with function to resolve `Key` event to str
    """

    SPACE_CHARACTERS = (
        "\u0020\u00a0\u1680\u202f\u205f\u3000"
        "\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u200b"
    )

    @property
    def app(self) -> "Dooit":
        from ..tui import Dooit

        app = super().app
        if not isinstance(app, Dooit):
            raise ValueError(f"Expected Dooit, got {type(app)}")

        return app

    @property
    def api(self) -> "DooitAPI":
        return self.app.api

    def resolve_key(self, event: events.Key) -> str:
        if not event.character:
            return event.key

        if event.is_printable or event.character in self.SPACE_CHARACTERS:
            return event.character

        return event.key

    async def handle_key(self, event: events.Key) -> bool:
        key = self.resolve_key(event)
        self.api.handle_key(key)
        return True
