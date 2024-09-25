from __future__ import annotations

from typing import Any, Union

from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Center
from textual.widgets import Header, Footer
from textual.screen import Screen

try:
    from .posts import Post
    from .api import MastoAPI
except ImportError:
    from posts import Post  # type: ignore[no-redef]
    from api import MastoAPI  # type: ignore[no-redef]


class PostDetails(Screen):
    BINDINGS = [
        ("b", "go_back", "Go back"),
    ]
    CSS_PATH = "style.css"

    def __init__(self, post_id) -> None:
        super().__init__()
        self.post_id = post_id
        self.masto_api = MastoAPI()
        _, self.post_context = self.masto_api.get_post_context(post_id=self.post_id)
        _, self.post = self.masto_api.get_post_by_id(post_id=self.post_id)
        post_widget = self.prepare_post_widgets(posts=[self.post], main_post=True)
        self.post_ancestors = self.post_context["ancestors"]  # type: ignore[arg-type]
        post_ancestors_widgets = self.prepare_post_widgets(self.post_ancestors)  # type: ignore[arg-type]
        self.post_descendants = self.post_context["descendants"]  # type: ignore[arg-type]
        post_descendants_widgets = self.prepare_post_widgets(self.post_descendants)  # type: ignore[arg-type]
        self.posts_widgets = (
            post_ancestors_widgets + post_widget + post_descendants_widgets
        )

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            Header(),
            Center(*self.posts_widgets, classes="posts"),
            Footer(),
        )

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def prepare_post_widgets(
        self, posts: list[dict[str, Union[str, Any, None]]], main_post: bool = False
    ) -> ComposeResult:
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
                author = post["account"]["username"]  # type: ignore[index]
                author_url = post["account"]["url"]  # type: ignore[index]
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
                    url=post["url"],  # type:ignore[arg-type]
                    reblogger=reblogger_handle,  # type:ignore[arg-type]
                    post_id=post["id"],  # type:ignore[arg-type]
                    original_post_id=original_post_id,
                    favourited=post["favourited"],  # type:ignore[arg-type]
                    boosted=post["reblogged"],  # type:ignore[arg-type]
                    bookmarked=post["bookmarked"],  # type:ignore[arg-type]
                    visibility=post["visibility"],  # type:ignore[arg-type]
                    reply_to_url=reply_post_url,
                    reply_to_author=reply_to_post_author,
                    media_attachments=media_attachments,  # type:ignore[arg-type]
                    is_with_spoiler=is_with_spoiler,  # type:ignore[arg-type]
                    spoiler_text=spoiler_text,
                    is_details_open=main_post,
                    poll=poll,  # type:ignore[arg-type]
                )
            )
        return posts_widgets
