from datetime import datetime
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from textual import on  # type: ignore[attr-defined]
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Checkbox, Static

try:
    from api import MastoAPI
except ImportError:
    from .api import MastoAPI  # type: ignore[no-redef]


class Poll(Static):
    CSS_PATH = "style.css"

    def __init__(
        self,
        poll_id: int,
        expires_at: str,
        expired: bool,
        multiple: bool,
        votes_count: int,
        voters_count: int,
        voted: bool,
        own_votes: List[int],
        options: Dict[str, Any],
    ) -> None:
        super().__init__()
        self.masto_api = MastoAPI()
        self.poll_id = poll_id
        self.expires_at = expires_at
        self.expired = expired
        self.multiple = multiple
        self.votes_count = votes_count
        self.voters_count = voters_count
        self.voted = voted
        self.own_votes = own_votes
        self.options = options
        self.options_widgets = self.prepare_poll_widgets(self.options)

    def compose(self) -> ComposeResult:
        yield Container(
            Static(
                "Multiple choice" if self.multiple else "Single choice",
                classes="poll_choice_indicator",
            ),
            *self.options_widgets,
            Button(
                "Vote",
                classes="buttons",
                disabled=self.voted,
                id="vote_button",
            ),
            Static(
                f"{self.voters_count} voters. Expires in {self.calculate_poll_time_left()} hours"
            ),
            classes="poll",
        )

    def calculate_poll_time_left(self):
        # Parse the future date string
        poll_ends_date = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
        # Get the current time in UTC
        now = datetime.now(ZoneInfo("UTC"))
        # Calculate the time difference
        time_difference = poll_ends_date - now
        # Calculate total hours and round to the nearest integer
        total_hours = round(time_difference.total_seconds() / 3600)
        return int(total_hours)

    def prepare_poll_widgets(self, options: Dict[str, Any]) -> List[Any]:
        options_widgets = []
        disable_checkboxes = False
        if self.voted:
            disable_checkboxes = True
        for option_index, option in enumerate(options):
            value = option_index in self.own_votes
            percent_of_votes = self.calculate_percentage(
                option["votes_count"]  # type:ignore[arg-type, index]
            )
            option_widget = Container(
                Checkbox(
                    f"{option['title']} ({percent_of_votes}%)",  # type:ignore[index]
                    disabled=disable_checkboxes,
                    value=value,
                    id=f"option_{option_index}",
                ),
                classes="poll_option",
            )
            options_widgets.append(option_widget)
        return options_widgets

    def calculate_percentage(self, votes_count: int) -> int:
        if self.votes_count == 0:
            return 0
        percentage = round((votes_count / self.votes_count) * 100)
        return percentage

    @on(Button.Pressed, "#vote_button")
    def vote(self) -> None:
        options_ids = list(range(len(self.options)))
        choices = []
        for option_id in options_ids:
            if self.query_one(f"#option_{option_id}").value:
                choices.append(option_id)
        if len(choices) == 0:
            return
        status_code, response = self.masto_api.vote_in_poll(self.poll_id, choices)
        self.options = response["options"]
        self.votes_count = response["votes_count"]
        self.voters_count = response["voters_count"]
        self.voted = response["voted"]
        if status_code == 200:
            self.query_one("#vote_button").disabled = True
            self.query_one("#vote_button").refresh()
            for option_id, option in enumerate(self.options):
                percent_of_votes = self.calculate_percentage(
                    option["votes_count"]  # type:ignore[arg-type, index]
                )
                self.query_one(f"#option_{option_id}").disabled = True
                self.query_one(
                    f"#option_{option_id}"
                ).label = (
                    f"{option['title']} ({percent_of_votes}%)"  # type:ignore[index]
                )
                self.query_one(f"#option_{option_id}").refresh()

    @on(Checkbox.Changed, "#option_0")
    def option_0(self) -> None:
        if self.query_one("#option_0").value and not self.multiple:
            options = list(range(len(self.options)))
            options.remove(0)
            for ind in options:
                self.query_one(f"#option_{ind}").value = False

    @on(Checkbox.Changed, "#option_1")
    def option_1(self) -> None:
        if self.query_one("#option_1").value and not self.multiple:
            options = list(range(len(self.options)))
            options.remove(1)
            for ind in options:
                self.query_one(f"#option_{ind}").value = False

    @on(Checkbox.Changed, "#option_2")
    def option_2(self) -> None:
        if self.query_one("#option_2").value and not self.multiple:
            options = list(range(len(self.options)))
            options.remove(2)
            for ind in options:
                self.query_one(f"#option_{ind}").value = False

    @on(Checkbox.Changed, "#option_3")
    def option_3(self) -> None:
        if self.query_one("#option_3").value and not self.multiple:
            options = list(range(len(self.options)))
            options.remove(3)
            for ind in options:
                self.query_one(f"#option_{ind}").value = False
