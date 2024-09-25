from textual.app import App, ComposeResult

try:
    from .api import MastoAPI
    from .login_form import LoginForm
    from .screens import HomeTimelineScreen, LocalTimelineScreen, GlobalTimelineScreen
    from .new_post_form import NewPostForm
    from .trendings import Trendings
except ImportError:
    from api import MastoAPI  # type: ignore[no-redef]
    from login_form import LoginForm  # type: ignore[no-redef]
    from screens import HomeTimelineScreen, LocalTimelineScreen, GlobalTimelineScreen  # type: ignore[no-redef]
    from new_post_form import NewPostForm  # type: ignore[no-redef]
    from trendings import Trendings  # type: ignore[no-redef]


class Textualodon(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("1", "show_tab('home_timeline')", "Home timeline"),
        ("2", "show_tab('local_timeline')", "Local timeline"),
        ("3", "show_tab('global_timeline')", "Global timeline"),
        ("4", "show_tab('trendings')", "Trendings"),
        ("w", "add_post", "Add new post"),
        ("q", "quit", "Quit"),
    ]
    CSS_PATH = "style.css"
    SCREENS = {
        "login_form": LoginForm,
        "home_timeline": HomeTimelineScreen,
        "local_timeline": LocalTimelineScreen,
        "global_timeline": GlobalTimelineScreen,
        "trendings": Trendings,
    }

    def __init__(self) -> None:
        super().__init__()
        self.masto_api = MastoAPI()

    def on_mount(self) -> ComposeResult:
        """Create child widgets for the app."""
        if not self.masto_api.verify_keys():
            self.push_screen(LoginForm())
        else:
            self.push_screen(HomeTimelineScreen())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark  # type: ignore[has-type]

    def action_quit(self) -> None:
        """An action to quit the app."""
        self.app.exit()

    def action_show_tab(self, tab: str) -> None:
        """An action to show a tab."""
        self.push_screen(self.SCREENS[tab]())

    def action_add_post(self) -> None:
        """An action to add a post."""
        self.push_screen(NewPostForm())

    def action_open_link(self, link: str) -> None:
        self.app.bell()
        import webbrowser

        webbrowser.open(link)


if __name__ == "__main__":
    app = Textualodon()
    app.run()
