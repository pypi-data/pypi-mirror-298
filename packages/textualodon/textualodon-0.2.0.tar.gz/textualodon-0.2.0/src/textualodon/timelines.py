from typing import Dict, List

from textual import on  # type: ignore[attr-defined]
from textual.app import ComposeResult
from textual.containers import Container, ScrollableContainer, Center
from textual.widgets import Button, Static

try:
    from .api import MastoAPI
    from .posts import Post
except ImportError:
    from api import MastoAPI  # type: ignore[no-redef]
    from posts import Post  # type: ignore[no-redef]


class FeedBase(Container):
    def __init__(self) -> None:
        super().__init__()
        self.masto_api = MastoAPI()
        self.posts: List[Dict[str, str]] = []
        self.posts_widgets: List[Post] = []

    CSS_PATH = "style.css"

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            Static(self.title, id="title"),
            Center(*self.posts_widgets, classes="posts"),
            Button("Load more", classes="buttons", id="more_button"),
            classes="feed",
        )

    def prepare_posts_widgets(self, posts: List[Dict[str, str]]) -> List[ComposeResult]:
        self.last_post_id = posts[-1]["id"]
        posts_widgets = []
        for post in posts:
            reblogger = None
            reblogger_handle = None
            reply_post_url = None
            reply_to_post_author = None
            original_post_id = None
            is_with_spoiler = post["sensitive"]
            spoiler_text = post["spoiler_text"]
            poll = post["poll"]
            if post["reblog"] is not None:
                author = post["reblog"]["account"]["username"]  # type: ignore[index]
                author_url = post["reblog"]["account"]["url"]  # type: ignore[index]
                author_handle = f"{author} ({author_url})"
                reblogger = post["account"]["username"]  # type: ignore[index]
                reblogger_url = post["account"]["url"]  # type: ignore[index]
                reblogger_handle = f"{reblogger} ({reblogger_url})"
                content = post["reblog"]["content"]  # type: ignore[index]
                media_attachments = post["reblog"]["media_attachments"]  # type: ignore[arg-type, index]
                original_post_id = post["reblog"]["id"]  # type: ignore[index]
            else:
                author = post["account"]["username"]
                author_url = post["account"]["url"]
                author_handle = f"{author} ({author_url})"
                content = post["content"]
                media_attachments = post["media_attachments"]
            if (reply_to_id := post["in_reply_to_id"]) is not None and (
                reply_to_account_id := post["in_reply_to_account_id"]
            ) is not None:
                _, reply_to_user = self.masto_api.get_account_by_id(reply_to_account_id)
                _, reply_to_post = self.masto_api.get_post_by_id(reply_to_id)
                reply_post_url = reply_to_post["url"]
                reply_to_post_author = f"{reply_to_user['acct']} ({reply_to_user['url']})"  # type: ignore[index]
            posts_widgets.append(
                Post(
                    author=author_handle,
                    content=content,
                    favourites_count=post["favourites_count"],  # type:ignore[arg-type]
                    reblogs_count=post["reblogs_count"],  # type:ignore[arg-type]
                    replies_count=post["replies_count"],  # type:ignore[arg-type]
                    url=post["url"],
                    reblogger=reblogger_handle,
                    post_id=post["id"],
                    original_post_id=original_post_id,
                    favourited=post["favourited"],  # type:ignore[arg-type]
                    boosted=post["reblogged"],  # type:ignore[arg-type]
                    bookmarked=post["bookmarked"],  # type:ignore[arg-type]
                    visibility=post["visibility"],
                    reply_to_url=reply_post_url,
                    reply_to_author=reply_to_post_author,
                    media_attachments=media_attachments,  # type:ignore[arg-type]
                    is_with_spoiler=is_with_spoiler,  # type:ignore[arg-type]
                    spoiler_text=spoiler_text,
                    poll=poll,  # type:ignore[arg-type]
                )
            )
        return posts_widgets


class HomeTimeline(FeedBase):
    def __init__(self) -> None:
        super().__init__()
        self.title = "Home timeline"
        self.posts = self.masto_api.get_home_timeline()
        self.posts_widgets = self.prepare_posts_widgets(posts=self.posts)

    @on(Button.Pressed, "#more_button")
    def load_more_posts(self) -> None:
        posts = self.masto_api.get_home_timeline(load_from=self.last_post_id)
        posts_widgets = self.prepare_posts_widgets(posts=posts)
        self.query_one(".posts").mount(*posts_widgets)


class LocalTimeline(FeedBase):
    def __init__(self) -> None:
        super().__init__()
        self.title = "Local timeline"
        self.posts = self.masto_api.get_local_timeline()
        self.posts_widgets = self.prepare_posts_widgets(posts=self.posts)

    @on(Button.Pressed, "#more_button")
    def load_more_posts(self) -> None:
        posts = self.masto_api.get_local_timeline(load_from=self.last_post_id)
        posts_widgets = self.prepare_posts_widgets(posts=posts)
        self.query_one(".posts").mount(*posts_widgets)


class GlobalTimeline(FeedBase):
    def __init__(self) -> None:
        super().__init__()
        self.title = "Global timeline"
        self.posts = self.masto_api.get_global_timeline()
        self.posts_widgets = self.prepare_posts_widgets(posts=self.posts)

    @on(Button.Pressed, "#more_button")
    def load_more_posts(self) -> None:
        posts = self.masto_api.get_global_timeline(load_from=self.last_post_id)
        posts_widgets = self.prepare_posts_widgets(posts=posts)
        self.query_one(".posts").mount(*posts_widgets)


class TrendingPosts(FeedBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.title = "Trending posts"
        self.posts = self.masto_api.get_trending_posts()
        self.posts_widgets = self.prepare_posts_widgets(posts=self.posts)
        self.number_of_posts = len(self.posts)

    @on(Button.Pressed, "#more_button")
    def load_more_posts(self) -> None:
        posts = self.masto_api.get_trending_posts(offset=self.number_of_posts)
        self.number_of_posts += len(posts)
        posts_widgets = self.prepare_posts_widgets(posts=posts)
        self.query_one(".posts").mount(*posts_widgets)


class TrendingPostsWithTag(FeedBase):
    def __init__(self, tag_name: str, *args, **kwargs) -> None:
        super().__init__()
        self.tag_name = tag_name
        self.title = f"Trending posts with tag {self.tag_name}"
        self.posts = self.masto_api.get_posts_with_tag(tag_name=self.tag_name)
        self.posts_widgets = self.prepare_posts_widgets(posts=self.posts)
        self.number_of_posts = len(self.posts)

    @on(Button.Pressed, "#more_button")
    def load_more_posts(self) -> None:
        posts = self.masto_api.get_posts_with_tag(
            tag_name=self.tag_name, load_from=self.number_of_posts
        )
        self.number_of_posts += len(posts)
        posts_widgets = self.prepare_posts_widgets(posts=posts)
        self.query_one(".posts").mount(*posts_widgets)
