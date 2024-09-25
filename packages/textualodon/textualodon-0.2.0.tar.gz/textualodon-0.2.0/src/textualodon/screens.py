from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

try:
    from .timelines import (
        GlobalTimeline,
        HomeTimeline,
        LocalTimeline,
        TrendingPostsWithTag,
    )
except ImportError:
    from timelines import GlobalTimeline, HomeTimeline, LocalTimeline, TrendingPostsWithTag  # type: ignore[no-redef]


class HomeTimelineScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield HomeTimeline()
        yield Footer()


class LocalTimelineScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield LocalTimeline()
        yield Footer()


class GlobalTimelineScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield GlobalTimeline()
        yield Footer()


class TagPostsScreen(Screen):
    BINDINGS = [
        ("b", "go_back", "Go back"),
    ]

    def __init__(self, tag_name: str):
        super().__init__()
        self.tag_name = tag_name

    def compose(self) -> ComposeResult:
        yield Header()
        yield TrendingPostsWithTag(tag_name=self.tag_name)
        yield Footer()

    def action_go_back(self) -> None:
        self.app.pop_screen()
