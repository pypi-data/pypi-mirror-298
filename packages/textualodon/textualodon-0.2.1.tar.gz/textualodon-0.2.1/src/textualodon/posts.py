from __future__ import annotations

import re
from typing import Any, Optional, Union

from bs4 import BeautifulSoup
from textual import on  # type: ignore[attr-defined]
from textual.app import ComposeResult
from textual.containers import Center, Horizontal
from textual.widgets import Static, Button

try:
    from .api import MastoAPI
    from .constants import visibility_emojis
    from .poll import Poll
except ImportError:
    from api import MastoAPI  # type: ignore[no-redef]
    from constants import visibility_emojis  # type: ignore[no-redef]
    from poll import Poll  # type: ignore[no-redef]


class Post(Static):
    CSS_PATH = "style.css"

    def __init__(
        self,
        author: str,
        content: str,
        favourites_count: int,
        reblogs_count: int,
        replies_count: int,
        url: str,
        reblogger: str,
        post_id: str,
        favourited: bool,
        bookmarked: bool,
        boosted: bool,
        visibility: str,
        reply_to_url: Optional[str] = None,
        reply_to_author: Optional[str] = None,
        media_attachments: Optional[list[dict[str, Union[str, Any, None]]]] = None,
        is_with_spoiler: bool = False,
        spoiler_text: Optional[str] = None,
        original_post_id: Optional[str] = None,
        is_details_open: bool = False,
        poll: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__()
        self.author = author
        self.content = self.__parse_content(content)
        self.favourites_count = favourites_count
        self.reblogs_count = reblogs_count
        self.replies_count = replies_count
        self.url = url
        self.reblogger = reblogger
        self.post_id = post_id
        self.masto_api = MastoAPI()
        self.favourited = favourited
        self.bookmarked = bookmarked
        self.visibility = visibility
        self.boosted = boosted
        self.reply_to_url = reply_to_url
        self.reply_to_author = reply_to_author
        self.media_attachments = media_attachments
        if self.media_attachments is None:
            self.media_attachments = []
        self.is_with_spoiler = is_with_spoiler
        self.spoiler_text = spoiler_text
        self.original_post_id = original_post_id
        self.is_details_open = is_details_open
        self.poll = poll

    @staticmethod
    def __parse_content(html_text) -> list[str]:
        soup = BeautifulSoup(html_text, "html.parser")

        def __parse_tags(soup) -> BeautifulSoup:
            a_tags = soup.find_all("a", {"class": "hashtag"})
            for a_tag in a_tags:
                href_content = a_tag.get("href", "")
                hashtag = re.sub("https://.*/tags/", " #", href_content)
                a_tag.replace_with(f" {hashtag}")
            return soup

        def __parse_links(soup) -> BeautifulSoup:
            a_hrefs = soup.find_all("a")
            for a_href in a_hrefs:
                href_content = a_href.get("href", "")
                a_href.replace_with(f"[u]{href_content}[/]")
            return soup

        def __parse_p(soup) -> list[str]:
            p_tags = soup.find_all("p")
            return [p_tag.get_text() for p_tag in p_tags]

        soup = __parse_tags(soup)
        soup = __parse_links(soup)
        soup = __parse_p(soup)

        return [str(s) for s in soup]

    def compose(self) -> ComposeResult:
        if len(self.content) > 1:
            content = [Static(line, classes="post_content") for line in self.content]
        else:
            try:
                content = [Static(self.content[0], classes="post_content")]
            except IndexError:
                content = []
        if self.reblogger:
            author = Horizontal(
                Static(
                    f"Reblogged by {self.reblogger}, Author: {self.author}",
                    classes="author",
                ),
            )
        elif self.reply_to_url and self.reply_to_author:
            author = Center(
                Static(
                    f"Author: {self.author}, Replied to {self.reply_to_author}",
                    classes="author",
                ),
                Static(f"Replied to url: {self.reply_to_url}", classes="author"),
            )
        else:
            author = Static(f"Author: {self.author}", classes="author")
        favourite_button_class = "favourited" if self.favourited else ""
        boost_button_class = "boosted" if self.boosted else ""
        bookmark_button_class = "bookmarked" if self.bookmarked else ""
        if self.reblogger:
            post_class = "reblog"
        elif self.reply_to_url and self.reply_to_author:
            post_class = "comment"
        else:
            post_class = "post"
        spoiler = Center(
            Static(f"CW: {self.spoiler_text}", classes="spoiler_text"),
            Button("Show more", classes="spoiler_button", id="hide_spoiler"),
            classes="spoiler",
            id="spoiler",
        )
        if not self.is_with_spoiler:
            spoiler.styles.display = "none"
        comments_button = Button(
            f"Comments {self.replies_count}", classes="button", id="details"
        )
        if self.is_details_open:
            comments_button.styles.display = "none"
        poll_widget = []
        if self.poll is not None:
            poll_widget.append(
                Poll(
                    poll_id=self.poll["id"],
                    expires_at=self.poll["expires_at"],
                    expired=self.poll["expired"],
                    multiple=self.poll["multiple"],
                    votes_count=self.poll["votes_count"],
                    voters_count=self.poll["voters_count"],
                    voted=self.poll["voted"],
                    own_votes=self.poll["own_votes"],
                    options=self.poll["options"],
                )
            )
        media_attachments_widgets = []
        for media in self.media_attachments:  # type: ignore[union-attr]
            media_type: str = media["type"]  # type: ignore[assignment]
            media_url: str = media["url"]  # type: ignore[assignment]
            media_description: str = media["description"]  # type: ignore[assignment]
            media_attachments_widgets.append(
                Media(
                    media_type=media_type,
                    url=media_url,
                    description=media_description,
                )
            )

        yield Center(
            spoiler,
            Static(visibility_emojis[self.visibility], classes="visibility"),
            author,
            *content,
            *poll_widget,
            *media_attachments_widgets,
            Horizontal(
                Button(
                    f"Like {self.favourites_count}",
                    classes=f"button {favourite_button_class}",
                    id="favourite",
                ),
                Button(
                    f"Boost {self.reblogs_count}",
                    classes=f"button {boost_button_class}",
                    id="boost",
                ),
                comments_button,
                Button("Reply", classes="button", id="reply"),
                Button(
                    "Bookmark",
                    classes=f"button {bookmark_button_class}",
                    id="bookmark",
                ),
                classes="buttons",
            ),
            classes=post_class,
        )

    @on(Button.Pressed, "#favourite")
    def favourite_post(self) -> None:
        if not self.favourited:
            _, response = self.masto_api.favourite_post(post_id=self.post_id)
            if response["favourited"]:
                self.favourited = True
                self.query_one("#favourite").add_class("favourited")
                self.favourites_count += 1
                self.query_one("#favourite").label = f"Like {self.favourites_count}"
                self.query_one("#favourite").refresh()
        else:
            _, response = self.masto_api.unfavourite_post(post_id=self.post_id)
            if not response["favourited"]:
                self.favourited = False
                self.query_one("#favourite").remove_class("favourited")
                self.favourites_count -= 1
                self.query_one("#favourite").label = f"Like {self.favourites_count}"
                self.query_one("#favourite").refresh()

    @on(Button.Pressed, "#boost")
    def boost_post(self) -> None:
        if not self.boosted:
            _, response = self.masto_api.boost_post(post_id=self.post_id)
            if response.get("reblogged"):
                self.boosted = True
                self.query_one("#boost").add_class("boosted")
                self.reblogs_count += 1
                self.query_one("#boost").label = f"Boost {self.reblogs_count}"
                self.query_one("#boost").refresh()
        else:
            _, response = self.masto_api.unboost_post(post_id=self.post_id)
            if not response["reblogged"]:
                self.boosted = False
                self.query_one("#boost").remove_class("boosted")
                self.reblogs_count -= 1
                self.query_one("#boost").label = f"Boost {self.reblogs_count}"
                self.query_one("#boost").refresh()

    @on(Button.Pressed, "#bookmark")
    def bookmark_post(self) -> None:
        if self.reblogger:
            post_id = self.original_post_id
        else:
            post_id = self.post_id
        if not self.bookmarked:
            _, response = self.masto_api.bookmark_post(post_id=post_id)  # type: ignore[arg-type]
            if response["bookmarked"]:
                self.bookmarked = True
                self.query_one("#bookmark").add_class("bookmarked")
                self.query_one("#bookmark").refresh()
        else:
            _, response = self.masto_api.unbookmark_post(post_id=post_id)  # type: ignore[arg-type]
            if not response["bookmarked"]:
                self.bookmarked = False
                self.query_one("#bookmark").remove_class("bookmarked")
                self.query_one("#bookmark").refresh()

    @on(Button.Pressed, "#hide_spoiler")
    def hide_spoiler_alert(self) -> None:
        self.query_one("#spoiler").remove()

    @on(Button.Pressed, "#details")
    def go_to_post_details(self) -> None:
        try:
            from .post_details import PostDetails
        except ImportError:
            from post_details import PostDetails  # type: ignore[no-redef]
        if self.original_post_id is not None:
            post_id = self.original_post_id
        else:
            post_id = self.post_id
        self.app.push_screen(PostDetails(post_id=post_id))

    @on(Button.Pressed, "#reply")
    def reply_to_post(self):
        try:
            from .new_post_form import NewPostForm
        except ImportError:
            from new_post_form import NewPostForm
        if self.original_post_id is not None:
            post_id = self.original_post_id
        else:
            post_id = self.post_id
        self.app.push_screen(
            NewPostForm(
                in_reply_to=post_id,
                reply_to_content=self.content,
                visibility=self.visibility,
            )
        )


class Media(Static):
    def __init__(self, media_type: str, url: str, description: str) -> None:
        super().__init__()
        self.media_type = media_type
        self.url = url
        self.description = description

    def compose(self) -> ComposeResult:
        if self.description:
            yield Center(
                Static(f"{self.media_type.title()}: [u]{self.url}[/]", classes="media"),
                Static(f"ALT: {self.description}", classes="media"),
                classes="media_attachment",
            )
        else:
            yield Center(
                Static(f"{self.media_type.title()}: {self.url}", classes="media"),
                classes="media_attachment",
            )
