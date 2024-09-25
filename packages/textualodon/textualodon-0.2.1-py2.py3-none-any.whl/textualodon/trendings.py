from textual import on  # type: ignore[attr-defined]
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Static,
    TabbedContent,
    TabPane,
)

try:
    from .api import MastoAPI
    from .screens import TagPostsScreen
    from .timelines import TrendingPosts
except ImportError:
    from api import MastoAPI  # type: ignore[no-redef]
    from screens import TagPostsScreen  # type: ignore[no-redef]
    from timelines import TrendingPosts  # type: ignore[no-redef]


class Trendings(Screen):
    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent():
            with TabPane("Posts", id="trending_posts"):
                yield Container(TrendingPosts(), classes="trending_posts")
            with TabPane("Tags", id="trending_tags"):
                yield Container(TrendingTags(), classes="trending_tags")
            with TabPane("Links", id="trending_links"):
                yield Container(TrendingLinks(), classes="trending_links")
        yield Footer()


class Tag(Container):
    def __init__(self, tag_name):
        super().__init__()
        self.tag_name = tag_name

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button(f"#{self.tag_name}", id="show_tag_posts"),
        )

    @on(Button.Pressed, "#show_tag_posts")
    def show_tag_posts(self):
        self.app.push_screen(TagPostsScreen(self.tag_name))


class TrendingTags(Container):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.masto_api = MastoAPI()
        self.trending_tags = self.masto_api.get_trending_tags()

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            Static("Trending Tags", id="title"),
            Container(
                *[Tag(tag_name=tag["name"]) for tag in self.trending_tags],
                classes="trending_tag",
            ),
        )


class Link(Container):
    def __init__(self, url: str, title: str, description: str):
        super().__init__()
        self.url = url
        self.title = title
        self.description = description

    def compose(self) -> ComposeResult:
        yield Center(
            Static(
                f"[@click=\"app.open_link('{self.url}')\"]{self.title}[/]",
                classes="trending_link_title",
            ),
            Static(self.description, classes="trending_link_description"),
            Static(
                "____________________________________________________________",
                classes="trending_link_delimeter",
            ),
            classes="trending_link",
        )

    @on(Button.Pressed, "#show_tag_posts")
    def show_tag_posts(self):
        self.app.push_screen(TagPostsScreen(self.tag_name))


class TrendingLinks(Container):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.masto_api = MastoAPI()
        self.trending_links = self.masto_api.get_trending_links()

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            Static("Trending Links", id="title"),
            Container(
                *[
                    Link(
                        url=link["url"],
                        title=link["title"],
                        description=link["description"],
                    )
                    for link in self.trending_links
                ],
            ),
        )
