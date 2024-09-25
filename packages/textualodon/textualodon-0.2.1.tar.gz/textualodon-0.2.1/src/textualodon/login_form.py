from textual import on  # type: ignore[attr-defined]
from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Label, Input, Button

try:
    from .api import MastoAPI
    from .app_logo import AppLogo
except ImportError:
    from api import MastoAPI  # type: ignore[no-redef]
    from app_logo import AppLogo  # type: ignore[no-redef]


class LoginForm(Screen):
    CSS_PATH = "style.css"

    def __init__(self) -> None:
        super().__init__()
        self.masto_api = MastoAPI()

    def compose(self) -> ComposeResult:
        yield Header()
        yield AppLogo()
        yield Center(
            Label("Instance URL", classes="login-form"),
            Input(id="url", classes="login-form", value=self.masto_api.instance_url),
            Label("Client ID", classes="login-form"),
            Input(id="client_id", classes="login-form", value=self.masto_api.client_id),
            Label("Client Secret", classes="login-form"),
            Input(
                id="client_secret",
                password=True,
                classes="login-form",
                value=self.masto_api.client_secret,
            ),
            Button("Login", id="loginButton", classes="login-form"),
            Label("Grant Token", classes="login-form grant_token"),
            Input(id="grant_token", password=True, classes="login-form grant_token"),
            Static(
                "Login successful! Reopen the app to continue.",
                classes="login-form login-success",
                id="login-success",
            ),
            id="login-form",
        )
        yield Footer()

    @on(Button.Pressed, "#loginButton")
    def login_pressed(self) -> None:
        instance_url = self.query_one("#url").value
        if instance_url and not instance_url.startswith("https://"):
            instance_url = "https://" + instance_url
        self.masto_api.instance_url = instance_url
        self.masto_api.client_id = self.query_one("#client_id").value
        self.masto_api.client_secret = self.query_one("#client_secret").value
        self.masto_api.grant_token = self.query_one("#grant_token").value
        if not self.masto_api.grant_token:
            self.masto_api.get_grant_token()
            for elem in self.query(".grant_token"):
                elem.display = "block"
        if not self.masto_api.access_token:
            self.masto_api.get_access_token()
        self.masto_api.write_config()
        if self.masto_api.verify_keys():
            self.query_one("#login-success").display = "block"
