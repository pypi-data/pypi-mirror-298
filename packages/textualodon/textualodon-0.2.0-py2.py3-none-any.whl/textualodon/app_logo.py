from textual.app import ComposeResult
from textual.widgets import Static


class AppLogo(Static):
    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        yield Static("Textualodon - Mastodon in your terminal", id="logo")
