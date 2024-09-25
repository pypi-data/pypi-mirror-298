from typing import List, Optional

from textual import on  # type: ignore[attr-defined]
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    Select,
    Static,
    TextArea,
)

try:
    from api import MastoAPI
    from constants import poll_expiration_time, post_languages
    from post_details import PostDetails
except ImportError:
    from .api import MastoAPI
    from .constants import poll_expiration_time, post_languages
    from .post_details import PostDetails


class NewPostForm(Screen):
    BINDINGS = [
        ("b", "go_back", "Go back"),
    ]
    CSS_PATH = "style.css"

    current_status_length = reactive(0)

    def __init__(
        self,
        in_reply_to: Optional[str] = None,
        reply_to_content: Optional[List[str]] = None,
        visibility: str = "public",
    ) -> None:
        self.masto_api = MastoAPI()
        self.status_limit = self.masto_api.get_instance_status_limit()
        self.in_reply_to = in_reply_to
        self.reply_to_content = reply_to_content
        self.visibility = visibility
        self.status_limit = self.masto_api.get_instance_status_limit()

        super().__init__()

    def on_mount(self):
        self.set_interval(1 / 60, self.update_current_status_length)

    def update_current_status_length(self):
        self.current_status_length = len(self.query_one(TextArea).text)

    def watch_current_status_length(self):
        status_length = self.query_one("#status_length")
        status_length.update(f"{ self.status_limit - self.current_status_length }")
        if self.status_limit - self.current_status_length < 0:
            status_length.add_class("toot_too_long")
        else:
            status_length.remove_class("toot_too_long")

    def compose(self) -> ComposeResult:
        if self.in_reply_to is None:
            title_widget = Static("Add new post", id="title")
        else:
            if self.reply_to_content is not None:
                if len(self.reply_to_content) > 1:
                    content = [
                        Static(line, classes="post_content")
                        for line in self.reply_to_content
                    ]
                else:
                    try:
                        content = [
                            Static(self.reply_to_content[0], classes="post_content")
                        ]
                    except IndexError:
                        content = []
            else:
                content = []
            title_widget = Container(Static("In reply to:"), *content, id="title")
        yield ScrollableContainer(
            Header(),
            title_widget,
            TextArea(id="post_content"),
            Static("Text can't be blank!", id="post_content_empty"),
            Static(
                f"{self.status_limit}",
                id="status_length",
            ),
            Horizontal(
                Label("Visibility", classes="horizontal_label"),
                Select(
                    options=[
                        [val, val]
                        for val in ["public", "unlisted", "private", "direct"]
                    ],
                    allow_blank=False,
                    value="public" if self.visibility != "direct" else "direct",
                    id="visibility",
                ),
                Checkbox("CW", id="cw_checkbox"),
                Checkbox("Poll", id="poll_checkbox"),
                Label("Language", classes="horizontal_label"),
                Select(
                    options=[[key, val] for key, val in post_languages.items()],
                    allow_blank=False,
                    value="en",
                    id="post_language",
                ),
            ),
            Container(
                Label("Content Warning", classes="label"),
                Input(id="cw_content"),
                id="cw_container",
            ),
            Container(
                Horizontal(
                    Checkbox("Allow multiple choices", id="multiple_choice"),
                    Checkbox("Hide total votes", id="hide_total"),
                ),
                Horizontal(
                    Label("Choice 1", classes="horizontal_label"),
                    Input(id="choice_1"),
                ),
                Horizontal(
                    Label("Choice 2", classes="horizontal_label"),
                    Input(id="choice_2"),
                ),
                Horizontal(
                    Label("Choice 3", classes="horizontal_label"),
                    Input(id="choice_3"),
                ),
                Horizontal(
                    Label("Choice 4", classes="horizontal_label"),
                    Input(id="choice_4"),
                ),
                Static(
                    "Polls have to have at least two options",
                    id="poll_not_enough_options",
                ),
                Horizontal(
                    Label("Expiration date", classes="horizontal_label"),
                    Select(
                        options=[
                            [key, val] for key, val in poll_expiration_time.items()
                        ],
                        allow_blank=False,
                        value=300,
                        id="poll_expiration",
                    ),
                ),
                id="poll_container",
            ),
            Button("Submit", id="submit"),
            Footer(),
        )

    def action_go_back(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#submit")
    def submit(self) -> None:
        post_content = self.query_one("#post_content").text
        if not post_content:
            self.query_one("#post_content_empty").styles.display = "block"
            return
        else:
            self.query_one("#post_content_empty").styles.display = "none"
        visibility = self.query_one("#visibility").value
        multiple_choice = self.query_one("#multiple_choice").value
        hide_total = self.query_one("#hide_total").value
        content_warning = None
        poll_options = None
        sensitive = False
        poll_expiration = 300
        if self.query_one("#cw_checkbox").value:
            sensitive = True
            content_warning = self.query_one("#cw_content").value
        if self.query_one("#poll_checkbox").value:
            poll_expiration = self.query_one("#poll_expiration").value
            poll_options = [
                self.query_one("#choice_1").value,
                self.query_one("#choice_2").value,
                self.query_one("#choice_3").value,
                self.query_one("#choice_4").value,
            ]
            for i in range(len(poll_options) - 1, 0, -1):
                if not poll_options[i]:
                    del poll_options[i]
            if len(poll_options) < 2:
                self.query_one("#poll_not_enough_options").styles.display = "block"
                return
            else:
                self.query_one("#poll_not_enough_options").styles.display = "none"
        status_code, result = self.masto_api.add_post(
            post_content=post_content,
            sensitive=sensitive,
            visibility=visibility,
            content_warning=content_warning,
            poll_options=poll_options,
            multiple_choice=multiple_choice,
            hide_total=hide_total,
            poll_expiration=poll_expiration,
            in_reply_to=self.in_reply_to,
        )
        if status_code == 200:
            self.app.push_screen(PostDetails(post_id=result["id"]))

    @on(Checkbox.Changed, "#cw_checkbox")
    def change_cw(self) -> None:
        if self.query_one("#cw_checkbox").value:
            self.query_one("#cw_container").styles.display = "block"
        else:
            self.query_one("#cw_container").styles.display = "none"

    @on(Checkbox.Changed, "#poll_checkbox")
    def change_poll(self) -> None:
        if self.query_one("#poll_checkbox").value:
            self.query_one("#poll_container").styles.display = "block"
        else:
            self.query_one("#poll_container").styles.display = "none"
